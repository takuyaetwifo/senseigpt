#!/bin/bash

# VOICEVOX Engine（バックグラウンド起動）
/opt/voicevox_engine/run.sh --host 0.0.0.0 --use_gpu false &

# Flaskアプリ（フォアグラウンド起動、必要なら GunicornにしてもOK）
python app.py


echo "=== /opt/voicevox_engineの中身 ==="
ls -l /opt/voicevox_engine
echo "=== run.shを実行 ==="
chmod +x /opt/voicevox_engine/run.sh
/opt/voicevox_engine/run.sh --host 0.0.0.0 --use_gpu false &
sleep 3
ps aux | grep voicevox
netstat -tlnp || ss -tlnp

