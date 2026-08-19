import pandas as pd


def load_data(filename):
    """
    Load historical XAUUSD candle data from CSV.
    """

    df = pd.read_csv(filename)

    print("Columns found:")
    print(df.columns.tolist())

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    required_columns = [
        "time",
        "open",
        "high",
        "low",
        "close"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    df["time"] = pd.to_datetime(df["time"])

    df = df.sort_values("time")
    df = df.drop_duplicates(subset="time")
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    print("XAUUSD data loader ready.")
