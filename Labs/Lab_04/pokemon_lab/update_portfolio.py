import os
import sys
import json
import pandas as pd

# ------------------------------------------------------------
# 1. Load lookup data (from JSON files)
# ------------------------------------------------------------
def _load_lookup_data(lookup_dir):
    lookup_data = []

    for filename in os.listdir(lookup_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(lookup_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_json = json.load(f)

        cards = raw_json.get("data", [])
        for card in cards:
            card_id = card.get("id")
            card_name = card.get("name")
            set_id = card.get("set", {}).get("id")
            set_name = card.get("set", {}).get("name")

            prices = card.get("tcgplayer", {}).get("prices", {})
            card_market_value = None
            if isinstance(prices, dict) and prices:
                first_variant = next(iter(prices.values()))
                card_market_value = first_variant.get("market")

            lookup_data.append({
                "card_id": card_id,
                "card_name": card_name,
                "set_id": set_id,
                "set_name": set_name,
                "card_market_value": card_market_value
            })

    lookup_df = pd.DataFrame(lookup_data)
    print(f"✅ Loaded lookup data with columns: {lookup_df.columns.tolist()}")
    return lookup_df


# ------------------------------------------------------------
# 2. Load inventory data (from CSV files)
# ------------------------------------------------------------
def _load_inventory_data(inventory_dir):
    all_data = []
    for filename in os.listdir(inventory_dir):
        if filename.endswith(".csv"):
            path = os.path.join(inventory_dir, filename)
            df = pd.read_csv(path)
            all_data.append(df)

    if not all_data:
        print(f"⚠️ No CSV files found in {inventory_dir}")
        return pd.DataFrame()

    inventory_df = pd.concat(all_data, ignore_index=True)

    # ✅ Create card_id (set_id-card_number) to match lookup
    if "set_id" in inventory_df.columns and "card_number" in inventory_df.columns:
        inventory_df["card_id"] = (
            inventory_df["set_id"].astype(str) + "-" + inventory_df["card_number"].astype(str)
        )

    print(f"✅ Loaded inventory data with columns: {inventory_df.columns.tolist()}")
    return inventory_df


# ------------------------------------------------------------
# 3. Merge data
# ------------------------------------------------------------
def _merge_data(inventory_df, lookup_df):
    """
    Merges the inventory and lookup dataframes on 'card_id',
    ensuring clean, consistent output column names.
    """
    merged_df = pd.merge(inventory_df, lookup_df, on="card_id", how="left")

    # Prefer the lookup name (card_name_y), but fall back to inventory if missing
    merged_df["card_name"] = merged_df["card_name_y"].combine_first(merged_df["card_name_x"])
    merged_df["set_id"] = merged_df["set_id_x"].combine_first(merged_df["set_id_y"])

    # Define clean output columns
    final_cols = [
        "card_name",
        "card_id",
        "set_id",
        "set_name",
        "binder_name",
        "page_number",
        "slot_number",
        "card_market_value",
    ]

    # Filter safely to existing columns
    merged_df = merged_df[[c for c in final_cols if c in merged_df.columns]]

    print(f"✅ Merged DataFrame columns (final): {list(merged_df.columns)}")
    return merged_df


# ------------------------------------------------------------
# 4. Update portfolio
# ------------------------------------------------------------
def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    merged_df = _merge_data(inventory_df, lookup_df)

    if merged_df.empty:
        print("⚠️ Merged DataFrame is empty. Nothing to write.")
        return

    # Clean missing values
    merged_df["card_market_value"] = merged_df["card_market_value"].fillna(0.0)
    merged_df["set_name"] = merged_df["set_name"].fillna("NOT_FOUND")

    # Create index column
    merged_df["index"] = (
        merged_df["binder_name"].astype(str) + "-" +
        merged_df["page_number"].astype(str) + "-" +
        merged_df["slot_number"].astype(str)
    )

    final_cols = [
        "card_id", "card_name", "set_name", "card_market_value",
        "binder_name", "page_number", "slot_number", "index"
    ]

    # Keep only valid columns
    final_cols = [col for col in final_cols if col in merged_df.columns]
    merged_df[final_cols].to_csv(output_file, index=False)

    print(f"✅ Portfolio written to {output_file}")


# ------------------------------------------------------------
# 5. Public interface
# ------------------------------------------------------------
def main():
    print("⚡ Running update_portfolio.py in PRODUCTION mode")
    update_portfolio("card_inventory", "card_set_lookup", "card_portfolio.csv")

def test():
    print("⚡ Running update_portfolio.py in TEST mode")
    update_portfolio("card_inventory_test", "card_set_lookup_test", "test_card_portfolio.csv")

if __name__ == "__main__":
    test()