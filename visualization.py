import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import r2_score

def plot_results(combined_results, title):
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ranges = list(combined_results.keys())
    percentages = list(combined_results.values())
    
    bars = ax.bar(ranges, percentages)
    
    ax.set_title(title, fontsize=14, pad=20)
    ax.set_xlabel('Price Range (Credits)', fontsize=12)
    ax.set_ylabel('Win Percentage (%)', fontsize=12)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    plt.xticks(ha='center')
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n{title}:")
    for range_name, average in combined_results.items():
        print(f"{range_name}: {average:.1f}%")

def plot_scatter(raw_data, title):
    """
    Create a scatter plot of Season win percentages vs prices.
    
    Args:
        raw_data (list): List of (price, percentage) tuples
        title (str): Plot title
    """
    plt.style.use('seaborn')
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract x and y values
    prices, percentages = zip(*raw_data)
    
    # Create scatter plot
    ax.scatter(prices, percentages, alpha=0.5)
    
    # Add trend line
    z = np.polyfit(prices, percentages, 1)
    p = np.poly1d(z)
    ax.plot(prices, p(prices), "r--", alpha=0.8, label=f'Trend line (R² = {r2_score(percentages, p(prices)):.3f})')
    
    # Customize the plot
    ax.set_title(title, fontsize=14, pad=20)
    ax.set_xlabel('Price (Credits)', fontsize=12)
    ax.set_ylabel('Win Percentage (%)', fontsize=12)
    
    # Add legend
    ax.legend()
    
    # Adjust layout
    plt.tight_layout()
    plt.show() 