#!/usr/bin/env bash

set -x

DOMAIN="ngtech.home"
COUNTRYCODE="IL"
STATE="Shomron"
REGION="Center"
ORGINZATION="NgTech LTD"
CERTUUID=`uuidgen | awk 'BEGIN { FS="-"}; {print $1}'`
SUBJECDETAILS=`echo -n "/C=$COUNTRYCODE/ST=$STATE/L=$REGION/O=$ORGINAZATION/CN=px$CERTUUID.$DOMAIN"`


echo "Creating private KEY for root CA"
openssl req -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -subj "$SUBJECDETAILS" \
    -extensions v3_ca -keyout /myCA.pem  -out /myCA.pem

echo "Creating der x509 certificate format"
openssl x509 -in /myCA.pem -outform DER -out /myCA-cert.der

openssl x509 -inform DER -in /myCA-cert.der -out /myCA-cert.pem -outform PEM

cat /myCA-cert.pem


set +x
