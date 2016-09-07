#!/usr/bin/env bash

PROFILE=$1
BUCKET=$2
export AWS_PROFILE=$1
export AWS_DEFAULT_PROFILE=$1

echo "<html><body><h1>Bucket $BUCKET Content</h1>" > index.html
aws s3 ls  $BUCKET --recursive|awk '!/index.html/ {print "<a href=\"./"$NF"\">"$NF"</a><br>"}' >> index.html
echo "</body></html>" >> index.html
aws s3 cp index.html s3://$BUCKET
