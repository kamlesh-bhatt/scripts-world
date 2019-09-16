# I had a requirement where i wanted to use fargate for stateful application, for that i used below script to 
# download/uploads files to s3 whenever there is any changes on the folder path /opt/sonarqube you can change this path to anypath
# that you want. From this script i was able to use fargate for stateful applications

while inotifywait -r -e modify,create,delete /opt/sonarqube/; do
aws s3 sync /opt/sonarqube/ s3://sonarqube-server/ --delete
done
