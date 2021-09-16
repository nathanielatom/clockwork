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

        Notes
        -----
        This function is vectorized, so performance will be much faster
        when called on very large arrays instead of using a loop.

        """
        return _utils.principal_angle(angle, degrees=True)

    @staticmethod
    def isAngleBetween(first_angle, middle_angle, second_angle):
        """
        Determines whether `middle_angle` is in the smaller sector between the other two bounding angles.

        Uses the smaller sector with acute or obtuse angle, as oppose to the larger sector
        with a reflex angle. The sector is also open (the bounds are exclusive).

        Parameters
        ----------
        first_angle: scalar or array_like
            Unwrapped angle in degrees.
        middle_angle: scalar or array_like
            Unwrapped angle in degrees.
        second_angle: scalar or array_like
            Unwrapped angle in degrees.

        Returns
        -------
        between: bool or array_like
            Whether `middle_angle` is between the others, element-wise.

        Notes
        -----
        This function is vectorized, so performance will be much faster
        when called on very large arrays instead of using a loop.

        """
        smaller_sector = _utils.circular_sub(first_angle, second_angle, closer=True, degrees=True)
        non_reflex = _utils.principal_angle(first_angle + smaller_sector, degrees=True) == _utils.principal_angle(second_angle, degrees=True)
        return _utils.circular_sieve(middle_angle, first_angle if non_reflex else second_angle, second_angle if non_reflex else first_angle, degrees=True, inclusive=False)
