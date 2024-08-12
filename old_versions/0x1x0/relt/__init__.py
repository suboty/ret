import logging
from typing import Callable

from relt.configs import logging_config


class RELTLogger:
    def __init__(self):
        self.logger = self.__get_logger()
        self.logger.info('RELT logger is init')

    @staticmethod
    def __get_logger():
        root = logging.getLogger()
        root.setLevel(logging_config['level'])

        handler = logging.StreamHandler(logging_config['stream_handler'])
        handler.setLevel(logging_config['level'])
        formatter = logging.Formatter(logging_config['format'])
        handler.setFormatter(formatter)
        root.addHandler(handler)
        return root

    def set_log_level(self, level: str = 'INFO'):
        if level.lower() == 'info':
            logging_config['level'] = logging.INFO
        elif level.lower() == 'debug':
            logging_config['level'] = logging.DEBUG
        else:
            raise NotImplementedError(
                'Error while logging level setting'
            )
        self.logger = self.__get_logger()

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(f'--- {message}')

    def warning(self, message: str):
        self.logger.warning(f'#-# {message}')

    def error(
            self,
            message: str,
            exc: Exception,
            raise_exc: Callable,
            traceback: str = None,
    ):
        if traceback:
            self.logger.error(
                f'### {message}. '
                f'Exception: {exc}. '
                f'Traceback: {traceback}'
            )
        else:
            self.logger.error(
                f'### Error: {message}. '
                f'Exception: {exc}. '
            )
        raise raise_exc(message)


logger = RELTLogger()
