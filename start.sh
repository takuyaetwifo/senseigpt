#!/bin/bash

# VOICEVOX Engine（バックグラウンド起動）
/opt/voicevox_engine/run.sh --host 0.0.0.0 --use_gpu false &

# Flaskアプリ（フォアグラウンド起動、必要なら GunicornにしてもOK）
python app.py
