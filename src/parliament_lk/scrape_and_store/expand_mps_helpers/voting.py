def parse_vote_20th_amendment(party_short, name):
    if name in [
        'Faizal Cassim',
        'Diana Gamage',
        'A. Aravindh Kumar',
        'Ali Sabri Raheem',
        'M. S. Thowfeek',
        'Naseer Ahamed',
        'H. M. M. Harees',
        'Ishak Rahuman',
    ]:
        return 'Voted: In Favour'

    if name in [
        'Basil Rohana Rajapaksa',
        'Ranil Wickremesinghe',
        'Ajith Mannapperuma',
        'Athuraliye Rathana',
    ]:
        return 'Did Not Vote: Not MP'

    if name in [
        'Mahinda Yapa Abeywardana',
    ]:
        return 'Did Not Vote: Speaker'

    if name in [
        'Maithreepala Sirisena',
    ]:
        return 'Did Not Vote: Absent'

    if party_short in ['SLPP', 'EPDP', 'OPPP', 'SLFP', 'NC', 'TMVP']:
        return 'Voted: In Favour'

    if party_short in [
        'SJB',
        'UNP',
        'JJB',
        'AITC',
        'ITAK',
        'ACMC',
        'TMTK',
        'TMVP',
        'SLMC',
        'MNA',
    ]:
        return 'Voted Against'

    return 'Unknown'
