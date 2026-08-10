import numpy as np
import pandas as pd


def _max_drawdown(values: np.ndarray) -> float:
    values = values[~np.isnan(values)]

    if values.size == 0:
        return np.nan

    historical_peak = np.maximum.accumulate(values)
    drawdowns = (historical_peak - values) / historical_peak

    return float(np.max(drawdowns))


def ops_ts_max_drawdown(input_path: str, window: int = 20) -> np.ndarray:
    df = (
        pd.read_parquet(input_path, columns=["symbol", "date", "hhmm", "Close"])
        .sort_values(["symbol", "date", "hhmm"], kind="mergesort")
    )

    ts_max_drawdown = df.groupby("symbol", sort=False)["Close"].transform(
        lambda series: series.rolling(window, min_periods=1).apply(
            _max_drawdown,
            raw=True,
        )
    )

    return ts_max_drawdown.to_numpy(dtype=np.float64, copy=False).reshape(-1, 1)
