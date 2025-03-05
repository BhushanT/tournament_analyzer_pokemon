import matplotlib.pyplot as plt
import seaborn as sns

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