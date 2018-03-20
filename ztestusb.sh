#!/bin/sh
if grep -qs 'mnt/almacenNTFS' /proc/mounts; then
   : 	
   #echo [`date`] " mnt/almacenNTFS montado"
else
    echo [$(date)] " ERROR: mnt/almacenNTFS nomontado"
    umount -a
    mount -a
fi
