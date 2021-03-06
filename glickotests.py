# -*- coding: utf-8 -*-
from glicko import Glicko, WIN, DRAW, LOSS
from glicko2 import Glicko2


class almost(object):

    def __init__(self, val, precision=3):
        self.val = val
        self.precision = precision

    def almost_equals(self, val1, val2):
        if round(val1, self.precision) == round(val2, self.precision):
            return True
        fmt = '%.{0}f'.format(self.precision)
        mantissa = lambda f: int((fmt % f).replace('.', ''))
        return abs(mantissa(val1) - mantissa(val2)) <= 1

    def __eq__(self, other):
        try:
            if not self.almost_equals(self.val.volatility, other.volatility):
                return False
        except AttributeError:
            pass
        return (self.almost_equals(self.val.mu, other.mu) and
                self.almost_equals(self.val.sigma, other.sigma))

    def __repr__(self):
        return repr(self.val)


def test_glickman_example_of_glicko():
    env = Glicko()
    r1 = env.create_rating(1500, 200)
    r2 = env.create_rating(1400, 30)
    r3 = env.create_rating(1550, 100)
    r4 = env.create_rating(1700, 300)
    rated = env.rate(r1, [(WIN, r2), (LOSS, r3), (LOSS, r4)])
    # env.create_rating(1464, 151.4)
    assert almost(rated) == env.create_rating(1464.106, 151.399)


def test_glickman_example_of_glicko2():
    env = Glicko2(tau=0.5)
    r1 = env.create_rating(1500, 200, 0.06)
    r2 = env.create_rating(1400, 30)
    r3 = env.create_rating(1550, 100)
    r4 = env.create_rating(1700, 300)
    rated = env.rate(r1, [(WIN, r2), (LOSS, r3), (LOSS, r4)])
    # env.create_rating2(1464.06, 151.52, 0.05999)
    assert almost(rated) == env.create_rating(1464.051, 151.515, 0.05999)


def test_issue1():
    env = Glicko2()
    env.determine_volatility(
        env.create_rating(
            -3.5744344457376810986204418441047892,
            1.61207698271845467630214443488512188,
            1.09021015118913666697153530549257994),
        19.070260525665084117008518660441041,
        25.990744829894950385096308309584856)
