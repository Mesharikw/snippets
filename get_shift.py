import datetime


class ShiftScheduler:
    def __init__(self, date=None, time=None):
        self.EPOCH_DATE = datetime.date(1970, 1, 1)
        self.shift_names = ['a', 'b', 'c', 'd']
        self.shift_schedule = {
            'day': [0, 25, 50, 75],
            'night': [25, 50, 75, 0],
            'first_off': [50, 75, 0, 25],
            'second_off': [75, 0, 25, 50]
        }
        self.date = datetime.datetime.today().date() if date is None else date
        if time is not None:
            self.date = datetime.datetime(self.date.year, self.date.month, self.date.day, time.hour, time.minute).date()

    def get_shift_index(self, date):
        days_since_epoch = (date - self.EPOCH_DATE).days
        return int((days_since_epoch / 4 - int(days_since_epoch / 4)) * 100)

    def get_shift(self, shift_type, date=None):
        date = self.date if date is None else date
        index = self.get_shift_index(date)
        shift_position = self.shift_schedule[shift_type].index(index)
        return self.shift_names[shift_position]

    def get_shifts(self, date=None):
        date = self.date if date is None else date
        return {shift_type: self.get_shift(shift_type, date) for shift_type in self.shift_schedule}
