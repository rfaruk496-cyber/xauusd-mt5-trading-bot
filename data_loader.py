import pandas as pd


def load_data(filename):
    """Load XAUUSD M5 historical data."""

    df = pd.read_csv(filename)

    # Convert column names to lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Convert datetime
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Sort oldest to newest
    df = df.sort_values("datetime")

    # Remove duplicate candles
    df = df.drop_duplicates(subset="datetime")

    # Reset row numbers
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    file = "XAUUSD_5m.csv"

    data = load_data(file)

    print("XAUUSD M5 data loaded successfully!")
    print("Number of candles:", len(data))
    print("\nFirst 5 candles:")
    print(data.head())

    print("\nLast 5 candles:")
    print(data.tail())
