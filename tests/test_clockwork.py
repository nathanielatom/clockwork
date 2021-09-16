import pytest
import numpy as np

import clockwork.utils as cw


def test_circular_math():
    angles = [350, 355, 0, 5] # degrees
    assert np.allclose(cw.circular_mean(angles, degrees=True), -2.5)
    assert np.allclose(cw.circular_var(angles, degrees=True), 0.004753458)
    assert np.allclose(cw.circular_std(angles, degrees=True), 0.09762)
    assert np.round(cw.circular_var(angles, degrees=True) * 2, 4) == np.round(cw.circular_std(angles, degrees=True) ** 2, 4)

    angles = np.array([-np.pi/2, np.pi/2]) # radians
    assert np.allclose(cw.circular_var(angles), 1) # indicator of meaningless mean
    # consider replacing values for this case with np.nan and np.inf respectively
    assert cw.circular_mean(angles) == 0
    assert np.allclose(np.round(cw.circular_std(angles), 2), 8.64) # infinity ~= 8.64 I guess lol


@pytest.mark.parametrize("angle,degrees,full_arc,expected", [(790.234, True, None, 70.234),
                                                             (884, True, None, 164),
                                                             (270, True, None, -90),
                                                             (-444, True, None, -84),
                                                             (-180, True, None, -180),
                                                             (180.000000000001, True, None, -180),
                                                             (27*np.pi/4, False, None, 3*np.pi/4),
                                                             (14.5, False, 12, 2.5),
                                                             (872.4844, False, 365.2422, 142)])
def test_principal_angle(angle, degrees, full_arc, expected):
    result = cw.principal_angle(angle, degrees=degrees, full_arc=full_arc)
    assert np.allclose(expected, result)


@pytest.mark.parametrize("angle,start,end,degrees,full_arc,expected", [(790.234, 25, 92, True, None, True),
                                                                       (884, 25, 92, True, None, False),
                                                                       (270, 25, 92, True, None, False),
                                                                       (-444, 25, 92, True, None, False),
                                                                       (-180, 170, -170, True, None, True),
                                                                       (180.000000000001, 170, -170, True, None, True),
                                                                       (27*np.pi/4, np.pi/2, 5*np.pi/4, False, None, True),
                                                                       (14.5, 3, 4.20, False, 12, False),
                                                                       (872.4844, 151, 192, False, 365.2422, False)])
def test_circular_sieve(angle, start, end, degrees, full_arc, expected):
    result = cw.circular_sieve(angle, start, end, degrees=degrees, full_arc=full_arc)
    assert expected == result
