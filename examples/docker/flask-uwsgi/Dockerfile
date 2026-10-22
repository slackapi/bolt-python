#
# docker build . -t your-repo/hello-bolt
#
FROM python:3.13-slim-trixie AS builder
RUN apt-get update \
    && apt-get -y install build-essential libpcre2-dev \
    && apt-get clean
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.13-slim-trixie AS app
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
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY *.py /app/
COPY uwsgi.ini /app/
ENTRYPOINT uwsgi --ini uwsgi.ini --http :$PORT

#
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e PORT=3000 -p 3000:3000 -it your-repo/hello-bolt
#