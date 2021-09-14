FROM alpine:3.14.2

ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk add shadow
RUN apk add --no-cache --update python3 py3-pip npm

# Add User
RUN useradd runner
RUN apk del shadow

# Move websocket code
COPY . /ws/.
RUN chmod +x /ws/server.py

# Install websocket node dependencies
RUN npm install

USER runner
WORKDIR /home/runner/

ENTRYPOINT ['node', '/ws/server.js']
