NAME="burgers_app"                                   # Name of the application
DJANGO_DIR=/app                                      # Django project directory
DJANGO_BUILD_DIR=$DJANGO_DIR/build/cloudbuild/django # Django project directory
BIND_ADDRESS=:8000                                   # we will communicate using this unix socket
NUM_WORKERS=3                                        # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=BurgersUnlimited.settings     # which settings file should Django use
DJANGO_WSGI_MODULE=BurgersUnlimited.wsgi             # WSGI module name

echo "Starting $NAME as $(whoami)"

# Activate the virtual environment
cd $DJANGO_DIR || exit
./build/cloudbuild/django/activate.sh
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

python manage.py migrate
python manage.py collectstatic --noinput

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--bind=$BIND_ADDRESS \
--log-level=debug \
--log-file=-
