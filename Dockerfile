FROM python:3-alpine
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY src/ ./

ARG APK_BUILD_DEPS=".build-deps gcc musl-dev linux-headers"
RUN apk add --no-cache --virtual $APK_BUILD_DEPS\
  && pip install --no-cache-dir --requirement requirements.txt \
  && apk del $APK_BUILD_DEPS
CMD [ "python", "ddns_update.py" ]
