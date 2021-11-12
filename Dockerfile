FROM python:3.9-alpine

COPY requirements.txt ./

RUN apk add ffmpeg linux-headers
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./index.py"]