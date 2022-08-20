import dj_database_url

DATABASES = dict()

# Primary database
db_config = dj_database_url.config()
db_config['DISABLE_SERVER_SIDE_CURSORS'] = True
db_config['CONN_MAX_AGE'] = None
DATABASES['default'] = db_config
