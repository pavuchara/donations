FROM python:3.12.0-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install gunicorn==23.0.0
RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "donations.wsgi"]
