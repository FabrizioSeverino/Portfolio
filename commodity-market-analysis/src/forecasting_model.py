import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.cluster import KMeans
import os

def load_data(db_path):
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        p.date, 
        c.commodity_name, 
        c.category,
        p.price_nominal_usd,
        p.price_mom_pct,
        p.price_12m_volatility
    FROM prices p 
    JOIN commodities c ON p.commodity_id = c.commodity_id
    """
    df = pd.read_sql_query(query, conn)
    df['date'] = pd.to_datetime(df['date'])
    conn.close()
    return df

def train_ml_models(df):
    results = {}
    
    # Target Commodities
    targets = ['Gold', 'Crude oil, average', 'Wheat, US SRW']
    df_targets = df[df['commodity_name'].isin(targets)].copy()
    
    df_pivot = df_targets.groupby(['date', 'commodity_name'])['price_nominal_usd'].mean().unstack()
    
    for col in targets:
        series = df_pivot[col].dropna()
        
        # Create lag features for ML
        data = pd.DataFrame({'price': series})
        for i in range(1, 6):
            data[f'lag_{i}'] = data['price'].shift(i)
            
        data = data.dropna()
        X = data.drop('price', axis=1)
        y = data['price']
        
        train_size = int(len(data) * 0.8)
        X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
        y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]
        
        # Random Forest
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        rf_preds = rf.predict(X_test)
        
        # XGBoost
        xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
        xgb.fit(X_train, y_train)
        xgb_preds = xgb.predict(X_test)
        
        results[col] = {
            'RF_RMSE': np.sqrt(mean_squared_error(y_test, rf_preds)),
            'RF_MAE': mean_absolute_error(y_test, rf_preds),
            'XGB_RMSE': np.sqrt(mean_squared_error(y_test, xgb_preds)),
            'XGB_MAE': mean_absolute_error(y_test, xgb_preds),
            'latest_price': y.iloc[-1]
        }
        
    return results

def detect_market_regimes(df):
    """
    Cluster periods into regimes based on momentum and volatility.
    """
    # Use features that represent market state across all commodities
    features = ['price_mom_pct', 'price_12m_volatility']
    
    clustering_data = df.dropna(subset=features).copy()
    X = clustering_data[features]
    
    # Standardize simply
    X_scaled = (X - X.mean()) / X.std()
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clustering_data['regime_cluster'] = kmeans.fit_predict(X_scaled)
    
    # Name clusters based on characteristics
    # Low vol, pos mom -> Bull
    # High vol -> High Volatility
    # neg mom -> Bear
    cluster_centers = kmeans.cluster_centers_
    
    return clustering_data

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../sql/commodity_data.db")
    
    print("Loading data...")
    df = load_data(db_path)
    
    print("Training ML Models...")
    ml_results = train_ml_models(df)
    
    for commodity, metrics in ml_results.items():
        print(f"\\n[{commodity}]")
        for k, v in metrics.items():
            print(f"{k}: {v:.2f}")
            
    print("\\nRunning Market Regime Detection...")
    regime_df = detect_market_regimes(df)
    print(f"Clustered {len(regime_df)} records.")
    print("Regime clusters value counts:")
    print(regime_df['regime_cluster'].value_counts())
