FROM python:3.11-rc-slim
WORKDIR /user/src/app

COPY worker.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./worker.py"]
