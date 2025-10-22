#!/usr/bin/env python3

import os
import sys
import pandas as pd


def generate_summary(portfolio_file):
    """
    Reads a portfolio CSV, calculates total portfolio value and most valuable card,
    and prints a simplified report to the console.
    """
    # 1. Verify file exists
    if not os.path.exists(portfolio_file):
        print(f"Error: {portfolio_file} does not exist.", file=sys.stderr)
        sys.exit(1)

    # 2. Read CSV into DataFrame
    try:
        df = pd.read_csv(portfolio_file)
    except Exception as e:
        print(f"Error reading {portfolio_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Check if empty
    if df.empty:
        print(f"No data found in {portfolio_file}.")
        return

    # 4. Ensure required columns exist
    required_cols = {'card_market_value', 'card_name', 'card_id'}
    missing = required_cols - set(df.columns)
    if missing:
        print(f"Error: Missing required columns in {portfolio_file}: {', '.join(sorted(missing))}", file=sys.stderr)
        sys.exit(1)

    # 5. Convert card_market_value to numeric safely
    df['card_market_value'] = pd.to_numeric(df['card_market_value'], errors='coerce')

    if df['card_market_value'].dropna().empty:
        print(f"No valid market values found in {portfolio_file}.")
        return

    # 6. Calculate total portfolio value
    total_portfolio_value = df['card_market_value'].sum(min_count=1)

    # 7. Identify most valuable card
    most_valuable_idx = df['card_market_value'].idxmax()
    most_valuable_card = df.loc[most_valuable_idx]

    # 8. Print summary report
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print(
        f"Most Valuable Card: {most_valuable_card['card_name']} "
        f"(ID: {most_valuable_card['card_id']})\n"
        f"Value: ${most_valuable_card['card_market_value']:,.2f}"
    )


# --- Public Interface Functions ---

def main():
    """Run the summary using the production portfolio."""
    print("🚀 Running generate_summary.py in PRODUCTION mode", file=sys.stderr)
    generate_summary("card_portfolio.csv")


def test():
    """Run the summary using the test portfolio."""
    print("⚡ Running generate_summary.py in TEST mode", file=sys.stderr)
    generate_summary("test_card_portfolio.csv")


# --- Execution Block ---

if __name__ == "__main__":
    # Default behavior: run in TEST mode for easier debugging and Makefile integration
    test()