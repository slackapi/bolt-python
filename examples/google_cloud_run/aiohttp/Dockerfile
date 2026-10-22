#
# https://cloud.google.com/run/docs/quickstarts/build-and-deploy
#
# export PROJECT_ID=`gcloud config get-value project`
# export SLACK_SIGNING_SECRET=
# export SLACK_BOT_TOKEN=
# gcloud builds submit --tag gcr.io/$PROJECT_ID/helloworld
# gcloud run deploy helloworld --image gcr.io/$PROJECT_ID/helloworld --platform managed --update-env-vars SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET,SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN
#

# ----------------------------------------------
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim-bookworm

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

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -U pip && pip install -r requirements.txt

# Start AIOHTTP server
ENTRYPOINT python main.py
