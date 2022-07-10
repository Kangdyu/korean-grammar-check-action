FROM python:3.10.4-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./grammar_checker/main.py

ENV GIT_PYTHON_REFRESH quiet

ENTRYPOINT ["python", "./grammar_checker/main.py"]