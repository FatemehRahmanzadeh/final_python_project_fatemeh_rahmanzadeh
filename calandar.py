from datetime import datetime
import calendar
import user
import work
from tabulate import tabulate

my_calendar = calendar.Calendar(6)


def show_day_works(usr, day):
    """
    this function is going to show works of user within a day
    :param usr: current user
    :param day: target day
    :return: a dictionary of works of this day
    """

    day_works = {'finished': [], 'in progress': []}
    for wrk in usr.works:
        if wrk.wrk_datetime.date() == datetime.strptime(day, '%Y-%m-%d'):
            if wrk.status == 'done':
                day_works['finished'].append(wrk.work_name)
            else:
                day_works['in progress'].append(wrk.work_name)

    print(tabulate(day_works, day_works.keys(), tablefmt="presto"))
    return {day: day_works}


def show_week_works(usr, target_date, week):
    """
    this function is going to show works of user within a week
    :param usr: current user
    :param target_date: date to take part week
    :param week: number of week of month
    :return: a dictionary of works of this wek
    """
    week_works = {'finished': [], 'in progress': []}
    for wrk in usr.works:
        if wrk.work_datetime.month() == target_date.month() and target_date.isocalendar()[1] == week:
            if wrk.status == 'done':
                week_works['finished'].append(wrk.work_name)
            else:
                week_works['in progress'].append(wrk.work_name)
    return {week: week_works}


def show_month_works(usr, target_date):
    """
    this function is going to show works of user within a month
    :param usr: current user
    :param target_date: date to take part month
    :return: a dictionary of works of this wek
    """
    month_works = {'finished': [], 'in progress': []}
    for wrk in usr.works:
        if wrk.work_datetime.month() == target_date.month():
            if wrk.status == 'done':
                month_works['finished'].append(wrk.work_name)
            else:
                month_works['in progress'].append(wrk.work_name)
    return {'month': month_works}


def show_calandar():
    return None
