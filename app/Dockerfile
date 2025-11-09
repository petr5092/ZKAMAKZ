FROM python:3.11-slim

RUN mkdir /max_container

WORKDIR /max_container

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

COPY ./docker/*.sh /max_container/docker/

CMD ["python", "main.py"]