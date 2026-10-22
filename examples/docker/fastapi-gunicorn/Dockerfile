#
# docker build . -t your-repo/hello-bolt
#
FROM python:3.13-slim-trixie
# eMudhra 53119: refresh the OS trust store and fail the build unless the
# ca-certificates package carries the distrust fix for this Debian suite.
ARG CA_CERTIFICATES_REFRESH=2026-10-21
RUN set -eu; \
    . /etc/os-release; \
    case "$VERSION_CODENAME" in \
      bookworm) min="20250419~deb12u2" ;; \
      trixie) min="20250419+deb13u1" ;; \
      *) echo "ca-certificates gate: no fixed package known for '$VERSION_CODENAME'" >&2; exit 1 ;; \
    esac; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates; \
    rm -rf /var/lib/apt/lists/*; \
    v="$(dpkg-query -W -f='${Version}' ca-certificates)"; \
    if dpkg --compare-versions "$v" ge "$min"; then \
      echo "ca-certificates gate OK: $VERSION_CODENAME $v >= $min"; \
    else \
      echo "ca-certificates gate FAILED: $VERSION_CODENAME $v < $min" >&2; exit 1; \
    fi
WORKDIR /app/
COPY *.py /app/
COPY requirements.txt /app/
RUN pip install -U pip && pip install -r requirements.txt
# Previously provided by tiangolo/uvicorn-gunicorn (Python 3.8, EOL):
# gunicorn with uvicorn workers serving $MODULE_NAME:$VARIABLE_NAME on port 80.
ENV MODULE_NAME=main VARIABLE_NAME=app PORT=80
CMD exec gunicorn --worker-class uvicorn_worker.UvicornWorker --bind "0.0.0.0:$PORT" "$MODULE_NAME:$VARIABLE_NAME"

#
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e VARIABLE_NAME="api" -p 80:80 -it your-repo/hello-bolt
# or
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e VARIABLE_NAME="api" -p 3000:80 -it your-repo/hello-bolt
