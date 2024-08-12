# Written by https://github.com/worldbeater

def matches(text, re):
    match re:
        case ('seq', *parsers):
            for parser in parsers:
                if (text := matches(text, parser)) is None:
                    return None
            return text
        case ('range', ('atom', l), ('atom', r)):
            if ord(l) <= ord(text[0]) <= ord(r):
                return text[1:]
        case ('alt', *parsers):
            for parser in parsers:
                if (state := matches(text, parser)) is not None:
                    return state
        case ('repeat', parser, times):
            for _ in range(times):
                if (text := matches(text, parser)) is None:
                    return None
            return text
        case ('+', parser):
            # Desugaring.
            return matches(matches(text, parser), ('*', parser))
        case ('*', parser):
            while text:
                if (state := matches(text, parser)) is None:
                    break
                text = state
            return text
        case ('atom', value):
            if text and text[0] == value:
                return text[1:]
