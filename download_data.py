"""Download + clean + sample the UCI Online Retail dataset.

Applies the same cleaning pipeline used for the committed sample in
``data/online_retail.csv``, deterministically (random_state=42).

Source: https://raw.githubusercontent.com/PacktWorkshops/The-Data-Analysis-Workshop/master/Chapter08/Datasets/online_retail_II.csv
Dataset: UCI Machine Learning Repository, "Online Retail", donated by Dr Daqing Chen. CC BY 4.0.
"""

from pathlib import Path
import pandas as pd

URL = ("https://raw.githubusercontent.com/PacktWorkshops/The-Data-Analysis-Workshop/"
       "master/Chapter08/Datasets/online_retail_II.csv")
DATA_DIR = Path(__file__).resolve().parent / "data"
OUT_PATH = DATA_DIR / "online_retail.csv"
SAMPLE_N = 150_000
SEED = 42


def load(url: str = URL) -> pd.DataFrame:
    return pd.read_csv(
        url,
        encoding="utf-8-sig",
        dtype={"Invoice": "str", "StockCode": "str", "Description": "str", "Country": "str"},
    )


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True, errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # 1. Drop rows with no product description (unidentifiable lines).
    df = df.dropna(subset=["Description"])
    # 2. Exclude cancellations: Invoice numbers starting with 'C' carry
    #    negative Quantity. They are returns, not sales, so they are removed
    #    rather than netted out — the dashboard analyses sales revenue.
    df = df[~df["Invoice"].str.startswith("C", na=False)]
    # 3. Keep only positive quantities/prices: removes bad-debt adjustments,
    #    samples and zero-price lines that would distort revenue.
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]
    df["LineTotal"] = df["Quantity"] * df["Price"]
    return df


def sample(df: pd.DataFrame, n: int = SAMPLE_N, seed: int = SEED) -> pd.DataFrame:
    # Deterministic downsample: the full 43 MB file is too heavy to commit.
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    raw = load()
    print(f"raw rows: {len(raw):,}")
    cleaned = clean(raw)
    print(f"after cleaning: {len(cleaned):,} rows")
    sampled = sample(cleaned)
    sampled.to_csv(OUT_PATH, index=False)
    print(f"saved {OUT_PATH} ({len(sampled):,} rows, seed={SEED})")


if __name__ == "__main__":
    main()
