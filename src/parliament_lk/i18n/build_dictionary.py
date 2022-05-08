import os

from deep_translator import GoogleTranslator
from utils import filex, timex
from utils.cache import cache

DIR_JS_BASE = os.path.join(
    '/Users/nuwan.senaratna/Not.Dropbox',
    '_CODING/js_react',
    'parliament_lk_app',
    'src/base',
)

WORDLIST_FILE = os.path.join(
    DIR_JS_BASE,
    'WORD_LIST.txt',
)
SOURCE_LANG = 'english'
TARGET_LANGS = ['sinhala', 'tamil']


HARD_CODED_CHANGES = {
    'A. Level': 'Advanced Level',
    'ISCED7 Masters': 'ISCED7 Masters Degree',
    'Vote for 20th Amendment': 'Voting for 20th Amendment',
    'Voted: In Favour': 'Voted In Favour',
    'App & Visualization by': 'App & Visualization',
    'Data from': 'Data',
}


def build_dictionary():
    word_list = sorted(list(set(filter(
        lambda x: x,
        filex.read(WORDLIST_FILE).split('\n'),
    ))))

    filex.write(WORDLIST_FILE, '\n'.join(word_list))

    for target_lang in TARGET_LANGS:
        translator = GoogleTranslator(source=SOURCE_LANG, target=target_lang)

        CACHE_NAME = "build_dictionary-" + target_lang
        CACHE_TIMEOUT = timex.SECONDS_IN.YEAR

        @cache(CACHE_NAME, CACHE_TIMEOUT)
        def translate(word):
            return translator.translate(word)

        var_name = f'{target_lang}_DICTIONARY'.upper()
        time_id = timex.get_time_id()
        log_lines = [
            f'// Auto Translated {time_id}',
            f'const {var_name} = ' + '{',
        ]
        for word_source in word_list:
            word_source_use = word_source
            for k, v in HARD_CODED_CHANGES.items():
                if k in word_source:
                    word_source_use = word_source.replace(k, v)
                    print(f'\tReplaced {k} with {v} -> {word_source_use}')

            word_target = translate(word_source_use)
            print(word_source, '->', word_target)
            if ' ' in word_source or '-' in word_source:
                word_source_str = f'"{word_source}"'
            else:
                word_source_str = word_source

            log_lines.append(f'  {word_source_str}: "{word_target}",')
        log_lines.append('};')
        log_lines.append(f'export default {var_name};')

        log_file = os.path.join(
            DIR_JS_BASE,
            f'{target_lang}_DICTIONARY.js',
        )
        filex.write(log_file, '\n'.join(log_lines))
        print(f'Wrote to {log_file}')
