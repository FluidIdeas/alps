#!/bin/bash

set -e

. /etc/alps/alps.conf

VERSION=$(grep DISTRIB_RELEASE /etc/lsb-release | cut -d= -f2 | sed 's/"//g')
BASEURL="https://bitbucket.org/chandrakantsingh/aryalinux/get"
TARBALL="$VERSION.tar.bz2"
SCRIPTSDIR="/var/cache/alps/scripts/"

TEMPDIR=$(mktemp -d)
pushd $TEMPDIR &> /dev/null

echo "Fetching scripts..."
wget -q "$BASEURL/$TARBALL" -O $TARBALL
DIRECTORY=$(tar tf $TARBALL | cut -d/ -f1 | uniq)

tar xf $TARBALL
cd $DIRECTORY/applications/
sudo rm -rf $SCRIPTSDIR/*
sudo cp -rf *.sh $SCRIPTSDIR/
sudo chmod a+x $SCRIPTSDIR/*

# Downloading binary scripts

rm -rf master.tar.bz2
echo "Fetching latest binary scripts..."
tmpdir=$(mktemp -d)
pushd $tmpdir &> /dev/null
wget -q https://bitbucket.org/chandrakantsingh/binary-app-installer/get/master.tar.bz2
dir=$(tar tf master.tar.bz2 | cut -d/ -f1 | uniq)
tar -xf master.tar.bz2
cd $dir
sudo cp -prf * /
cd ..
rm -rf $dir
popd &> /dev/null


popd &> /dev/null
sudo rm -r $TEMPDIR

echo "Scripts updated successfully..."

