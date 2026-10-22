#
# docker build . -t your-repo/hello-bolt
#
FROM python:3.13-alpine3.24 AS builder
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.13-alpine3.24 AS app
# eMudhra 53119: refresh the OS trust store and fail the build unless
# ca-certificates carries the distrust fix (>= 20261020-r0).
ARG CA_CERTIFICATES_REFRESH=2026-10-21
RUN set -eu; \
    apk add --no-cache --upgrade ca-certificates ca-certificates-bundle; \
    for p in ca-certificates ca-certificates-bundle; do \
      v="$(apk info -e -v "$p" | sed "s/^$p-//")"; \
      if [ "$(apk version -t "$v" 20261020-r0)" = "<" ]; then \
        echo "ca-certificates gate FAILED: $p $v < 20261020-r0" >&2; exit 1; \
      fi; \
      echo "ca-certificates gate OK: $p $v >= 20261020-r0"; \
    done
WORKDIR /app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY main.py /app/
ENTRYPOINT uvicorn main:asgi_app --port $PORT --workers 1

#
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e PORT=3000 -p 3000:3000 -it your-repo/hello-bolt
#
