import pytest
import numpy as np

from clockwork.angle_calc import AngleCalc


@pytest.fixture
def calc():
    return AngleCalc()


def test_boundTo180(calc):
    """
    See more extensive tests in test_clockwork.test_principal_angle.
    """
    assert np.allclose(calc.boundTo180(360), 0)
    assert np.allclose(calc.boundTo180(270), -90)
    assert np.allclose(calc.boundTo180(-450), -90)


def test_isAngleBetween(calc):
    """
    See more extensive tests in test_clockwork.test_circular_sieve.
    Note that function differs in that the order of the bounds are
    important, it will happily tell you if your angle is within a sector > 180 degrees.
    """
    assert not calc.isAngleBetween(-90, -180, 80)
    assert calc.isAngleBetween(-90, -180, 110)
    assert not calc.isAngleBetween(-90, 470, 110)
    assert calc.isAngleBetween(-170, -180, 170)
    assert calc.isAngleBetween(170, 180, -170)
    assert calc.isAngleBetween(5*45, 27*45, 90)
