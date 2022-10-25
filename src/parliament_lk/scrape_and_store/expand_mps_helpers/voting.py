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


def parse_vote_22nd_amendment(party_short, name):
    print(name)

    if name == 'Sarath Weerasekera':
        return 'Voted Against'

    if name in [
        'Rajavarothiam Sampanthan',
        'Abdul Haleem',
        'Vadivel Suresh',
        'S. Noharathalingam',
        'G. G. Ponnambalam',
        'Selvarajah Kajendren',
        'Hector Appuhamy',
        'Velu Kumar',
        'S. M. Marikkar',
        'Hesha Withanage',
        'M. A. Sumanthiran',
        'Shanakiyan Rajaputhiran Rasamanickam',
        'Thavaraja Kalai Arasan',
    ]:
        return 'Did Not Vote: Absent'

    if name in [
        'G. L. Peiris',
        'Upul Galappaththi',
        'Angajan Ramanathan',
        'Shan Vijayalal De Silva',
        'Tissa Vitarana',
    ]:
        return 'Did Not Vote: Absent'

    if name in [
        'Mahinda Rajapaksa',
        'Prasanna Ranatunga',
        'Mahinda Amaraweera',
        'Premitha Bandara Tennakoon',
        'Sanath Nishantha',
        'Siripala Gamalath',
        'Anuradha Jayaratne',
        'Seetha Arambepola',
        'Johnston Fernando',
        'Pavithradevi Wanniarachchi',
        'Gamini Lokuge',
        'Janaka Bandara Thennakoon',
        'S. M. Chandrasena',
        'Rohitha Abegunawardhana',
        'Wimalaweera Dissanayake',
        'Dhammika Perera',
        'S. M. M. Muszhaaraff',
        'Jayantha Ketagoda',
        'Major Pradeep Undugoda',
        'Sanjeeva Edirimanna',
        'Nalaka Bandara Kottegoda',
        'Nipuna Ranawaka',
        'M. W. D. Sahan Pradeep Withana',
        'Sagara Kariyawasam',
        'Ranjith Bandara',
        'Jayantha Weerasinghe',
    ]:
        return 'Did Not Vote: Absent'

    if name in [
        'Douglas Devananda',
        'Mahindananda Aluthgamage',
        'A. Aravindh Kumar',
        'Ajith Rajapakse',
        'Akila Ellawala',
        'Anupa Pasqual',
        'Arundika Fernando',
        'Ashoka Priyantha',
        'C. B. Rathnayake',
        'Chamal Rajapaksa',
        'Chamara Sampath Dasanayake',
        'D. B. Herath',
        'Diana Gamage',
        'Dilum Amunugama',
        'Dinesh Gunawardena',
        'Bandula Gunawardana',
        'D. V. Chanaka',
        'Geetha Samanmale Kumarasinghe',
        'Indika Anuruddha Herath',
        'Mayadunna Chinthaka Amal',
        'Piyal Nishantha De Silva',
        'Shasheendra Rajapaksa',
        'Gayashan Nawananda',
        'Gunathilaka Rajapaksha',
        'Harin Fernando',
        'H. Nandasena',
        'Isuru Dodangoda',
        'Jagath Kumara Sumithraarachchi',
        'Jagath Pushpakumara',
        'Janaka Wakkumbura',
        'Kanaka Herath',
        'Kanchana Wijesekera',
        'Kapila Athukorala',
        'Karunadasa Kodithuwakku',
        'Udayakantha Gunathilaka',
        'K. Kader Masthan',
        'Kokila Gunawardene',
        'Kulasingam Dhileeban',
        'Kumarasiri Rathnayaka',
        'Lohan Ratwatte',
        'Manusha Nanayakkara',
        'Milan Jayathilake',
        'Mohan Priyadarshana De Silva',
        'Muditha Prishanthi',
        'M .U. M. Ali Sabry',
        'Nalin Fernando',
        'Namal Rajapaksa',
        'Naseer Ahamed',
        'Nimal Siripala de Silva',
        'Rohana Dissanayaka',
        'Prasanna Ranaweera',
        'Premalal Jayasekara',
        'Premnath C. Dolawatte',
        'Rajika Wickramasinghe',
        'Ramesh Pathirana',
        'Roshan Ranasinghe',
        'Sampath Athukorala',
        'Sarath Weerasekera',
        'S. B. Dissanayake',
        'Shehan Semasinghe',
        'Sisira Jayakody',
        'Sivanesathurai Santhirakanthan',
        'Sudarshana Denipitiya',
        'Sudath Manjula',
        'Suren Raghavan',
        'Susil Premajayantha',
        'S. Viyalanderan',
        'Tharaka Balasuriya',
        'Thenuka Vidanagamage',
        'Lasantha Alagiyawanna',
        'Thisakutti Arachchi',
        'U. K. Sumith Udukumbura',
        'Tiran Alles',
        'Upul Mahendra Rajapaksha',
        'Wajira Abeywardana',
        'Vidura Wickramanayaka',
        'Vijitha Berugoda',
        'Wijeyadasa Rajapakshe',
    ]:
        return 'Voted: In Favour'

    if party_short in ['SJB', 'JJB']:
        return 'Voted: In Favour'

    return 'Voted: In Favour'
