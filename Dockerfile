FROM python:3.8-slim
WORKDIR /code
COPY . /code/
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev libpcre3-dev postgresql-client \
    && apt-get -y autoremove
RUN pip install --no-cache-dir -r requirements/development.txt
RUN mkdir -p /var/log/sharpshort
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
CMD ["init"]
