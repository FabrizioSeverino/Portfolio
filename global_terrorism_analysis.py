# Importazione librerie
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

sns.set_theme(style="whitegrid")

# Caricamento Dataset
file_path = "Global Terrorism Index 2023.xlsx"
try:
    df = pd.read_excel(file_path)
    print("Dataset caricato con successo!")
except Exception as e:
    print(f"Errore durante il caricamento: {e}")
    df = pd.DataFrame()  # Fallback per evitare errori successivi

# Se il dataset è vuoto, interrompe ulteriori analisi
if df.empty:
    exit()

# Selezione Colonne e Pulizia
columns_to_keep = ["Country", "Incidents", "Fatalities", "Injuries", "Hostages", "Year"]
df_cleaned = df[columns_to_keep].dropna()

# Conversione a numerico (iterativa per maggiore efficienza)
for col in ["Incidents", "Fatalities", "Injuries"]:
    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")

# Analisi e Aggregazioni
attacks_by_year = df_cleaned.groupby("Year")["Incidents"].sum()
fatalities_by_year = df_cleaned.groupby("Year")["Fatalities"].sum()
top_countries = df_cleaned.groupby("Country")["Incidents"].sum().sort_values(ascending=False).head(10)
injuries_vs_fatalities = df_cleaned.groupby("Country")[["Injuries", "Fatalities"]].sum()

# Visualizzazione 1 - Trend e Top Paesi
fig1 = plt.figure(figsize=(16, 12))
gs1 = GridSpec(2, 2, figure=fig1)

ax1 = fig1.add_subplot(gs1[0, 0])
ax1.plot(attacks_by_year.index, attacks_by_year.values, 'o-b', label="Attacchi")
ax1.plot(fatalities_by_year.index, fatalities_by_year.values, 'x-r', label="Fatalità")
ax1.set_title("Trend Attacchi e Fatalità", fontsize=16, fontweight="bold")
ax1.set_xlabel("Anno")
ax1.set_ylabel("Numero")
ax1.legend()
ax1.grid()

ax2 = fig1.add_subplot(gs1[0, 1])
sns.barplot(
    x=top_countries.values,
    y=top_countries.index,
    hue=top_countries.index,  # Correzione del warning
    palette="rocket",
    ax=ax2,
    legend=False  # Evita la doppia legenda
)
ax2.set_title("Top 10 Paesi - Attacchi", fontsize=16, fontweight="bold")
ax2.set_xlabel("Incidenti")
ax2.set_ylabel("Paese")

ax3 = fig1.add_subplot(gs1[1, :])
injuries_vs_fatalities.sort_values("Fatalities", ascending=False).head(10).plot(
    kind="bar", stacked=True, ax=ax3, color=["#FF9999", "#66B2FF"]
)
ax3.set_title("Decessi vs Feriti (Top 10 Paesi)", fontsize=16, fontweight="bold")
ax3.set_xlabel("Paesi")
ax3.set_ylabel("Numero")

plt.tight_layout()
plt.show()

# Visualizzazione 2 - Distribuzioni e Correlazioni
fig2, axes = plt.subplots(1, 2, figsize=(16, 8))

sns.histplot(df_cleaned["Incidents"], kde=True, bins=30, color="blue", ax=axes[0])
axes[0].set_title("Distribuzione Incidenti", fontsize=16, fontweight="bold")

sns.scatterplot(
    x="Injuries",
    y="Fatalities",
    data=df_cleaned,
    hue="Country",
    palette="viridis",
    legend=False,
    ax=axes[1]
)
axes[1].set_title("Relazione Feriti vs Fatalità", fontsize=16, fontweight="bold")
axes[1].set_xlabel("Feriti")
axes[1].set_ylabel("Fatalità")

plt.tight_layout()
plt.show()
