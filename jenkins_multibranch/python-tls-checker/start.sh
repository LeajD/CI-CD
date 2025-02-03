#!/bin/bash
python /app/tls-checker.py
python /app/tls-checker.py > /app/domains-info.txt
sh /app/send-webhook.sh