chown -R root:www-data ./
chmod -R 750 ./
find ./ -type f -print0|xargs -0 chmod 740
chmod -R 770 ./tmp/media
find ./tmp/media -type f -print0|xargs -0 chmod 760
chmod 760 ./tmp/django.log
chmod 760 ./tmp/db.sqlite3
chmod 770 ./tmp
