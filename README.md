# repl
Coding as a service

## Structure
*subject to change*

1. Manager Server
2. Dockerized sandbox environment

## Note:
On Windows you must use this additional config for the server to run 
and connect to docker.sock correctly

```
server:
  ...
  environment:
    - COMPOSE_CONVERT_WINDOWS_PATHS=1
  volumes:
    - //var/run/docker.sock:/var/run/docker.sock
```
