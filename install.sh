#!/bin/bash

#username
user="user"

lpath="/home/$user/.local/share/gedit/plugins"
path_ua="/usr/share/locale/uk/LC_MESSAGES/mencode.mo"
path_ru="/usr/share/locale/ru/LC_MESSAGES/mencode.mo"


if [[ $EUID -ne 0 ]]; then
 echo "You must be a root user" 2>&1
 exit 1
else

 grep "^$user:" /etc/passwd >/dev/null
 if [ $? -ne 0 ]; then
  echo "Not found user $user "
  exit 1
 else
  #install mencode
  mkdir -p $lpath
  cp mencode.plugin mencode.py $lpath
  chown -R $user:$user $lpath

  # install locale
  cp mencode.mo_ru $path_ru
  cp mencode.mo_ua $path_ua
  chown root:root $path_ua
  chown root:root $path_ru
 fi

fi





