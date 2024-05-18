"""Set the configs for relt as a python dict."""

import logging
import sys

logging_config = {'level': logging.INFO,
                  'stream_handler': sys.stdout,
                  'format': "%(asctime)s | %(levelname)s]: %(message)s"
                  }
