FROM python:3.11-slim

RUN mkdir /max_container

WORKDIR /max_container

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .



RUN chmod +x ./docker/max_app.sh
CMD ["python", "main.py"]