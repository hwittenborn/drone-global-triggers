FROM python:3.12

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

COPY ./src/ /usr/local/share/drone-global-triggers
WORKDIR /usr/local/share/drone-global-triggers
ENTRYPOINT ["python", "-um", "hypercorn", "main:app", "--bind", "0.0.0.0:8080"]
