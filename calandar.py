from datetime import datetime
from colorama import Fore
from tabulate import tabulate


def show_day_works(usr, target_date):
    """
    this function is going to show works of user within a day
    :param usr: current user
    :param target_date: target day
    :return: a dictionary of works of this day
    """
    try:
        day_works = {'finished': [], 'in progress': []}
        for wrk in usr.works:
            if wrk.work_datetime.date() == target_date.date():
                if wrk.status == 'done':
                    day_works['finished'].append(wrk.work_name)
                else:
                    day_works['in progress'].append(wrk.work_name)

        assert day_works

    except AssertionError:
        print(f'{Fore.CYAN}no work found for you this day{Fore.RESET}')
        return 0
    return tabulate(day_works, day_works.keys(), tablefmt="presto")


def show_week_works(usr, target_date):
    """
    this function is going to show works of user within a week
    :param usr: current user
    :param target_date: date to take part week
    :return: a dictionary of works of this wek
    """
    week = target_date.isocalendar()[1]
    week_works = {'finished': [], 'in progress': []}
    try:
        for wrk in usr.works:
            if wrk.work_datetime.isocalendar()[1] == week:
                if wrk.status == 'done':
                    week_works['finished'].append(f"{wrk.work_name}:\n{wrk.work_datetime.date()}")
                else:
                    week_works['in progress'].append(f"{wrk.work_name}:\n{wrk.work_datetime.date()}")
        assert week_works

    except AssertionError:
        print(f'{Fore.CYAN}no work found for you this week{Fore.RESET}')
        return 0
    return tabulate(week_works, week_works.keys(), tablefmt="presto")


def show_month_works(usr, target_date):
    """
    this function is going to show works of user within a month
    :param usr: current user
    :param target_date: date to take part month
    :return: a dictionary of works of this wek
    """
    month = target_date.month
    try:
        month_works = {'finished': [], 'in progress': []}
        for wrk in usr.works:
            if wrk.work_datetime.month == month:
                if wrk.status == 'done':
                    month_works['finished'].append(f"{wrk.work_name}:\n{wrk.work_datetime.date()}")
                else:
                    month_works['in progress'].append(f"{wrk.work_name}:\n{wrk.work_datetime.date()}")
        assert month_works

    except AssertionError:
        print(f'{Fore.CYAN}no work found for you this month{Fore.RESET}')
        return 0
    return tabulate(month_works, month_works.keys(), tablefmt="presto")

# t2 = datetime.strptime('2021-05-1 08:12:00', "%Y-%m-%d %H:%M:%S")
# print(t2.month)
# print(t2.isocalendar()[0])
