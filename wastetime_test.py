# coding: utf-8
import unittest
from datetime import datetime

from wastetime import get_waste_time_in_minutes


def to_date(str):
    return datetime.strptime(str, '%Y-%m-%d %H:%M')


class TestRedmineReport(unittest.TestCase):

    def test_get_wast_time_from_regular_date(self):
        waste_time = get_waste_time_in_minutes(created_on=to_date('2015-11-03 13:00'), closed_on=to_date('2015-11-04 13:00'))
        self.assertEqual(1440, waste_time.get('continuos'))
        self.assertEqual(480, waste_time.get('working'))

    def test_get_wast_time_when_next_day_is_hollyday(self):
        waste_time = get_waste_time_in_minutes(created_on=to_date('2015-11-18 13:00'), closed_on=to_date('2015-11-20 13:00'))
        self.assertEqual(1440, waste_time.get('continuos'))
        self.assertEqual(480, waste_time.get('working'))

    def test_get_wast_time_when_next_day_is_weekend(self):
        waste_time = get_waste_time_in_minutes(created_on=to_date('2015-11-20 13:00'), closed_on=to_date('2015-11-23 13:00'))
        self.assertEqual(1440, waste_time.get('continuos'))
        self.assertEqual(480, waste_time.get('working'))


if __name__ == '__main__':
    unittest.main()
