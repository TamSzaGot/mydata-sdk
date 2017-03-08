# -*- coding: utf-8 -*-

"""
__author__ = "Jani Yli-Kantola"
__copyright__ = ""
__credits__ = ["Harri Hirvonsalo", "Aleksi Palomäki"]
__license__ = "MIT"
__version__ = "1.3.0"
__maintainer__ = "Jani Yli-Kantola"
__contact__ = "https://github.com/HIIT/mydata-stack"
__status__ = "Development"
"""

from app.helpers import get_custom_logger

# create logger
from app.mod_api_auth.services import clear_apikey_sqlite_db
from app.mod_blackbox.services import clear_blackbox_sqlite_db
from app.mod_database.helpers import drop_table_content

logger = get_custom_logger(__name__)


def clear_mysql_db():
    # Clear MySQL tables
    logger.info("Clearing MySQL Database")
    try:
        drop_table_content()
    except Exception as exp:
        logger.error("Could not clear MySQL Database: " + repr(exp))
        raise
    else:
        logger.info("MySQL Database cleared")
        return True


def clear_blackbox_db():
    logger.info("Clearing Blackbox Database")
    try:
        clear_blackbox_sqlite_db()
    except Exception as exp:
        logger.error("Could not clear Blackbox Database: " + repr(exp))
        raise
    else:
        logger.info("Blackbox Database cleared")
        return True


def clear_api_key_db():
    # Clear ApiKey Database
    logger.info("##########")
    logger.info("Clearing ApiKey Database")
    try:
        clear_apikey_sqlite_db()
    except Exception as exp:
        logger.error("Could not clear ApiKey Database: " + repr(exp))
        raise
    else:
        logger.info("ApiKey Database cleared")
        return True

