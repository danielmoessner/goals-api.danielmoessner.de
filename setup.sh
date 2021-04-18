cd /home/
git clone https://github.com/danielmoessner/goals-api.danielmoessner.de.git
cd goals-api.danielmoessner.de
mkdir tmp
mkdir tmp/logs
mkdir tmp/media
mkdir tmp/static
touch tmp/logs/django.log
ln -s /home/goals-api.danielmoessner.de/apache.conf /etc/apache2/sites-available/goals-api.danielmoessner.de.conf
