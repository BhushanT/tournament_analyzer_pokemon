from main import get_spreadsheet_data, calculate_records_by_price, group_by_price_ranges
from collections import defaultdict

def aggregate_multiple_spreadsheets(sheet_ids):
    """
    Aggregate records from multiple spreadsheets.
    
    Args:
        sheet_ids (list): List of Google Sheet IDs to process
        
    Returns:
        tuple: (grouped_results, raw_data) where raw_data contains individual price/percentage pairs
    """
    combined_records = defaultdict(lambda: {'wins': 0, 'total': 0})
    raw_data = []  # List to store individual price/percentage pairs
    
    for sheet_id in sheet_ids:
        original_sheet_id = get_spreadsheet_data.__defaults__[0]
        get_spreadsheet_data.__defaults__ = (sheet_id,)
        
        try:
            data = get_spreadsheet_data()
        except Exception as e:
            print(f"Error loading sheet {sheet_id}: {str(e)}")
            continue
        
        records = calculate_records_by_price(data)
        
        # Store individual records before combining
        for price, stats in records.items():
            if stats['total'] > 0:  # Only include players with matches
                percentage = (stats['wins'] / stats['total']) * 100
                raw_data.append((price, percentage))
                if price == 3000:  # Print only entries where price is 3000
                    print(f"Price 3000: {percentage}%")
        # Combine records for grouped analysis
        for price, stats in records.items():
            combined_records[price]['wins'] += stats['wins']
            combined_records[price]['total'] += stats['total']
        
        get_spreadsheet_data.__defaults__ = (original_sheet_id,)
    
    # Calculate overall percentages for groups
    percentages = {
        price: (stats['wins'] / stats['total']) * 100 
        for price, stats in combined_records.items()
    }
    
    # Return both grouped results and raw data
    return group_by_price_ranges(percentages), raw_data

if __name__ == "__main__":
    def extract_sheet_id(url):
        # Extract the ID between /d/ and the next /
        start = url.find('/d/') + 3
        end = url.find('/', start)
        return url[start:end]

    with open('spreadsheet_links/spreadsheets_spl.txt', 'r') as f:
        sheet_ids = [extract_sheet_id(line.strip()) 
                    for line in f 
                    if line.strip()]
    combined_results, raw_data = aggregate_multiple_spreadsheets(sheet_ids)
    
    # Add matplotlib imports
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Set the style
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract x and y values
    ranges = list(combined_results.keys())
    percentages = list(combined_results.values())
    
    # Create bar plot
    bars = ax.bar(ranges, percentages)
    
    # Customize the plot
    ax.set_title('Average SPL Win Percentage by Price (2016-2025)', 
                 fontsize=14, pad=20)
    ax.set_xlabel('Price Range (Credits)', fontsize=12)
    ax.set_ylabel('Win Percentage (%)', fontsize=12)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    # Rotate x-axis labels for better readability
    plt.xticks(ha='center')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    
    # Display the plot
    plt.show()
    
    print("\nCombined average win percentages by price range:")
    for range_name, average in combined_results.items():
        print(f"{range_name}: {average:.1f}%")
