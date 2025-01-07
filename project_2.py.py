# Importiamo le librerie necessarie
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# 1. Caricamento del dataset
df = pd.read_csv("youth_smoking_drug_data_10000_rows_expanded.csv")

# 2. Panoramica del dataset
print("Descrizione statistica del dataset:")
print(df.describe())  # Descrizione generale dei dati numerici
print("\nPrime 5 righe del dataset:")
print(df.head())      # Prime 5 righe del dataset

# 3. Verifica dei valori nulli
print("\nNumero di valori nulli per colonna:")
print(df.isnull().sum())  # Conta i valori nulli in ogni colonna

# 4. Analisi per Fascia d'Età
print("\nAnalisi per fascia d'età:")
age_group_analysis = df.groupby("Age_Group")[["Smoking_Prevalence", "Drug_Experimentation"]].mean()
print(age_group_analysis)

# 5. Visualizzazione interattiva della prevalenza di fumo per Status Socioeconomico
fig = px.box(df, x="Socioeconomic_Status", y="Smoking_Prevalence", 
             title="Prevalenza di Fumo per Status Socioeconomico",
             labels={"Socioeconomic_Status": "Status Socioeconomico", 
                     "Smoking_Prevalence": "Prevalenza di Fumo (%)"})
fig.show()

# 6. Analisi dell'influenza dei pari e della famiglia
print("\nAnalisi dell'influenza dei pari e della famiglia:")
family_peer_analysis = df.groupby("Peer_Influence")[["Family_Background", "Smoking_Prevalence", "Drug_Experimentation"]].mean()
print(family_peer_analysis)

# 7. Analisi delle tendenze temporali (2020-2024)
print("\nAnalisi delle tendenze temporali (2020-2024):")
temporal_trends = df.groupby("Year")[["Smoking_Prevalence", "Drug_Experimentation"]].mean()

# Correzione per l'asse x con gli anni
temporal_trends.index = temporal_trends.index.astype(int)  # Converte gli anni in numeri interi

# Grafico interattivo per le tendenze temporali
fig = px.line(temporal_trends, x=temporal_trends.index, y=["Smoking_Prevalence", "Drug_Experimentation"],
              labels={"value": "Prevalenza (%)", "Year": "Anno"},
              title="Tendenze di Fumo e Uso di Droghe (2020-2024)", 
              markers=True)
fig.update_xaxes(tickmode='linear')  # Assicura che gli anni siano mostrati in forma corretta (2020, 2021, ...)
fig.show()

#Visualizzazione interattiva per Fascia d'Età (grafico a barre)
fig = px.bar(age_group_analysis, x=age_group_analysis.index, 
             y=["Smoking_Prevalence", "Drug_Experimentation"], 
             title="Prevalenza di Fumo e Uso di Droghe per Fascia d'Età",
             labels={"value": "Prevalenza (%)", "age_group": "Fascia d'Età"})
fig.show()


