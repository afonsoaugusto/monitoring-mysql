import mysql.connector
from mysql.connector import Error

from prometheus_client import start_http_server, Summary
from prometheus_client import Counter
import random
import time
import os
import sys

import logging
logger = logging.getLogger()
# set logging level from environment variable or default to INFO
logger.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))

failures = Counter('monitor_failures', 'Counter of failures')
exceptions = Counter('monitor_exceptions', 'Counter of exceptions')


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('monitor_request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(failures: Counter,exceptions: Counter, logger : logging.Logger):
    try:
        # get connection variable from environment variable
        connection = mysql.connector.connect(host=os.environ.get('DB_HOST', 'localhost'),
                                              database=os.environ.get('DB_NAME', 'monitoring'),
                                              user=os.environ.get('DB_USER', 'root'),
                                              password=os.environ.get('DB_PASSWORD', 'root'),
                                              use_pure=True,
                                              connect_timeout=5000)

        if connection.is_connected():
            db_Info = connection.get_server_info()
            logger.info("Connected to MySQL Server version " + str(db_Info))
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            logger.info("You're connected to database: " + str(record))

    except Error as e:
        failures.inc()
        logging.error('Error while connecting to MySQL ' + e.__class__.__name__)
    except Exception as e:
        exceptions.inc()
        logging.error('Exception while connecting to MySQL ' + e.__class__.__name__)
    finally:
        try:
            if connection.is_connected():
                cursor.close()
                connection.close()
                logger.info("MySQL connection is closed")
        except Exception as e:
            exceptions.inc()
            logging.error('Exception MySQL not connected ' + e.__class__.__name__)

if __name__ == '__main__':
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    format_handler = logging.StreamHandler(sys.stdout)
    format_handler.setFormatter(formatter)
    logging.getLogger().addHandler(format_handler)
    # Start up the server to expose the metrics.
    start_http_server(8000)
    
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    
    # Generate some requests.
    
    while True:
        process_request(failures, exceptions, logger)
        time.sleep(1)
