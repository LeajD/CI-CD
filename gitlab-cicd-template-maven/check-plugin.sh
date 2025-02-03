echo 'running check-plugin.sh script ...'
curl -k -u admin:JUSTFORTESTINGGG "http://dind-1:9000/api/system/plugins" -vvv

value=$(curl -k -u admin:JUSTFORTESTINGGG -s "http://dind-1:9000/api/system/plugins" | jq '.plugins[] | select(.name == "SingleSignOn").name')
if [ "$value" == "null" ] || [ "$value" == "" ]; then
  echo "Error: $CI_PROJECT_NAME  plugin not found !"
  #exit 1
else
  echo "$CI_PROJECT_NAME plugin found !"
fi
