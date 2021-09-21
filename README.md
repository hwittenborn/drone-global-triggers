<div align=center><h1>drone-global-triggers</h1></div>

## Introduction
drone-global-trigers is a [validation extension](https://docs.drone.io/extensions/validation/) for Drone CI, allowing you to globally specify what [build event types](https://docs.drone.io/pipeline/docker/syntax/trigger/#by-event) are allowed to run on your CI servers.

## Installing
The only supported way for running is through the official Docker image which can be pulled from the following repository:

```
proget.hunterwittenborn.com/docker/hwittenborn/drone-global-triggers
```

## Running
First, set the `DRONE_VALIDATE_PLUGIN_ENDPOINT` and `DRONE_VALIDATE_PLUGIN_SECRET` environment variables under the config of your Drone server (i.e. the config for the service runnning the `drone/drone` Docker image).

After, create the `drone-global-triggers` container, configured as follows:

- Pass the `DRONE_VALIDATE_PLUGIN_SECRET` variable, with its value set the same as that set under the config for your Drone server.

- Pass the `ALLOWLIST` variable, which should be a comma-separated list of [build events](https://docs.drone.io/pipeline/docker/syntax/trigger/#by-event) that are allowed to run.

- Bind a public port to the container's internal port `8080`.

For example:

```sh
docker run -p "8080:8080" \
           -e "DRONE_VALIDATE_PLUGIN_SECRET=your_secret_here" \
           -e "ALLOWLIST=push,cron,custom"
           proget.hunterwittenborn.com/docker/hwittenborn/drone-global-triggers
```

## Support
Issues and questions regarding usage should be posted under the issue tracker.
