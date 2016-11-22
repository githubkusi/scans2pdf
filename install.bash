#!/bin/bash
TAR=/usr/local/bin

echo install scripts to $TAR

for F in scan2pdf
do
    echo ln -s $PWD/$F $TAR

    if [ -e $TAR/$F ]
    then
        sudo rm $TAR/$F
    fi
    sudo ln -s $PWD/$F $TAR
done

