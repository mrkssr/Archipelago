from pathlib import Path

import pandas as pd


def main():
    input_path = Path(__file__, "..", "items.xlsx")
    output_path = Path(__file__, "..", "items.json")

    df = pd.read_excel(input_path, 0)
    df.to_json(output_path, orient="records")


if __name__ == "__main__":
    main()
