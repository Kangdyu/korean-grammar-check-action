FROM python:3.10.4-alpine

RUN apk add --no-cache build-base

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /korean-grammar-check-action

RUN apk add --no-cache git

ENV GIT_PYTHON_REFRESH quiet

RUN chmod +x /korean-grammar-check-action/grammar_checker/main.py
ENTRYPOINT ["python", "/korean-grammar-check-action/grammar_checker/main.py"]