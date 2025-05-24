FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get install -y curl unzip
RUN curl -LO https://github.com/VOICEVOX/voicevox_engine/releases/download/0.22.2/voicevox_engine-linux-x64-cpu-0.22.2.zip \
  && unzip voicevox_engine-linux-x64-cpu-0.22.2.zip -d /app/voicevox_engine \
  && chmod +x /app/voicevox_engine/run.sh

COPY . /app
COPY start.sh /app
RUN chmod +x /app/start.sh

EXPOSE 5000
EXPOSE 50021

CMD ["/app/start.sh"]
