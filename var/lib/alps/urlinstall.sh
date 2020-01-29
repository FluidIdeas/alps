#!/bin/bash

set +h

. /etc/alps/alps.conf

URL="$1"
TARBALL=$(echo $URL | rev | cut -d/ -f1 | rev)

cd $SOURCE_DIR

wget -c $URL -O $TARBALL
if echo $TARBALL | grep "zip$" &> /dev/null; then
	DIR_COUNT=$(unzip -l website.zip | tr -s ' ' | head --lines=-2 | tail --lines=+4 | rev | cut -d ' ' -f1 | rev | cut -d/ -f1 | uniq | wc -l)
	if [ $DIR_COUNT -eq 1 ]; then
		DIRECTORY=$(unzip -l website.zip | tr -s ' ' | head --lines=-2 | tail --lines=+4 | rev | cut -d ' ' -f1 | rev | cut -d/ -f1 | uniq)
		unzip $TARBALL
	else
		DIRECTORY=$(mktemp --tmpdir=$(pwd))
		unzip $TARBALL -d $DIRECTORY
	fi
	pushd $DIRECTORY
elif echo $TARBALL | grep ".tar.gz" &> /dev/null || echo $TARBALL | grep ".tar.bz2" &> /dev/null || echo $TARBALL | grep ".tar.xz" &> /dev/null || echo $TARBALL | grep ".tgz" &> /dev/null || echo $TARBALL | grep ".tar" &> /dev/null; then
	DIR_COUNT=$(tar tf $TARBALL | cut -d/ -f1 | uniq | wc -l)
	if [ $DIR_COUNT -eq 1 ]; then
		DIRECTORY=$(tar tf $TARBALL | cut -d/ -f1 | uniq)
		tar xf $TARBALL
	else
		DIRECTORY=$(mktemp --tmpdir=$(pwd))
		tar $TARBALL -C $DIRECTORY
	fi
fi

pushd $DIRECTORY

if [ -f "./autogen.sh" ]; then
	CONF_SYSTEM="autogen"
elif [ -f "./configure" ]; then
	CONF_SYSTEM="configure"
elif [ -f "./CMakeLists.txt" ]; then
	CONF_SYSTEM="cmake"
elif [ -f "Makefile" ]; then
	CONF_SYSTEM="makefile"
elif [ -f "meson.build" ]; then
	CONF_SYSTEM="meson"
else
	echo "Could not figure out a way to build and install from this source automatically. Exiting..."
	exit
fi

FAILED="yes"

if [ "$CONF_SYSTEM" == "autogen" ]; then
	./autogen.sh --prefix=/usr &&
	./configure --prefix=/usr &&
	make -j$(nproc) &&
	sudo make install
	FAILED="no"
elif [ "$CONF_SYSTEM" == "configure" ]; then
	./configure --prefix=/usr &&
	make -j$(nproc) &&
	sudo make install
	FAILED="no"
elif [ "$CONF_SYSTEM" == "cmake" ]; then
	mkdir build
	cd build
	cmake -DCMAKE_INSTALL_PREFIX=/usr .. &&
	make -j$(nproc) &&
	sudo make install
	FAILED="no"
elif [ "$CONF_SYSTEM" == "meson" ]; then
	mkdir build
	cd build
	meson --prefix=/usr &&
	ninja &&
	sudo ninja install
	FAILED="no"
elif [ "$CONF_SYSTEM" == "makefile" ]; then
	sed -i "s@/usr/local@/usr@g" Makefile
	make -j$(nproc) &&
	sudo make install
	FAILED="no"
fi

popd

if [ "$FAILED" == "no" ]; then
	echo "Source downloaded and installed successfully."
	rm -rf $DIRECTORY
else
	echo "Source could not be installed successfully."
fi
