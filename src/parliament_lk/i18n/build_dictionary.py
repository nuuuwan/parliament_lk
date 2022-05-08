import os
from deep_translator import GoogleTranslator
from utils import filex
from utils.cache import cache

WORDLIST_FILE = 'src/parliament_lk/i18n/word_list.txt'
SOURCE_LANG = 'english'
TARGET_LANG = 'tamil'

translator = GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG)


@cache("build_dictionary-" + TARGET_LANG, 86400 * 90)
def translate(word):
    return translator.translate(word)


def main():
    word_list = sorted(list(filter(
        lambda x: x,
        filex.read(WORDLIST_FILE).split('\n'),
    )))

    var_name = f'{TARGET_LANG}_DICTIONARY'.upper()
    log_lines = [f'const {var_name} = ' + '{']
    for word_source in word_list:
        word_target = translate(word_source)
        print(word_source, '->', word_target)
        log_lines.append(f"    '{word_source}': '{word_target}',")
    log_lines.append('};')
    log_lines.append(f'export default {var_name};')

    log_file = f'/tmp/{TARGET_LANG}.txt'
    filex.write(log_file, '\n'.join(log_lines))
    print(f'Wrote to {log_file}')
    os.system(f'open -a atom {log_file}')


if __name__ == '__main__':
    main()
