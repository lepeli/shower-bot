FROM python:3.9-alpine

COPY requirements.txt ./

RUN apk add build-base ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./index.py"]