import datetime


def get_shfit(date=None, shift=None):

    # date:     date in string
    # shift:    0 - for day shift, 1 - for Night shift, 2 - for 1st off, 3 - for 2nd off

    shifts = {
        'day': {
            0: 'A',
            25: 'B',
            5: 'C',
            75: 'D'
        },
        'night': {
            25: 'A',
            5: 'B',
            75: 'C',
            0: 'D'
        },
        'first_off': {
            5: 'A',
            75: 'B',
            0: 'C',
            25: 'D'
        },
        'second_off': {
            75: 'A',
            0: 'B',
            25: 'C',
            5: 'D'
        }
    }

    today = datetime.datetime.now().date()
    date_beings = datetime.date(1983, 1, 1)
    if not date:
        date = today
    elif type(date) is str:
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    else:
        raise Exception("Date should be string or empty!")
    diff_dates = (date - date_beings).days
    div_dates = diff_dates / 4
    map_date = int((div_dates - int(div_dates)) * 100)
    if shift == 0:
        return shifts['day'].get(map_date)
    elif shift == 1:
        return shifts['night'].get(map_date)
    elif shift == 2:
        return shifts['first_off'].get(map_date)
    elif shift == 3:
        return shifts['second_off'].get(map_date)
    elif not shift:
        return {'day': shifts['day'].get(map_date), 'night': shifts['night'].get(map_date),
                '1st-off': shifts['first_off'].get(map_date), '2nd-off': shifts['second_off'].get(map_date)}

