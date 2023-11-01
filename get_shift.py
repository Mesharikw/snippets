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
            self.time = time
            self.date = datetime.datetime(self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute).date()
            if int(self.time.strftime('%H')) <= 5:
                self.date -= datetime.timedelta(days=1)

    def get_shift_index(self, date):
        days_since_epoch = (date - self.EPOCH_DATE).days
        return int((days_since_epoch / 4 - int(days_since_epoch / 4)) * 100)

    def get_shift(self, shift_type):
        index = self.get_shift_index(self.date)
        shift_position = self.shift_schedule[shift_type].index(index)
        return self.shift_names[shift_position]

    def get_shifts(self):
        return {shift_type: self.get_shift(shift_type, self.date) for shift_type in self.shift_schedule}
    
    def current_shift(self, date=None, time=None):
        self.date = datetime.datetime.today().date() if date is None else date
        self.time = datetime.datetime.now().time() if time is None else time
        current = 'night'  if (self.time.strftime('%p') == 'AM'and int(self.time.strftime('%H')) <= 5) or (self.time.strftime('%p') == 'PM' and int(self.time.strftime('%H')) >= 18)  else 'day'
        if int(self.time.strftime('%H')) <= 5:
            self.date -= datetime.timedelta(days=1)
        return self.get_shift(current)
        
        
