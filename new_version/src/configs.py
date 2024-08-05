import logging
import sys

logging_config = {
    'level': logging.DEBUG,
    'stream_handler': sys.stdout,
    'format': "%(asctime)s | %(levelname)s]: %(message)s"
}
