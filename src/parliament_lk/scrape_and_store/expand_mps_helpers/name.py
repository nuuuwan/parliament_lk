import re


def parse_name_cleaned(name):
    for k in [
        "Hon.",
        ", M.P.",
        "(Dr.)",
        "(Mrs.)",
        "(Major)",
        "Field Marshal",
        "(Ms.)",
        ", PC",
        "Thero",
        "(Ven.) ",
        "(Prof.)",
        ', Attorney at Law',
        ',',
    ]:
        name = name.replace(k, ' ')
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def parse_gender(name):
    for k in ['Mrs.', 'Miss', 'Ms.']:
        if k in name:
            return 'Female'
    return 'Male'


def parse_first_and_last_names(name_cleaned):
    names = name_cleaned.split(' ')
    n_last_name_words = 1
    if names[-2].lower() in ['ali', 'de', 'bakeer']:
        n_last_name_words = 2

    return (
        ' '.join(names[:-n_last_name_words]),
        ' '.join(names[-n_last_name_words:]).title(),
    )
