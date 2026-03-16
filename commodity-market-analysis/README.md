# Global Commodity Intelligence: Price Analysis and Forecasting (1960–2026)

[🇮🇹 Vai alla versione Italiana](#versione-italiana)

A fully integrated Data Science and Data Engineering portfolio project that analyzes 60 years of commodity prices, explores market regimes, evaluates correlation networks, and predicts future prices using Machine Learning models.

**Dataset**: [World Bank Commodity Price Intelligence (1960-2026)](https://www.kaggle.com/datasets/kanchana1990/world-bank-commodity-price-intelligence-19602026)

## 🎯 Features
*   **Data Engineering**: Robust ETL pipeline converting historical CSV data into a standardized SQLite Database.
*   **Exploratory Data Analysis**: Evaluates long-term price trends and volatility cycles.
*   **Correlation Networks**: Analyzes Pearson correlations between energy indices (like Crude Oil) and agricultural commodities (like Wheat or Soybeans).
*   **Machine Learning Forecasting**: Predicts benchmark commodity prices using Random Forest and XGBoost with temporal lag features.
*   **Market Regime Clustering**: Deploys KMeans to classify market conditions (Bull, Bear, High Volatility).
*   **Interactive Dashboard**: A Streamlit application tying all analytical insights into an accessible, interactive presentation layer.

## 🛠 Tech Stack
*   **Data Engineering**: Python, Pandas, SQLite
*   **Data Visualization**: Matplotlib, Seaborn, Plotly Express
*   **Machine Learning**: Scikit-Learn, XGBoost, Statsmodels (ARIMA)
*   **Frontend**: Streamlit
*   **Environment**: Jupyter Notebooks, `venv`

## 🚀 How to Run

1. **Clone the repository and build the environment:**
   ```bash
   git clone <your-repo-link>
   cd commodity-market-analysis
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Data Engineering Pipeline:**
   ```bash
   # Make sure data/raw contains your dataset
   # Initialize SQLite schema
   sqlite3 sql/commodity_data.db < sql/schema.sql
   
   # Run ETL
   python src/data_cleaning.py
   python src/feature_engineering.py
   ```

3. **Explore Jupyter Notebooks:**
   Notebooks are located in the `notebooks/` directory.

4. **Launch the Dashboard:**
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```

---

# Versione Italiana

Un progetto portfolio integrato di Data Science e Data Engineering che analizza 60 anni di prezzi delle materie prime, esplora i regimi di mercato, valuta le reti di correlazione e prevede i prezzi futuri utilizzando modelli di Machine Learning.

**Dataset**: [World Bank Commodity Price Intelligence (1960-2026)](https://www.kaggle.com/datasets/kanchana1990/world-bank-commodity-price-intelligence-19602026)

## 🎯 Funzionalità
*   **Data Engineering**: Robusta pipeline ETL che converte i dati storici in formato CSV in un database SQLite standardizzato.
*   **Analisi Esplorativa dei Dati (EDA)**: Valuta i trend dei prezzi a lungo termine e i cicli di volatilità.
*   **Reti di Correlazione**: Analizza le correlazioni di Pearson tra gli indici energetici (come il petrolio greggio) e le materie prime agricole (come grano o semi di soia).
*   **Previsioni con Machine Learning**: Prevede i prezzi delle materie prime di riferimento utilizzando Random Forest e XGBoost con l'utilizzo di feature temporali (time lags).
*   **Clustering dei Regimi di Mercato**: Utilizza l'algoritmo KMeans per classificare le condizioni di mercato (Toro, Orso, Alta Volatilità).
*   **Dashboard Interattiva**: Un'applicazione Streamlit che raccoglie tutti gli insight analitici in un livello di presentazione interattivo e accessibile.

## 🛠 Tecnologie Utilizzate
*   **Data Engineering**: Python, Pandas, SQLite
*   **Data Visualization**: Matplotlib, Seaborn, Plotly Express
*   **Machine Learning**: Scikit-Learn, XGBoost, Statsmodels (ARIMA)
*   **Frontend**: Streamlit
*   **Ambiente Sviluppo**: Jupyter Notebooks, `venv`

## 🚀 Come avviare il progetto

1. **Clona la repository e crea l'ambiente virtuale:**
   ```bash
   git clone <tuo-link-repo>
   cd commodity-market-analysis
   python -m venv venv
   .\venv\Scripts\activate # Per Windows
   pip install -r requirements.txt
   ```

2. **Esegui la Data Engineering Pipeline:**
   ```bash
   # Assicurati che data/raw contenga il tuo dataset CSV
   # Inizializza lo schema SQLite
   sqlite3 sql/commodity_data.db < sql/schema.sql
   
   # Esegui l'ETL
   python src/data_cleaning.py
   python src/feature_engineering.py
   ```

3. **Esplora i Jupyter Notebooks:**
   I notebook si trovano nella directory `notebooks/`.

4. **Avvia la Dashboard:**
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```
