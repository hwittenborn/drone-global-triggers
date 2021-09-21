import base64
import hashlib
import hmac
import json
import logging
import os
import re
import traceback

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

# Validate we have all needed environment variables.
for i in ["DRONE_VALIDATE_PLUGIN_SECRET", "ALLOWLIST"]:
    if os.environ.get(i) is None:
        print(f"[Error] {i} isn't set, but is needed to function.")
        exit(1)

plugin_secret = os.environ.get("DRONE_VALIDATE_PLUGIN_SECRET")
allowlist = os.environ.get("ALLOWLIST").split(",")


# Define main function.
async def entrypoint(request, response):
    headers = request.headers
    body = (await request.body()).decode()

    # Get needed JSON data.
    json_body = json.loads(body)
    build_link = json_body["build"]["link"]

    # Verify digest.
    digest = headers.get("digest").split("=")
    digest_title = digest[0]
    digest_string = "=".join(digest[1:])

    calculated_digest = hashlib.sha256(body.encode()).digest()
    calculated_digest_base64 = base64.b64encode(calculated_digest).decode()

    if calculated_digest_base64 != digest_string:
        print(f"[Error] Sent data didn't match recorded digest hash ({build_link}).")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Digest hash didn't match recorded data."}

    signature = headers.get("signature").split(',')

    # Make sure we have the signature header.
    if signature is None:
        print(f"[Error] Couldn't find the signature header ({build_link}).")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Couldn't find the signature header."}

    # Get list of signature headers we need to verify.
    for i in signature:
        if re.search("^headers=", i) is not None:
            signature_headers = re.sub('^headers=|"', "", i).split(" ")

    # Generate HMAC string.
    hmac_verification_string = ""

    for i in signature_headers:
        current_header_value = headers.get(i)

        if current_header_value is None:
            print(f"[Error] Couldn't find needed header '{i} ({build_link})'.")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Headers missing in request."}

        hmac_verification_string += f"{i}: {current_header_value}\n"

    # Strip the leading newline from the verification string.
    hmac_verification_string = hmac_verification_string.strip()

    # base64-encode the HMAC signature.
    hmac_digest = hmac.digest(plugin_secret.encode(), hmac_verification_string.encode(), hashlib.sha256)
    hmac_digest_base64 = base64.b64encode(hmac_digest).decode()

    # Verify that we should allow the build to run.
    build_event = json_body["build"]["event"]

    if build_event in allowlist:
        return JSONResponse(status_code=200, content={"hi":"me"})

    else:
        return JSONResponse(status_code=498)


# Actually run everything
app = FastAPI()

@app.post("/")
async def main(request: Request, response: Response):
    try:
        return await entrypoint(request, response)
    except Exception as error:
        print(f"[Error] An unknown error has occurred.")
        logging.error(traceback.format_exc())
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "An unknown error has occurred."}
