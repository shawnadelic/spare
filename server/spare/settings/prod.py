from .base import *  # noqa
import dj_database_url

DEBUG = False

# Recommended settings (Heroku takes care of this for us)
ALLOWED_HOSTS = ['*']

# Set database URL
db = dj_database_url.config(default=os.environ['DATABASE_URL'], conn_max_age=600)
db['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db
}

MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE
