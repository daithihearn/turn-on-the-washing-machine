import unittest
from datetime import datetime, date
# Replace 'your_module' with the actual module name
from PriceService import Price, get_cheapest_period, calculate_average, get_two_cheapest_periods, get_most_expensive_period


test_data = [Price(0.1, datetime(2023, 1, 1, 1)),
             Price(0.2, datetime(2023, 1, 1, 2)),
             Price(0.15, datetime(2023, 1, 1, 3)),
             Price(0.05, datetime(2023, 1, 1, 4)),
             Price(0.05, datetime(2023, 1, 1, 5)),
             Price(0.05, datetime(2023, 1, 1, 6)),
             Price(0.15, datetime(2023, 1, 1, 7)),
             Price(0.15, datetime(2023, 1, 1, 8)),
             Price(0.15, datetime(2023, 1, 1, 9)),
             Price(0.15, datetime(2023, 1, 1, 10)),
             Price(0.15, datetime(2023, 1, 1, 11)),
             Price(0.15, datetime(2023, 1, 1, 12)),
             Price(0.15, datetime(2023, 1, 1, 13)),
             Price(0.15, datetime(2023, 1, 1, 14)),
             Price(0.15, datetime(2023, 1, 1, 15)),
             Price(0.051, datetime(2023, 1, 1, 16)),
             Price(0.051, datetime(2023, 1, 1, 17)),
             Price(0.051, datetime(2023, 1, 1, 18)),
             Price(0.15, datetime(2023, 1, 1, 19)),
             Price(0.25, datetime(2023, 1, 1, 20)),
             Price(0.25, datetime(2023, 1, 1, 21)),
             Price(0.5, datetime(2023, 1, 1, 22)),
             Price(0.5, datetime(2023, 1, 1, 23))]

test_data_consecutive = [Price(0.1, datetime(2023, 1, 1, 1)),
                         Price(0.2, datetime(2023, 1, 1, 2)),
                         Price(0.15, datetime(2023, 1, 1, 3)),
                         Price(0.05, datetime(2023, 1, 1, 4)),
                         Price(0.05, datetime(2023, 1, 1, 5)),
                         Price(0.05, datetime(2023, 1, 1, 6)),
                         Price(0.051, datetime(2023, 1, 1, 7)),
                         Price(0.051, datetime(2023, 1, 1, 8)),
                         Price(0.051, datetime(2023, 1, 1, 9)),
                         Price(0.15, datetime(2023, 1, 1, 10)),
                         Price(0.15, datetime(2023, 1, 1, 11)),
                         Price(0.15, datetime(2023, 1, 1, 12)),
                         Price(0.15, datetime(2023, 1, 1, 13)),
                         Price(0.15, datetime(2023, 1, 1, 14)),
                         Price(0.15, datetime(2023, 1, 1, 15)),
                         Price(0.52, datetime(2023, 1, 1, 16)),
                         Price(0.51, datetime(2023, 1, 1, 17)),
                         Price(0.16, datetime(2023, 1, 1, 18)),
                         Price(0.15, datetime(2023, 1, 1, 19)),
                         Price(0.25, datetime(2023, 1, 1, 20)),
                         Price(0.25, datetime(2023, 1, 1, 21)),
                         Price(0.05, datetime(2023, 1, 1, 22)),
                         Price(0.05, datetime(2023, 1, 1, 23))]


class TestPriceFunctions(unittest.TestCase):

    def test_get_cheapest_period(self):
        prices = test_data
        cheapest = get_cheapest_period(prices, 3)
        self.assertEqual([p.value for p in cheapest], [0.05, 0.05, 0.05])

    def test_calculate_average(self):
        prices = [Price(10, datetime(2023, 1, 1, 1)),
                  Price(20, datetime(2023, 1, 1, 2)),
                  Price(30, datetime(2023, 1, 1, 3))]
        avg = calculate_average(prices)
        self.assertEqual(avg, 20)

    def test_get_two_cheapest_periods(self):
        prices = test_data
        first, second = get_two_cheapest_periods(prices, 3)
        self.assertEqual([p.value for p in first], [0.05, 0.05, 0.05])
        self.assertEqual([p.value for p in second], [0.051, 0.051, 0.051])

    def test_get_two_cheapest_periods_consecutive(self):
        prices = test_data_consecutive
        first, second = get_two_cheapest_periods(prices, 3)
        self.assertEqual([p.value for p in first], [
                         0.05, 0.05, 0.05, 0.051, 0.051, 0.051])
        self.assertEqual(second, [])

    def test_get_most_expensive_period(self):
        prices = test_data
        expensive = get_most_expensive_period(prices, 3)
        self.assertEqual([p.value for p in expensive], [0.25, 0.5, 0.5])


if __name__ == '__main__':
    unittest.main()
