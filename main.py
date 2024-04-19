from lexical_analyzer import re3_tokens as re3_tokenizer


if __name__ == '__main__':

    while True:
        try:
            re_string = input()
            print('Tokens: ', re3_tokenizer.mapper(string=re_string))
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(f'Error while translating: {e}')
