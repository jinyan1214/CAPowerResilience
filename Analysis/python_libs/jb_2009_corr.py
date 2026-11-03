import numpy as np

def jayaram_baker_correlation_2009(im, h, flag_clustering=False):
    """Computing intra-event correlation coeffcieint between Sa(T) at two sites
    Reference:
        Jayaram and Baker (2009) Correlation model for spatially distributed
        ground-motion intensities
    Input:
        im: intensity measure name
        h: distance between the two sites
        flag_clustering: the geologic condition of the soil varies widely over
                         the region (default: false)
    Output:
        rho: correlation between normalized intra-event residuals
    """
    # parse period form im
    try:
        # for Sa
        if im.startswith('SA'):
            T = float(im[3:-1])
        elif im.startswith('PGA'):
            T = 0.0
    except ValueError:
        print(
            f'CorrelationModel.jayaram_baker_correlation_2009: error - cannot handle {im}'
        )

    if T >= 1.0:
        b = 22.0 + 3.7 * T
    elif flag_clustering:
        b = 8.5 + 17.2 * T
    else:
        b = 40.7 - 15.0 * T
    rho = np.exp(-3.0 * h / b)
    return rho