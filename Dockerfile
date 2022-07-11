FROM python:3.10.4-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apk add --no-cache git

ENV GIT_PYTHON_REFRESH quiet

RUN chmod +x ./grammar_checker/main.py
ENTRYPOINT ["python", "./grammar_checker/main.py"]