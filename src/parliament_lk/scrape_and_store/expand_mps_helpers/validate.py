import json
import random


def validate(expanded_mp_list):
    n = len(expanded_mp_list)
    random.randint(0, n - 1)
    for mp in expanded_mp_list:
        if 'Tharaka' in mp['name_cleaned']:
            print(json.dumps(mp, indent=2))
    return

    subset_list = sorted(list(map(
        lambda mp: [
            mp['vote_20th_amendment'],
            mp['party_short'],
            mp['name_cleaned'],
        ],
        expanded_mp_list,
    )), key=lambda x: str(x[0]))

    x0_to_list = {}
    for x in subset_list:
        x0 = str(x[0])
        if x0 not in x0_to_list:
            x0_to_list[x0] = []
        x0_to_list[x0].append(tuple(x[1:]))

    for x0, x_rem_list in sorted(x0_to_list.items(), key=lambda x: x[0]):
        print('-' * 32)
        print(x0, len(x_rem_list))
        for x_rem in sorted(list(set(x_rem_list))):
            print('\t', x_rem)
