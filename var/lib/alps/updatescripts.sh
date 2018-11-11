#!/bin/bash

set -e

. /etc/lsb-release

VERSION="$DISTRIB_RELEASE"
BASEURL="https://bitbucket.org/chandrakantsingh/aryalinux/get"
TARBALL="$VERSION.tar.bz2"
SCRIPTSDIR="/var/cache/alps/scripts/"

TEMPDIR=$(mktemp -d)
pushd $TEMPDIR &> /dev/null

echo "Fetching scripts..."
wget -q "$BASEURL/$TARBALL"
DIRECTORY=$(tar tf $TARBALL | cut -d/ -f1 | uniq)

tar xf $TARBALL
cd $DIRECTORY/applications/
sudo rm -rf $SCRIPTSDIR/*
sudo cp -rf *.sh $SCRIPTSDIR/
sudo chmod a+x $SCRIPTSDIR/*

popd &> /dev/null
sudo rm -r $TEMPDIR

echo "Scripts updated successfully..."

