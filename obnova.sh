#!/bin/bash

case "$1" in

-1)
dpkg --get-selections "*" && dpkg -l ;;

-2)
apt update -y && apt upgrade -y && apt dist-upgrade -y && apt --purge autoremove -y

lsb_release -a
cat /etc/debian_version ;;

-3)
echo "deb http://mirror.yandex.ru/debian bullseye main" > /etc/apt/sources.list
echo "deb-src http://mirror.yandex.ru/debian bullseye main\n" >> /etc/apt/sources.list

echo "deb http://mirror.yandex.ru/debian bullseye-updates main" >> /etc/apt/sources.list
echo "deb-src http://mirror.yandex.ru/debian bullseye-updates main\n" >> /etc/apt/sources.list

echo "deb http://security.debian.org/ bullseye-security main" >> /etc/apt/sources.list
echo "deb-src http://security.debian.org/ bullseye-security main" >> /etc/apt/sources.list

apt update -y && apt upgrade -y && apt dist-upgrade ;;

-4)
lsb_release -a
cat /etc/debian_version ;;

esac
