import datetime
import exceptions


def date_correct(user_date):
    try:
        user_date = user_date.replace('.', '-')
        date_f1 = datetime.datetime.strptime(user_date, "%d-%m-%Y").date()
        today = datetime.date.today()
        if date_f1 < today:
            raise exceptions.DateErrorLast
        return date_f1.strftime("%d-%m-%Y")
    except ValueError:
        try:
            user_date = user_date.replace('.', '-')
            date_f2 = datetime.datetime.strptime(user_date, "%d-%m-%y").date()
            today = datetime.date.today()
            if date_f2 < today:
                raise exceptions.DateErrorLast
            return date_f2.strftime("%d-%m-%Y")
        except ValueError:
            raise exceptions.DateError
