FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /fast
WORKDIR /fast
COPY . /fast
COPY Pipfile .
RUN pip install pipenv
RUN pipenv install --skip-lock