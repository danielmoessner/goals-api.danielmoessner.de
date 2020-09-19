chown -R root:www-data /home/mastergoal_project
chmod -R 750 /home/mastergoal_project
find /home/mastergoal_project -type f -print0|xargs -0 chmod 740
chmod -R 770 /home/mastergoal_project/tmp/media
find /home/mastergoal_project/tmp/media -type f -print0|xargs -0 chmod 760
chmod 770 /home/mastergoal_project/tmp/logs
chmod -R 760 /home/mastergoal_project/tmp/logs/*
chmod 770 /home/mastergoal_project/tmp
chmod -R 760 /home/mastergoal_project/tmp/db.sqlite3
