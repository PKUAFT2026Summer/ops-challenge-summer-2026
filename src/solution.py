import numpy as np
import pandas as pd


def _slope(values: np.ndarray) -> float:
    valid = ~np.isnan(values)

    if valid.sum() < 2:
        return np.nan

    y = values[valid]
    x = np.arange(values.size, dtype=np.float64)[valid]

    x_mean = x.mean()
    y_mean = y.mean()
    denominator = np.sum((x - x_mean) ** 2)

    if denominator == 0:
        return np.nan

    return float(np.sum((x - x_mean) * (y - y_mean)) / denominator)


def ops_ts_rolling_slope(input_path: str, window: int = 20) -> np.ndarray:
    df = (
        pd.read_parquet(input_path, columns=["symbol", "date", "hhmm", "Close"])
        .sort_values(["symbol", "date", "hhmm"], kind="mergesort")
    )

    result = df.groupby("symbol", sort=False)["Close"].transform(
        lambda series: series.rolling(window=window, min_periods=2).apply(
            _slope,
            raw=True,
        )
    )

    return result.to_numpy(dtype=np.float64, copy=False).reshape(-1, 1)
