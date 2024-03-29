FROM python:3.11-alpine

WORKDIR /urlminifier

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /urlminifier

EXPOSE 8000

ENV HOST=0.0.0.0

CMD ["python","app.py"]
