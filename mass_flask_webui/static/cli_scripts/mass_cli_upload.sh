#!/usr/bin/env bash
set -e

API_URL=""
COMMENT=""

usage() {
	echo "Usage: $0 -u <api_url> (-d <directory>|-f <file>) [-c <comment>]"
	exit 1
}

upload_file() {
    if [ -z ${API_URL} ];
    then
        echo "API URL not configured. Aborting."
        exit 1
    fi
    echo "Submitting $1"
    if [ ! -z "${COMMENT}" ];
    then
        curl -X POST -H "Content-Type:multipart/form-data" -F "metadata={\"comment\": \"${COMMENT}\"};type=application/json" -F "file=@$1;type=binary/octet-stream" ${API_URL}/sample/submit_file/
    else
        curl -X POST -H "Content-Type:multipart/form-data" -F "file=@$1;type=binary/octet-stream" ${API_URL}/sample/submit_file/
    fi
}

upload_directory() {
find $1 -type f -print0 | while IFS= read -r -d $'\0' line; do
    upload_file $line
done
}

# Get parameters
while getopts ":u:d:f:c:" opt; do
	case $opt in
	u)
		API_URL=$OPTARG
		;;
	d)
		DIRECTORY=$OPTARG
		;;
	f)
		FILE=$OPTARG
		;;
	c)
	    COMMENT=$OPTARG
	    ;;
	\?)
		usage
		;;
	esac
done

if [ -z ${API_URL} ];
then
    echo "API URL not configured. Aborting."
    usage
    exit 1
fi

if [ ! -z ${DIRECTORY} ];
then
    echo "Uploading files from $DIRECTORY ..."
	upload_directory ${DIRECTORY}
	echo "Finished."
	exit 0
fi

if [ ! -z ${FILE} ];
then
	upload_file ${FILE}
	echo "Finished."
	exit 0
fi
