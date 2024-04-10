FROM certbot/certbot:latest

RUN apt-get update && apt-get install -y bash