import polars as pl
import numpy as np
from numba import njit

@njit(cache=True)
def _argmin(v, g, w):
    n = len(v)
    out = np.empty(n, np.float64)
    q = np.empty(n, np.int64)
    h = t = s = 0
    for i in range(n):
        if i == 0 or g[i] != g[i - 1]:
            h = t = 0
            s = i
        l = max(s, i - w + 1)
        while h < t and q[h] < l:
            h += 1
        while h < t and v[q[t - 1]] > v[i]:
            t -= 1
        q[t] = i
        t += 1
        out[i] = q[h] - l + 1.0
    return out

def ops_ts_argmin(input_path: str, window: int = 20) -> np.ndarray:
    df = (
        pl.scan_parquet(input_path)
        .select(["symbol", "date", "hhmm", "Close"])
        .collect()
        .with_row_index("_i")
        .sort(["symbol", "date", "hhmm", "_i"])
        .with_columns(pl.col("symbol").cast(pl.Categorical).to_physical().alias("_g"))
    )
    return _argmin(
        df["Close"].to_numpy(),
        df["_g"].to_numpy(),
        window,
    ).reshape(-1, 1)