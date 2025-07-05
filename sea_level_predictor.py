import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('sea-level_fig-1.csv')
    
    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', label='Data')
    
    # Get slope and y-intercept of the best fit line (all data)
    res = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    slope, intercept = res.slope, res.intercept
    
    # Plot first line of best fit (1880-2050)
    years_all = pd.Series(range(1880, 2051))
    plt.plot(years_all, intercept + slope * years_all, 'r', label='Best Fit Line 1880-2013')
    
    # Get data from year 2000 onwards
    df_recent = df[df['Year'] >= 2000]
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    slope_recent, intercept_recent = res_recent.slope, res_recent.intercept
    
    # Plot second line of best fit (2000-2050)
    years_recent = pd.Series(range(2000, 2051))
    plt.plot(years_recent, intercept_recent + slope_recent * years_recent, 'green', 
             label='Best Fit Line 2000-2013')
    
    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()
    
    # Save plot and return data for testing
    plt.savefig('sea_level_plot.png')
    return plt.gca()