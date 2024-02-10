
FROM python:3.8
COPY ./app /code
COPY requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip install --no-cache-dir -r /code/requirements.txt


EXPOSE 8080

COPY entrypoint.sh /code/entrypoint.sh

RUN chmod +x /code/entrypoint.sh
ENTRYPOINT /code/entrypoint.sh
