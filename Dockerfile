FROM python:3.9

COPY requirements.txt ./

RUN apk add build-base ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./index.py"]