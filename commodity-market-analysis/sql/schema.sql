-- schema.sql

DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS commodities;

CREATE TABLE commodities (
    commodity_id TEXT PRIMARY KEY,
    commodity_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit TEXT NOT NULL
);

CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    commodity_id TEXT NOT NULL,
    price_nominal_usd REAL,
    price_mom_pct REAL,
    price_yoy_pct REAL,
    price_12m_volatility REAL,
    FOREIGN KEY (commodity_id) REFERENCES commodities (commodity_id)
);

CREATE INDEX idx_prices_date ON prices(date);
CREATE INDEX idx_prices_commodity ON prices(commodity_id);
