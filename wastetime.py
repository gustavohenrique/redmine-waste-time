# coding: utf-8
from redmine import Redmine
from datetime import timedelta

import sys


TRACKERS = {
    'DEPLOY_PROD': 4
}

USERS = {
    'DEVOPS': 159
}

# month as key and days as value
HOLLYDAYS_2015 = {
    9: [7],
    10: [12],
    11: [2, 20]
}


def get_issues(created_on, closed_on):
    redmine = Redmine('http://rednm.globosat.net.br/', key='put the key here')
    p = redmine.project.get('bck-infra')
    issues = redmine.issue.filter(
        project_id=p.id,
        created_on='><%s|%s' % (created_on, closed_on),
        limit=1000,
        status_id='closed',
        tracker_id=TRACKERS['DEPLOY_PROD'],
        assigned_to_id=USERS['DEVOPS']
    )
    return issues


def is_hollyday_or_weekend(date, days):
    next_date = date + timedelta(days=days)
    is_hollyday = next_date.day in HOLLYDAYS_2015[next_date.month]
    is_weekend = next_date.weekday() in [5, 6]
    return is_hollyday or is_weekend


def get_waste_time_in_minutes(created_on, closed_on):
    diff = closed_on - created_on
    continuos = diff.total_seconds() / 60

    working = 0
    days = diff.days
    if days > 0:
        days += 1

    for i in range(1, days):
        if is_hollyday_or_weekend(date=created_on, days=i):
            # Subtract 24h in minutes
            continuos -= 1440
        else:
            # Sum 8h in minutes
            working += 480

    return {
        'continuos': int(continuos),
        'working': working
    }


if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print 'Run as: python %s 2015-11-01 2015-11-02' % sys.argv[0]
        exit(1)
    issues = get_issues(created_on=sys.argv[1], closed_on=sys.argv[2])
    continuos = 0
    working = 0

    for i in issues:
        waste_time = get_waste_time_in_minutes(created_on=i.created_on, closed_on=i.closed_on)
        continuos += waste_time.get('continuos')
        working += waste_time.get('working')

    print u'%s horas contínuas ou %s dia(s)' % ((continuos / 60), (continuos / 60 / 24))
    print u'%s horas de trabalho ou %s dia(s)' % ((working / 60), (working / 60 / 24))
