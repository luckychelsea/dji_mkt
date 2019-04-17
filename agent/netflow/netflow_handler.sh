#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "missing filename"
    exit
fi

PATH=/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin
tmpdir='/tmp/djing_flow'

if [ ! -d "$tmpdir" ]; then
    mkdir -p "$tmpdir"
fi

cd "$tmpdir"
fname=$1
port=`echo $(find -name "$fname") | tr / "\n" | head -2 | tail -n1`

if [[ -z "$port" ]]; then
    echo "$fname not found in any directory"
else
    mkdir -p dump/${port}
    mv ${port}/${fname} dump/${port}/${fname}.dmp
fi
