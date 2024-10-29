from geppy.core.symbol import _is_nonkeyword_identifier


def get_all_unicode_letters(start_code, stop_code):
    start_idx, stop_idx = [int(code, 16) for code in (start_code, stop_code)]
    characters = []
    for unicode_idx in range(start_idx, stop_idx + 1):
        characters.append(chr(unicode_idx))
    return characters


def get_terminals(
        add_digits: bool = True,
        add_lower_latin_letters: bool = True,
        add_custom_symbols: bool = False,
        custom_symbols=None,
):
    if custom_symbols is None:
        custom_symbols = []
    terminals = []

    if add_digits:
        terminals += get_all_unicode_letters('0030', '0039')

    if add_lower_latin_letters:
        terminals += get_all_unicode_letters('0061', '007A')

    if add_custom_symbols:
        terminals += custom_symbols

    # check ability to get __name__ for GEP algorithm
    correct_terminals = []
    for x in terminals:
        try:
            assert _is_nonkeyword_identifier(x)
            correct_terminals.append(x)
        except:
            pass

    return correct_terminals
