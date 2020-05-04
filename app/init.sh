#!/usr/bin/env bash


mkdir -p /var/lib/yt-classifier/lists-avaliable
mkdir -p /var/lib/yt-classifier/lists-enabled
cp -rv /yt-classifier/lists/nudity /var/lib/yt-classifier/lists-avaliable/

cd /var/lib/yt-classifier/
ln -sv lists-enabled lists

cd lists-enabled

ln -sv ../lists-avaliable/nudity

