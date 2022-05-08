def parse_academic_highest_level(
        academic_qualifications,
        professional_qualifications):
    if not academic_qualifications and not professional_qualifications:
        return '0 Unknown'
    s = str(professional_qualifications) + ' ' + str(academic_qualifications)

    LEVEL_TO_KEYWORDS = {
        '8 Doctorate': [
            'Doctor of Public Service',
            'PhD',
            'Ph.D',
            'Doctor of Philosophy',
            'M.D.',
            'Doctarate in Public Administration',
            'PHD',
            ' MD ',
        ],
        '7 Masters': [
            'Msc',
            'MA ',
            'Mphil ',
            'M.Ed',
            'MBA',
            'M.Sc',
            'MSc',
            'M.Com.',
            'M.B.A',
            'LLM',
        ],
        '6 Bachelors': [
            'Postgraduate Degree In Business Management',
            'BSc',
            'MBBS',
            'M.B.B.S.',
            'B.A',
            'Business Management Degree',
            'BSc.',
            'B.Eng',
            'B.com',
            'B.A. ',
            'B.Com.',
            'B. Sc.',
            'BA',
            'B.B.A ',
            'B. Com',
            'B.Sc',
            'LLB',
            'Bachelor',
            'L.L.B.',
            'Attorney',
            'B.Ed',
            'LL. B',
            'Open University Degree',
            'B.B.A',
            'L.LB',
            'Sri Lanka Law College',
            'Electrical and Electronics Engineering',
        ],
        '5 Short-Tertiary': [],
        '4 Post-Secondary': ['Diploma', 'Dip.', 'HCIMA', 'Dip in'],
        '3 Upper Secondary (A. Levels)': [
            'G.C.E Advanced Level',
            'A/L',
            'Advanced level',
            'GCE Advanced Level',
            'Advance level',
            'advanced Level',
            'G.C.E. (Advanced Level)',
        ],
        '2 Lower Secondary (O. Levels)': [
            'O/L',
            'O /L',
            'upto Advanced Level',
            'Secondary Education',
            'Upto Advanced Level',
        ],
        '1 Primary': [''],
    }

    for level, keywords in LEVEL_TO_KEYWORDS.items():
        for k in keywords:
            if k and k in s:
                return level

    return '1 Primary'
