from deep_translator import GoogleTranslator
from utils import filex
from utils.cache import cache

WORDLIST_FILE = 'src/parliament_lk/i18n/word_list.txt'
TARGET_LANG = 'tamil'

translator = GoogleTranslator(source='english', target=TARGET_LANG)


@cache("build_dictionary-" + TARGET_LANG, 86400 * 90)
def translate(word):
    return translator.translate(word)


def main():
    word_list = sorted(list(filter(
        lambda x: x,
        filex.read(WORDLIST_FILE).split('\n'),
    )))

    for word in word_list:
        word_target = translate(word)
        print(f"'{word}': '{word_target}',")


if __name__ == '__main__':
    main()
