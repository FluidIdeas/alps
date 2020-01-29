#!/bin/bash

. /etc/alps/alps.conf

set -e

echo "Cleaning up..."
sudo rm -rf $SOURCE_DIR/*
echo "Done."