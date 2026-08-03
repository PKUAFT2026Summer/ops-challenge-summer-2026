import numpy as np
import pandas as pd


def ops_rolling_mad(input_path: str, window: int = 20) -> np.ndarray:
    df = (
        pd.read_parquet(input_path, columns=["symbol", "date", "hhmm", "Close"])
        .sort_values(["symbol", "date", "hhmm"], kind="mergesort")
    )

    ts_mad = df.groupby("symbol", sort=False)["Close"].transform(
        lambda series: series.rolling(window, min_periods=1).apply(
            lambda values: np.median(np.abs(values - np.median(values))),
            raw=True,
        )
    )

    return ts_mad.to_numpy(dtype=np.float64, copy=False).reshape(-1, 1)
