#
# docker build . -t your-repo/hello-bolt
#
FROM python:3.8.5-slim-buster as builder
RUN apt-get update && apt-get clean
COPY *.py /src/
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.8.5-slim-buster as app
COPY --from=builder /src/ /app/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
EXPOSE 3000
WORKDIR /app/
ENTRYPOINT python app.py

#
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -p 3000:3000 -it your-repo/hello-bolt
#