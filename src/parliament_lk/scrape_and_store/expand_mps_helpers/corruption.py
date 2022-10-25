YEAR_2017_18 = '2017/18'
YEAR_2018_19 = '2018/19'
YEAR_2019_20 = '2019/20'
YEAR_2020_21 = '2020/21'
YEAR_2021_22 = '2021/22'


def parse_asset_declaration_years(name):
    # Source: https://www.tisrilanka.org/mpassets/

    return '; '.join(
        {
            'Tharaka Balasuriya': [YEAR_2017_18, YEAR_2018_19],
            'Harsha de Silva': [YEAR_2018_19],
            'Wimalaweera Dissanayake': [YEAR_2018_19],
            'Vidura Wickramanayaka': [YEAR_2017_18, YEAR_2018_19],
            'M. A. Sumanthiran': [YEAR_2017_18, YEAR_2018_19],
            'Vasudeva Nanayakkara': [YEAR_2017_18, YEAR_2018_19],
            'Dayasiri Jayasekara': [YEAR_2018_19, YEAR_2019_20, YEAR_2020_21],
            'Eran Wickramaratne': [YEAR_2017_18, YEAR_2018_19],
            'Madhura Withanage': [YEAR_2021_22],
            'Sivagnanam Shritharan': [YEAR_2021_22],
        }.get(name, [])
    )
