FROM python:3.12-slim

WORKDIR /app

COPY application/requirements.txt /app/requirements.txt

RUN python -m pip install --no-cache-dir -r /app/requirements.txt

COPY application/app.py /app/app.py

EXPOSE 8085

CMD ["python", "app.py"]