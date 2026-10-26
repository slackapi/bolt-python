#
# docker build . -t your-repo/hello-bolt
#
FROM python:3.11-alpine3.20 as builder
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.11-alpine3.20 as app
# Refresh the OS trust store so the image gets the latest ca-certificates.
RUN apk add --no-cache --upgrade ca-certificates ca-certificates-bundle
WORKDIR /app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY main.py /app/
ENTRYPOINT uvicorn main:asgi_app --port $PORT --workers 1

#
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e PORT=3000 -p 3000:3000 -it your-repo/hello-bolt
#
