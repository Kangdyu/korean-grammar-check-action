FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./scripts/entrypoint.sh
ENTRYPOINT ["./scripts/entrypoint.sh"]