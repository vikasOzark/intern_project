from django.test import TestCase

# Create your tests here.
from datetime import datetime, timedelta, date, time

date_apt = '2022-08-22'
nowd = date.today()
ti = datetime.strptime(date_apt,'%Y-%m-%d').date()


if ti > nowd:
    print(ti ,' -> ', nowd)
    print('corre')

else:
    print('not')