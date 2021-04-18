chown -R root:www-data /home/goals-api.danielmoessner.de
chmod -R 750 /home/goals-api.danielmoessner.de
find /home/goals-api.danielmoessner.de -type f -print0|xargs -0 chmod 740
chmod -R 770 /home/goals-api.danielmoessner.de/tmp/media
find /home/goals-api.danielmoessner.de/tmp/media -type f -print0|xargs -0 chmod 760
chmod 770 /home/goals-api.danielmoessner.de/tmp/logs
chmod -R 760 /home/goals-api.danielmoessner.de/tmp/logs/*
chmod 770 /home/goals-api.danielmoessner.de/tmp
chmod -R 760 /home/goals-api.danielmoessner.de/tmp/db.sqlite3
