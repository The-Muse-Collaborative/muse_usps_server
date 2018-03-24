FROM python:3.6.4-alpine3.7
WORKDIR /usr/src/app
EXPOSE 8000

COPY requirements.txt ./
RUN apk add --update --no-cache g++ gcc git libxslt-dev
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del g++ gcc git

COPY . .

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "muse_usps_server:APPLICATION"]
