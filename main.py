from src.translator import Translator
from src.logger import logger

if __name__ == '__main__':

    translator = Translator()

    input_regex = 'abc(d|e)'

    logger.info(translator.translate(string=input_regex, input_syntax='python', output_syntax='python'))
    logger.info(translator.ast)
