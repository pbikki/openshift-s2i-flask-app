import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))


logging.basicConfig()
LOGGER = logging.getLogger(__name__)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'

    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        # the order of these is significant, do not rearrange!
        url_env_names = ['POSTGRES_USER', 'POSTGRES_PW', 'POSTGRES_HOST',
                         'POSTGRES_PORT', 'POSTGRES_DB']
        url_envs = [os.getenv(part) for part in url_env_names]
        if any([env is None for env in url_envs]):
            LOGGER.warning(
                'Unable to form SQLALCHEMY_DATABASE_URI. Please set '
                'DATABASE_URL or {}.'.format(', '.join(url_env_names)))
        else:
            SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}:{}/{}'.format(*url_envs)
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
