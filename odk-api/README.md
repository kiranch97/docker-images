### Tasks

| Description                           | Status      | Prio     | Comments |
| ------------------------------------- | ----------- | -------- | -------- |
| Build app in gunicorn container       | Done        | Must     | |
| Adapt the ODK app to send right format| Done        | Must     | |
| Adapt frame analyser                  | Done        | Must     | |
| Deploy new API + app on staging       | Done        | Must     | Not functional yet though |
| Get WSS connection on staging server  | Done        | Must     | |
| Fix timezone offset for results       | In progress | Must     | Set TZ env var to my timezone + `time.tzset()` |


### Features

| Description                           | Status | Prio     | Comments |
| ------------------------------------- | ------ | -------- |--------------- |
| Receive raw frames                    | Done   | Must     | |
| Put raw frame on queue                | Done   | Must     | |
| Receive analysed frames               | Done   | Must     | |
| Save analysed frame in database       | Done   | Must     | |
| Create detected objects count         | Done   | Must     | |
| Current QR check function             | Done   | Medium   | |
| JWT authentication                    | -      | Should   | |
| User management dashboard             | -      | Could    | Already build by Tiangolo [here](https://github.com/tiangolo/full-stack-fastapi-postgresql) |
| CORS allowed hosts                    | Done   | Medium   | |

### Issues

- When starting up API in Docker with Gunicorn app keeps trying connection in endless loop, for every worker (core)
- Naming a folder `logging` with an `__init__.py` broke the docker proces, since it replaces the python `logging` package

### Gunicorn

- Using the [uvicorn-gunicorn](https://github.com/tiangolo/uvicorn-gunicorn-docker) Dockerfile a worker is spawned for every core in the system.
- It has some more features settings, highly recommended to read through the [config file](https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/gunicorn_conf.py)
- There is an option to run some code only once with `--preload`, but didn't get that working. Now the initialization is happening for every worker again, which is not needed, but also doesn't hurt (I think). Could be improved in the future.

### Sources

- https://github.com/nsidnev/fastapi-realworld-example-app
- https://github.com/tiangolo/full-stack-fastapi-postgresql
- https://www.starlette.io/config/
- https://fastapi.tiangolo.com/tutorial/bigger-applications/
- https://medium.com/@ageitgey/learn-how-to-use-static-type-checking-in-python-3-6-in-10-minutes-12c86d72677b
