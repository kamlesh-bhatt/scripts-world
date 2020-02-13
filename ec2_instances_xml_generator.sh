#!/bin/bash
APP=$(aws ec2 describe-instances --query 'Reservations[].Instances[].[ [Tags[?Key==`Application Name`].Value][0][0] ]'  --output text )
for fn in $APP; do echo "$fn" >> a.txt; done
APP=$(cat a.txt | sort -u)
#rm -f a.txt
ENV[3]='Corporation'
ENV[2]='Test'
ENV[1]='Staging'
ENV[0]='Production'
echo '<EC2>' > /var/www/html/index2.xml
for i in "${ENV[@]}"
do
  numPenv=$(aws ec2 describe-instances --filter Name=tag:'Environment Type',Values=$i --query 'Reservations[].Instances[].[ [Tags[?Key==`Name`].Value][0][0],InstanceType,PrivateIpAddress,PublicIpAddress,State.Name ]' )
  num=$( echo $numPenv | jq length )
  echo '<env name="'$i'" num="'$num'">'  >> /var/www/html/index2.xml
  for j in $APP
  do
    Out=$(aws ec2 describe-instances --filters Name=tag:'Environment Type',Values=$i Name=tag:'Application Name',Values=$j --query 'Reservations[].Instances[].[ [Tags[?Key==`Name`].Value][0][0],InstanceType,PrivateIpAddress,PublicIpAddress,State.Name ]' )
    num_=$( echo $Out | jq length )
    if [ $num_ -ne 0 ]; then
       echo '   <app name="'$j'" num="'$num_'">' >> /var/www/html/index2.xml
       for row in $(echo "${Out}" | jq -c '.[]'); do
           STR="<server name="
           for item in $(echo "${row}" | jq -c '.[]'); do
             if echo $item | grep -i '"SL' >/dev/null; then
                STR=$STR$item
             elif echo $item | egrep '([0-9]{1,3}\.){3}[0-9]{1,3}' | egrep -v '"10|"172|"192'  >/dev/null; then
                STR=$STR" extip="$item
             elif echo $item | egrep '"run|"stop' >/dev/null; then
                STR=$STR" status="$item
             elif echo $item | egrep '([0-9]{1,3}\.){3}[0-9]{1,3}' | egrep '"10|"172|"192' >/dev/null; then
                STR=$STR" intip="$item
             elif echo $item | grep 'null' >/dev/null; then
                STR=$STR' extip="null"'
             else
                STR=$STR" size="$item
             fi
           done
           #echo $STR" />"
           echo $STR" />" >> /var/www/html/index2.xml
       done
       echo '   </app>' >>  /var/www/html/index2.xml
    fi
  done
  echo '</env>' >> /var/www/html/index2.xml
done
echo '</EC2>' >> /var/www/html/index2.xml
cat /var/www/html/index2.xml > /var/www/html/index.xml
