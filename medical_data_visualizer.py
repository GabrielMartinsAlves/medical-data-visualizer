import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Importar dados e adicionar coluna 'overweight'
df = pd.read_csv('medical_examination.csv')
df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2 > 25).astype(int)

# Normalizar 'cholesterol' e 'gluc'
df[['cholesterol', 'gluc']] = (df[['cholesterol', 'gluc']] > 1).astype(int)

# Função para o gráfico categórico
def draw_cat_plot():
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    fig = sns.catplot(data=df_cat, kind="bar", x="variable", y="total", hue="value", col="cardio").fig
    fig.savefig('catplot.png')
    return fig
# Função para o mapa de calor
def draw_heat_map():
    df_filtered = df[(df['ap_lo'] <= df['ap_hi']) &
                     df['height'].between(df['height'].quantile(0.025), df['height'].quantile(0.975)) &
                     df['weight'].between(df['weight'].quantile(0.025), df['weight'].quantile(0.975))]

    corr = df_filtered.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(16, 9))
    sns.heatmap(corr, mask=mask, square=True, annot=True, fmt="0.1f", linewidths=0.5)
    fig.savefig('heatmap.png')
    return fig
