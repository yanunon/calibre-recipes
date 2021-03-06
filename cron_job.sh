#! /bin/bash
#
# cron_job.sh
# Copyright (C) 2013 Yang Junyong <yanunon@gmail.com>
#
# Distributed under terms of the MIT license.
#
export LANG="zh_CN.UTF-8"
if [[ $# < 1 ]]; then
    echo 'Usage:cron_job recipe_name'
    exit
fi

SCRIPT=$(readlink -f $0)
DIR=`dirname $SCRIPT`
cd $DIR

DATE=`date +%Y-%m-%d`
RECIPE="$1.recipe"
OUT_FILE="$1_$DATE.mobi"

SUBJECT="$1 [$DATE]"

KINDLE_MAIL="kindle_username@kindle.com"
SENDER_MAIL="gmail_username@gmail.com"
SENDER_USERNAME="gmail_username"
SENDER_PASSWORD="gmail_password"


ebook-convert $RECIPE $OUT_FILE --output-profile kindle
calibre-smtp --attachment=$OUT_FILE --relay=smtp.gmail.com --port=587 --username=$SENDER_USERNAME --password=$SENDER_PASSWORD --encryption-method=TLS $SENDER_MAIL $KINDLE_MAIL "" --subject="$SUBJECT"
