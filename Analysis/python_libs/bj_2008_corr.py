import numpy as np


def bj_2008_corr(T1, T2):
    """
    Compute the Baker & Jayaram (2008) correlation of spectral acceleration
    epsilon values for NGA ground-motion models.

    The empirical model is fitted over:
        0.01 s <= T1, T2 <= 10 s

    Reference
    ---------
    Baker, J.W. and Jayaram, N. (2008),
    "Correlation of spectral acceleration values from NGA ground motion models,"
    Earthquake Spectra, 24(1), 299-317.

    Parameters
    ----------
    T1 : array_like
        First set of spectral periods, in seconds.
    T2 : array_like
        Second set of spectral periods, in seconds.

    Returns
    -------
    rho : ndarray
        Correlation matrix with shape (len(T1), len(T2)).
    """

    T1 = np.atleast_1d(np.asarray(T1, dtype=float))
    T2 = np.atleast_1d(np.asarray(T2, dtype=float))

    rho = np.zeros((len(T1), len(T2)))

    for i in range(len(T1)):
        for j in range(len(T2)):

            T_min = min(T1[i], T2[j])
            T_max = max(T1[i], T2[j])

            C1 = 1 - np.cos(
                np.pi / 2
                - np.log(T_max / max(T_min, 0.109)) * 0.366
            )

            if T_max < 0.2:
                C2 = (
                    1
                    - 0.105
                    * (1 - 1 / (1 + np.exp(100 * T_max - 5)))
                    * (T_max - T_min)
                    / (T_max - 0.0099)
                )

            if T_max < 0.109:
                C3 = C2
            else:
                C3 = C1

            C4 = (
                C1
                + 0.5
                * (np.sqrt(C3) - C3)
                * (1 + np.cos(np.pi * T_min / 0.109))
            )

            if T_max <= 0.109:
                rho[i, j] = C2
            elif T_min > 0.109:
                rho[i, j] = C1
            elif T_max < 0.2:
                rho[i, j] = min(C2, C4)
            else:
                rho[i, j] = C4

    return rho