import datetime

import work
# s = {'sender':{"work_name": "work out",
#             "work_datetime": "2021-05-19 12:00:00",
#             "category": "sport",
#             "importance": 'true',
#             "urgency": 'true',
#             "location": "gym",
#             "link": "gym.ir",
#             "description": "1hour per day",
#             "status": 'null',
#             "notification": 'null'}, 'sender2':{
#             "work_name": "study english",
#             "work_datetime": "2021-05-12 12:30:00",
#             "category": "education",
#             "importance": 'true',
#             "urgency": 'false',
#             "location": "",
#             "link": "",
#             "description": ""
#         }}
# work_select = {}
# s2={i: sender for i, sender in enumerate(s.items())}
# for i, w in s2.items():
#     work_select[i] = (w[0],(work.Work(*(w[1].values()))))
# print(work_select)
#
# wok = []
# while work_select:
#     for i, event in work_select.items():
#         print(f'{i+1}. {event[0]}: {event[1].work_name}')
#     select = int(input('choose a work:'))
#     selected_itm = work_select.pop(select-1)
#     act = int(input('1. accept 2. reject:'))
#     if act == 1:
#         wok.append(selected_itm[1])
#     elif act == 2:
#         continue
#     print(work_select)
# print(work_select)

d = datetime.datetime(2021, 12, 2, 12,20, 0)
w = work.Work('test', '2021-02-01 22:00:00', 'tst', True, False)
# print(type(w.work_datetime))
# w.postpone(1, "hour")
# print(w.postpone(1, "hour"))
# print(d + datetime.timedelta(seconds=1*3600))
# print(w.work_datetime + datetime.timedelta(seconds=1*3600))
s="d"
def switch(s):
    if s=='d':
        s='f'
        return s
    elif s== 'f':
        s='d'
        return s
    else:
        return 'error'

s='f'
new=switch(s)
print(new)
