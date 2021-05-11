from datetime import datetime
import calendar
import user
import work
from tabulate import tabulate

my_calendar = calendar.Calendar(6)


def show_day_works(user, day):
    """
    this function is going to show works of user within a day
    :param user: current user
    :param day: target day
    :return: a dictionary of works of this day
    """

    day_works = {'finished': [], 'in progress': []}
    for work in user.works:
        if work.work_datetime.date() == datetime.strptime(day, '%Y-%m-%d'):
            if work.status == 'done':
                day_works['finished'].append(work.work_name)
            else:
                day_works['in progress'].append(work.work_name)

    print(tabulate(day_works, works.keys(), tablefmt="presto"))
    return {day:day_works}

def show_week_works(user, date, week):
    """
    this function is going to show works of user within a week
    :param user: current user
    :param week: target week
    :return: a dictionary of works of this wek
    """
    week_works = {'finished': [], 'in progress': []}
    for work in user.works:
        if work.work_datetime.month() == date.month() and date.isocalendar()[1] == week:
            if work.status == 'done':
                week_works['finished'].append(work.work_name)
            else:
                week_works['in progress'].append(work.work_name)
    return {week:week_works}

def show_month_works(user, month):
    """
    this function is going to show works of user within a month
    :param user: current user
    :param month: target month
    :return: a dictionary of works of this wek
    """
    month_works = {'finished': [], 'in progress': []}
    for work in user.works:
        if work.work_datetime.month() == date.month():
            if work.status == 'done':
                month_works['finished'].append(work.work_name)
            else:
                month_works['in progress'].append(work.work_name)
    return {week:month_works}
