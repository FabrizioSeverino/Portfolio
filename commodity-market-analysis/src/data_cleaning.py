import pandas as pd
import os

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path)
    
    # Check for core columns
    expected_cols = ['date', 'commodity_name', 'category', 'unit', 'price_nominal_usd', 'price_mom_pct', 'price_yoy_pct', 'price_12m_volatility']
    
    for col in expected_cols:
        if col not in df.columns:
            print(f"Warning: column {col} not found in dataset!")

    # Format dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows without a valid date or commodity_name
    df = df.dropna(subset=['date', 'commodity_name'])
    
    # Forward fill missing prices for a given commodity_name, then backward fill
    df = df.sort_values(by=['commodity_name', 'date'])
    df['price_nominal_usd'] = df.groupby('commodity_name')['price_nominal_usd'].ffill().bfill()
    
    # Drop where price is still NaN
    df = df.dropna(subset=['price_nominal_usd'])
    
    # Create derived columns if missing or just keep the ones present
    df['price_mom_pct'] = df['price_mom_pct'].fillna(0)
    df['price_yoy_pct'] = df['price_yoy_pct'].fillna(0)
    df['price_12m_volatility'] = df['price_12m_volatility'].fillna(0)
    
    print(f"Cleaned dataset shape: {df.shape}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    RAW_DATA = "../data/raw/wb_commodity_price_intelligence_1960_2026.csv"
    CLEANED_DATA = "../data/processed/cleaned_prices.csv"
    
    # Ensure run from src folder or adjust path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, RAW_DATA)
    output_file = os.path.join(base_dir, CLEANED_DATA)
    
    clean_data(input_file, output_file)
