import calendar


class Birthday:

    def __init__(self, user_id, day=-1, month=-1, year=-1):
        self.user_id = user_id
        self.day = day
        self.month = month
        self.year = year

    def printable_date(self):
        if self.day == 1:
            aux = 'st'
        elif self.day == 2:
            aux = 'nd'
        elif self.day == 3:
            aux = 'rd'
        else:
            aux = 'th'
        string = f'{calendar.month_name[int(self.month)]} the {self.day}{aux}'
        return string


