FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/