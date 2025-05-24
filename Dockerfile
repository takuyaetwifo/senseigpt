FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# ここを修正！
RUN apt-get update && apt-get install -y curl p7zip-full

# VOICEVOX Engine (CPU x64, 0.23.0)
RUN curl -LO https://github.com/VOICEVOX/voicevox_engine/releases/download/0.23.0/voicevox_engine-linux-cpu-x64-0.23.0.7z.001 \
 && curl -LO https://github.com/VOICEVOX/voicevox_engine/releases/download/0.23.0/voicevox_engine-linux-cpu-x64-0.23.0.7z.002 \
 && curl -LO https://github.com/VOICEVOX/voicevox_engine/releases/download/0.23.0/voicevox_engine-linux-cpu-x64-0.23.0.7z.003 \
 && curl -LO https://github.com/VOICEVOX/voicevox_engine/releases/download/0.23.0/voicevox_engine-linux-cpu-x64-0.23.0.7z.004 \
 && ls -lh voicevox_engine-linux-cpu-x64-0.23.0.7z.* \
 && 7z x voicevox_engine-linux-cpu-x64-0.23.0.7z.001 -o/app/voicevox_engine \
 && chmod +x /app/voicevox_engine/run.sh

COPY . /app
COPY start.sh /app
RUN chmod +x /app/start.sh

EXPOSE 5000
EXPOSE 50021

CMD ["/app/start.sh"]
