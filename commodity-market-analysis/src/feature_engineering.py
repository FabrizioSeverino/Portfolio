import pandas as pd
import sqlite3
import os
import uuid

def engineer_features_and_load_db(input_path, db_path):
    print(f"Loading cleaned data from {input_path}")
    df = pd.read_csv(input_path)
    
    # Create a unique integer ID or use a UUID for commodities
    commodities = df[['commodity_name', 'category', 'unit']].drop_duplicates().reset_index(drop=True)
    
    # Generate random UUIDs for commodities or simple slug
    commodities['commodity_id'] = commodities['commodity_name'].apply(lambda x: str(uuid.uuid5(uuid.NAMESPACE_DNS, x)))
    
    # Merge back to get commodity_id in prices
    df = pd.merge(df, commodities, on=['commodity_name', 'category', 'unit'], how='left')
    
    # Filter only required columns for prices
    prices = df[['date', 'commodity_id', 'price_nominal_usd', 'price_mom_pct', 'price_yoy_pct', 'price_12m_volatility']]
    
    print(f"Connecting to database at {db_path}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    print("Writing to commodities table...")
    commodities.to_sql('commodities', conn, if_exists='append', index=False)
    
    print("Writing to prices table...")
    prices.to_sql('prices', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print("Database loading complete.")

if __name__ == "__main__":
    CLEANED_DATA = "../data/processed/cleaned_prices.csv"
    DB_PATH = "../sql/commodity_data.db"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, CLEANED_DATA)
    db_file = os.path.join(base_dir, DB_PATH)
    
    # Assume schema is already applied or handled elsewhere
    # But usually df.to_sql with append works if schema exists
    engineer_features_and_load_db(input_file, db_file)
