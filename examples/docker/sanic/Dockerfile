#
# docker build . -t your-repo/hello-bolt
#
FROM python:3.8-slim-bookworm as builder
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.8-slim-bookworm as app
# Refresh the OS trust store so the image gets the latest ca-certificates.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app/
COPY *.py /app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
ENTRYPOINT python main.py

#
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e PORT=3000 -p 3000:3000 -it your-repo/hello-bolt
#
