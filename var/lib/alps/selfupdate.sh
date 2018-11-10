#!/bin/bash

set -e

URL="https://bitbucket.org/chandrakantsingh/alps-new/get/master.tar.bz2"
TARBALL="master.tar.bz2"

TEMPDIR=$(mktemp -d)
cd $TEMPDIR

echo "Fetching and updating alps..."

wget -q $URL
DIRECTORY=$(tar tf $TARBALL | cut -d/ -f1 | uniq)

tar xf $TARBALL
pushd $DIRECTORY &> /dev/null
rm etc/alps/{installed-list,versions}
sudo cp -rf * /
sudo chmod a+x /var/lib/alps/*.sh
sudo chmod a+x /usr/bin/alps

popd &> /dev/null

sudo rm -r $TEMPDIR

echo "alps updated successfully..."

