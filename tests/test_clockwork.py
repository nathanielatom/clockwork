import pytest
import numpy as np

import clockwork as cw


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


# @pytest.mark.parametrize()
# def test_principal_angle():


# @pytest.mark.parametrize()
# def test_circular_sieve()
