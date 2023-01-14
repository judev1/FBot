FROM alpine:latest
WORKDIR /usr/src/app
RUN apk update
RUN apk add bash git build-base python3-dev imagemagick jpeg-dev zlib-dev freetype-dev
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY . .

CMD [ "python3", "app.py" ]