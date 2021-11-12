FROM python:3.9-alpine

COPY requirements.txt ./

RUN apk add linux-headers build-base
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./index.py"]