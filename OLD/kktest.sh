#!/bin/sh
. $PWD/bash.conf
echo $MOUNTDIR
#MOUNTDIR=/mnt/almacenNTFS
set KK = $MOUNTDIR
echo $KK
echo $MOUNTDIR
cat /proc/mounts | grep -o mnt

#if echo $MOUNTDIR | grep -qs /proc/mounts; then
#    echo "$MOUNTDIR montado"
#else
#    umount -a
#    mount -a
#fi
