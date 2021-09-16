"""
For UBC Sailbot Software Technical Quiz.
"""

import clockwork.utils as _utils


class AngleCalc:
    """
    Angle calculation utilities.
    """

    @staticmethod
    def boundTo180(angle):
        """
        Convert any angle to the principal branch in [-180, 180).

        Parameters
        ----------
        angle: scalar or array_like
            Unwrapped angle in degrees.

        Returns
        -------
        principal_angle: scalar or array_like
            Angle wrapped to principal branch in degrees.

        Examples
        --------


        Notes
        -----
        This function is vectorized, so performance will be much faster
        when called on very large arrays instead of using a loop.

        """
        return _utils.principal_angle(angle, degrees=True)

    @staticmethod
    def isAngleBetween(first_angle, middle_angle, second_angle):
        return _utils.circular_sieve(middle_angle, first_angle, second_angle, degrees=True)
