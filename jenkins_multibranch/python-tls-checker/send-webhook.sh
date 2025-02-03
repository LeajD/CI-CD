CONTENT=$(cat /app/domains-info.txt)
curl -i -X POST --data-urlencode "payload={\"text\": \"$CONTENT\"}" $SLACK_URL