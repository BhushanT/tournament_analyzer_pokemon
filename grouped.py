from main import get_spreadsheet_data, calculate_records_by_price, group_by_price_ranges
from collections import defaultdict

def aggregate_multiple_spreadsheets(sheet_ids):
    """
    Aggregate records from multiple spreadsheets.
    
    Args:
        sheet_ids (list): List of Google Sheet IDs to process
    """
    combined_records = defaultdict(lambda: {'wins': 0, 'total': 0})
    
    for sheet_id in sheet_ids:
        # Temporarily modify the sheet_id in get_spreadsheet_data
        original_sheet_id = get_spreadsheet_data.__defaults__[0]
        get_spreadsheet_data.__defaults__ = (sheet_id,)
        
        # Get and process data from this spreadsheet
        data = get_spreadsheet_data()
        records = calculate_records_by_price(data)
        
        # Combine records
        for price, stats in records.items():
            combined_records[price]['wins'] += stats['wins']
            combined_records[price]['total'] += stats['total']
        
        # Restore original sheet_id
        get_spreadsheet_data.__defaults__ = (original_sheet_id,)
    
    # Calculate overall percentages
    percentages = {
        price: (stats['wins'] / stats['total']) * 100 
        for price, stats in combined_records.items()
    }
    
    # Group into ranges and return results
    return group_by_price_ranges(percentages)

if __name__ == "__main__":
    def extract_sheet_id(url):
        # Extract the ID between /d/ and the next /
        start = url.find('/d/') + 3
        end = url.find('/', start)
        return url[start:end]

    with open('spreadsheets.txt', 'r') as f:
        sheet_ids = [extract_sheet_id(line.strip()) 
                    for line in f 
                    if line.strip()]
    
    combined_results = aggregate_multiple_spreadsheets(sheet_ids)
    
    print("\nCombined average win percentages by price range:")
    for range_name, average in combined_results.items():
        print(f"{range_name}: {average:.1f}%")
