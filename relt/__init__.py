import logging

from relt.configs import logging_config


def get_logger():
    root = logging.getLogger()
    root.setLevel(logging_config['level'])

    handler = logging.StreamHandler(logging_config['stream_handler'])
    handler.setLevel(logging_config['level'])
    formatter = logging.Formatter(logging_config['format'])
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


logger = get_logger()

logger.info('relt logger is init')


def set_log_level(level: str = 'INFO'):
    global logger
    if level.lower() == 'info':
        logging_config['level'] = logging.INFO
    elif level.lower() == 'debug':
        logging_config['level'] = logging.DEBUG
    else:
        pass
    logger = get_logger()
