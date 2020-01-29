#!/bin/bash

set -e

SEARCH_TEXT1="$1=>"
SEARCH_TEXT2="$1:"

grep -v "$SEARCH_TEXT1" $INSTALLED_LIST > /tmp/modified-installed
grep -v "$SEARCH_TEXT2" $VERSION_LIST > /tmp/modified-versions

sudo mv /tmp/modified-installed $INSTALLED_LIST
sudo mv /tmp/modified-versions $VERSION_LIST
