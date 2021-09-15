import numpy as np


def _scalar_from_0D_array(arr):
    """
    Sometimes operations produce 0D arrays, which are nicer as scalars. Returns an array view otherwise.
    """
    def itemize(obj):
        try:
            return obj.item()
        except (AttributeError, ValueError):
            return obj
    if isinstance(arr, tuple):
        return tuple(itemize(ar[()]) for ar in arr)
    return itemize(arr[()])


def _complex_circular_mean(input_angles, *, degrees=False, full_arc=None, skipnan=False, axis=None):
    """
    The complex mean (basically vector sum) of some angles on the unit circle.
    """
    mean = np.nanmean if skipnan else np.mean
    to_rad = np.deg2rad if degrees else lambda x: x
    if full_arc is not None:
        to_rad = lambda arc: arc * 2 * np.pi / full_arc
    return _scalar_from_0D_array(mean(np.exp(to_rad(input_angles) * 1j), axis=axis))


def circular_mean(input_angles, *, degrees=False,
                  full_arc=None, skipnan=False, axis=None):
    """
    Calculate the circular mean of angles or other circular quantities.

    Parameters
    ----------
    input_angles: array_like
        Array of angles to reduce.

    Keyword Arguments
    -----------------
    degrees: bool, optional
        If ``True``, treat angles in units of degrees, else radians.
    full_arc: scalar, optional
        If not ``None``, manually override the full arc length of a circle. Examples:

            - a circle turning from 0 to 1 representing normalized digital frequency (0.5 is Nyquist);
            - a circle turning from 0 to 24 hours representing time of day.
            - a circle turning from 0 to 365.2422 days representing time of year.
    skipnan: boolean
        Whether the operation should skip NaNs.
    axis: int, optional
        Axis along which to reduce. The default value of ``None`` will reduce to a single value.

    Returns
    -------
    averages: `numpy.ndarray`, `float`, or `str`
        Average of input. If `axis` is ``None``, a single `float` will be returned.

    See Also
    --------
    circular_var
    circular_std
    circular_sieve
    circular_sub

    Notes
    -----
    The circular mean [1]_ is calculated with the following formula:

    .. math:: Arg \\left( \\frac{1}{N} \\sum_{n=1}^{N}{e^{j \\theta_{n}}} \\right)

    where :math:`\\theta_{n}` is a given angle in radians, and :math:`N` is the number of angles.

    .. note:: The circular mean output is also a modular / circular quantity.

    References
    ----------
    .. [1] Wikipedia, "Mean of Circular Quantities".
    https://en.wikipedia.org/wiki/Mean_of_circular_quantities

    """
    to_deg = np.rad2deg if degrees else lambda x: x
    if full_arc is not None:
        to_deg = lambda rad: full_arc * rad / (2 * np.pi)
    complex_mean = _complex_circular_mean(input_angles, degrees=degrees, full_arc=full_arc,
                                          skipnan=skipnan, axis=axis)
    angular_result = to_deg(np.angle(complex_mean))
    return angular_result


def circular_var(input_angles, *, degrees=False,
                 full_arc=None, skipnan=False, axis=None):
    """
    Calculate the circular variance of angles or other circular quantities.

    Parameters
    ----------
    input_angles: array_like
        Array of angles to reduce.

    Keyword Arguments
    -----------------
    degrees: bool, optional
        If ``True``, treat angles in units of degrees, else radians.
    full_arc: scalar, optional
        If not ``None``, manually override the full arc length of a circle. Examples:

            - a circle turning from 0 to 1 representing normalized digital frequency (0.5 is Nyquist);
            - a circle turning from 0 to 24 hours representing time of day.
            - a circle turning from 0 to 365.2422 days representing time of year.
    skipnan: boolean
        Whether the operation should skip NaNs.
    axis: int, optional
        Axis along which to reduce. The default value of ``None`` will reduce to a single value.

    Returns
    -------
    variances: `numpy.ndarray` or `float`
        Circular variance of input. If `axis` is ``None``, a single `float` will be returned.

    See Also
    --------
    circular_mean
    circular_std
    circular_sieve
    circular_sub

    Notes
    -----
    The circular variance [1]_ is calculated with the following formula:

    .. math:: 1 - \\left| \\frac{1}{N} \\sum_{n=1}^{N}{e^{j \\theta_{n}}} \\right|

    where :math:`\\theta_{n}` is a given angle in radians, and :math:`N` is the number of angles.

    .. note:: The circular variance output is *not* a modular / circular quantity! It ranges from [0, 1].

    An approximate square relationship with circular standard deviation only holds for small values.

    References
    ----------
    .. [1] Wikipedia, "Directional Statistics: Measures of Location and Spread".
    https://en.wikipedia.org/wiki/Directional_statistics#Measures_of_location_and_spread

    """
    complex_mean = _complex_circular_mean(input_angles, degrees=degrees, full_arc=full_arc,
                                          skipnan=skipnan, axis=axis)
    return 1 - np.abs(complex_mean)


def circular_std(input_angles, *, degrees=False,
                 full_arc=None, skipnan=False, axis=None):
    """
    Calculate the circular standard deviation of angles or other circular quantities.

    Parameters
    ----------
    input_angles: array_like
        Array of angles to reduce.

    Keyword Arguments
    -----------------
    degrees: bool, optional
        If ``True``, treat angles in units of degrees, else radians.
    full_arc: scalar, optional
        If not ``None``, manually override the full arc length of a circle. Examples:

            - a circle turning from 0 to 1 representing normalized digital frequency (0.5 is Nyquist);
            - a circle turning from 0 to 24 hours representing time of day.
            - a circle turning from 0 to 365.2422 days representing time of year.
    skipnan: boolean
        Whether the operation should skip NaNs.
    axis: int, optional
        Axis along which to reduce. The default value of ``None`` will reduce to a single value.

    Returns
    -------
    standard_deviations: `numpy.ndarray` or `float`
        Circular standard deviation of input. If `axis` is ``None``, a single `float` will be returned.

    See Also
    --------
    circular_var
    circular_mean
    circular_sieve
    circular_sub

    Notes
    -----
    The circular standard deviation [1]_ is calculated with the following formula:

    .. math:: \\sqrt{-2 \\ln \\left| \\frac{1}{N} \\sum_{n=1}^{N}{e^{j \\theta_{n}}} \\right|}

    where :math:`\\theta_{n}` is a given angle in radians, and :math:`N` is the number of angles.

    .. note:: The circular standard deviation output is *not* a modular / circular quantity! It
              ranges from [0, :math:`\\infty`], which in practice is [0, 8.64] due to floating point
              quantization. That's some approximatation!

    An approximate square root relationship with circular variance only holds for small values.

    References
    ----------
    .. [1] Wikipedia, "Directional Statistics: Measures of Location and Spread".
    https://en.wikipedia.org/wiki/Directional_statistics#Measures_of_location_and_spread

    """
    complex_mean = _complex_circular_mean(input_angles, degrees=degrees, full_arc=full_arc,
                                          skipnan=skipnan, axis=axis)
    return np.sqrt(-2 * np.log(np.abs(complex_mean)))


def circular_sieve(input_angles, start_angle, end_angle, *, degrees=False,
                   full_arc=None):
    """
    Pass angles through a sieve or filter to determine whether they are inside or outside of
    a circular sector.

    Parameters
    ----------
    input_angles: array_like
        Array of angles to sieve or filter.
    start_angle: array_like
        Array of start angles that represent the inclusive beginning of the circular sector.
        Must be the same shape as `end_angle` and broadcastable to `input_angles`.
    end_angle: array_like
        Array of end angles that represent the inclusive end of the circular sector.
        Must be the same shape as `start_angle` and broadcastable to `input_angles`.

    Keyword Arguments
    -----------------
    degrees: bool, optional
        If ``True``, treat angles in units of degrees, else radians.
    full_arc: scalar, optional
        If not ``None``, manually override the full arc length of a circle. Examples:

            - a circle turning from 0 to 1 representing normalized digital frequency (0.5 is Nyquist);
            - a circle turning from 0 to 24 hours representing time of day.
            - a circle turning from 0 to 365.2422 days representing time of year.

    Returns
    -------
    within_sector: `numpy.ndarray` or `bool`
        Boolean mask of input angles within the circular sector.

    See Also
    --------
    circular_mean
    circular_var
    circular_std
    circular_sub

    Notes
    -----
    Boundary cases of input angles _exactly_ equal to sector start or end angles may return incorrect
    values in rare cases when non-principal angles are used; that is, angles outside the range
    `[-pi, pi]` when converted to radians.

    """
    shape_start, shape_end = np.shape(start_angle), np.shape(end_angle)
    if shape_start != shape_end:
        message = f'start_angle shape {shape_start} and end_angle shape {shape_end} must be the same'
        raise ValueError(message)
    to_rad = np.deg2rad if degrees else lambda x: x
    to_deg = np.rad2deg if degrees else lambda x: x
    if full_arc is not None:
        to_rad = lambda arc: arc * 2 * np.pi / full_arc
        to_deg = lambda arc: arc * full_arc / 2 * np.pi

    # convert to [-pi, pi) or [-180, 180)
    principal_angle = lambda theta: to_deg(np.angle(np.exp(to_rad(np.asarray(theta)) * 1j)))
    input_angles = principal_angle(input_angles)
    start_angle = principal_angle(start_angle)
    end_angle = principal_angle(end_angle)

    no_cut_mask = start_angle <= end_angle
    branch_cut_mask = ~no_cut_mask
    if np.isscalar(branch_cut_mask):
        scalar_branch_cut_or_vector = branch_cut_mask
        no_cut_mask, branch_cut_mask = ..., ...
    else: # always run in vector case
        scalar_branch_cut_or_vector = True
        if np.isscalar(input_angles):
            input_angles = np.ones_like(start_angle) * input_angles
    mask = np.empty_like(input_angles, dtype=bool)
    mask[no_cut_mask] = (input_angles[no_cut_mask] >= start_angle[no_cut_mask]) & (input_angles[no_cut_mask] <= end_angle[no_cut_mask])
    if scalar_branch_cut_or_vector:
        mask[branch_cut_mask] = (input_angles[branch_cut_mask] >= start_angle[branch_cut_mask]) | (input_angles[branch_cut_mask] <= end_angle[branch_cut_mask])
    return _scalar_from_0D_array(mask)


def circular_sub(angles_minuend, angles_subtrahend, *, closer=True,
                 degrees=False, full_arc=None):
    """
    Calculates angles_minuend - angles_subtrahend on a circle.

    Parameters
    ----------
    angles_minuend: array_like
        Array of angles to subtract from.
    angles_subtrahend: array_like
        Array of angles to subtract.

    Keyword Arguments
    -----------------
    closer: bool, optional
        Whether to return the closer (acute and obtuse) delta between angles or the further (reflex) one.
    degrees: bool, optional
        If ``True``, treat angles in units of degrees, else radians.
    full_arc: scalar, optional
        If not ``None``, manually override the full arc length of a circle. Examples:

            - a circle turning from 0 to 1 representing normalized frequency (0.5 is Nyquist);
            - a circle turning from 0 to 24 hours representing time of day.
            - a circle turning from 0 to 365.2422 days representing time of year.

    Returns
    -------
    differences: `numpy.ndarray`, `float`, or `str`
        Circular difference of input.

    See Also
    --------
    circular_mean
    circular_var
    circular_std
    circular_sieve

    Notes
    -----
    The order of arguments doesn't actually matter as the result is always non-negative.

    References
    ----------
    .. [1] Stackexchange, "Comparing Angles and Working Out the Difference".
    https://gamedev.stackexchange.com/questions/4467/comparing-angles-and-working-out-the-difference

    """
    if full_arc is None:
        full_arc = 360 if degrees else 2 * np.pi
    arc_delta = ((full_arc / 2) - np.abs(np.abs(angles_minuend - angles_subtrahend) - (full_arc / 2))) % full_arc
    if not closer:
        arc_delta = full_arc - arc_delta
    return arc_delta
