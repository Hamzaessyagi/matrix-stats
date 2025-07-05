import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import data
def import_data():
    return pd.read_csv('medical_examination.csv')

# 2. Add 'overweight' column based on BMI > 25
def add_overweight(df):
    df['overweight'] = ((df['weight'] / ((df['height'] / 100) ** 2)) > 25).astype(int)
    return df

# 3. Normalize 'cholesterol' and 'gluc': 0 = good, 1 = bad
def normalize_data(df):
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)
    return df

# 4. Draw categorical plot
def draw_cat_plot():
    df = import_data()
    df = add_overweight(df)
    df = normalize_data(df)

    # Melt DataFrame for categorical plot
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # Group and count
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']) \
                   .size().reset_index(name='total')

    # Draw seaborn catplot
    fig = sns.catplot(
        data=df_cat,
        kind='bar',
        x='variable',
        y='total',
        hue='value',
        col='cardio'
    ).fig
    plt.show()

    return fig

# 5. Draw heat map of correlations
def draw_heat_map():
    df = import_data()
    df = add_overweight(df)
    df = normalize_data(df)

    # Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate correlation matrix
    corr = df_heat.corr()

    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 9))

    # Draw heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        center=0,
        vmin=-0.5,
        vmax=0.5,
        square=True,
        linewidths=0.5,
        cbar_kws={'shrink': 0.5},
        ax=ax
    )

    return fig

# 6. Optional: Test run (you can also use main.py)
if __name__ == '__main__':
    cat_fig = draw_cat_plot()
    cat_fig.savefig('catplot.png')

    heat_fig = draw_heat_map()
    heat_fig.savefig('heatmap.png')

    print("✅ Les graphiques ont été générés avec succès.")
