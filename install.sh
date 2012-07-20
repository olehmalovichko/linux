#install mencode
mkdir -p  ~/.local/share/gedit/plugins
cp mencode.plugin mencode.py ~/.local/share/gedit/plugins

# install locale
su
cp mencode.mo_ru /usr/share/locale/ru/LC_MESSAGES/mencode.mo
cp mencode.mo_ua /usr/share/locale/ua/LC_MESSAGES/mencode.mo





