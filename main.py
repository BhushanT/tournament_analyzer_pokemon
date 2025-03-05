import pandas as pd
from collections import defaultdict

def get_spreadsheet_data(sheet_id="1aBskkibF1216tcVJBbdMIptr7eFONa5kcpDmLd5Qmlw"):
    data = None
    # different sheets have different column names
    for sheet_name in ["Overall%20MVP", "Overall"]:
        try:
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
            df = pd.read_csv(url)
            

            # for some reason pandas doesn't detect the price column correctly, but only on certain sheets
            if 'Unnamed: 2' in df.columns:
                df = df.rename(columns={'Unnamed: 2': 'Price '})
            
            
            required_columns = ['Price ', 'Cost ', 'Cost:']
            if not any(col in df.columns for col in required_columns):
                continue
                
            data = df
            break
        except Exception as e:
            print(f"Error accessing sheet '{sheet_name}': {e}")
            continue
    
    if data is None:
        raise Exception("Could not load data from either sheet name")
    
    filtered_data = []
    for _, row in data.iterrows():
        try:
            if 'Price ' in row.index:
                price_col = 'Price '
            elif 'Cost ' in row.index:
                price_col = 'Cost '
            elif 'Cost:' in row.index:
                price_col = 'Cost:'
            else:
                raise Exception("Could not find Price or Cost column")
                
            if 'Record ' in row.index:
                record_col = 'Record '
            elif 'Record:' in row.index:
                record_col = 'Record:'
            else:
                raise Exception("Could not find Record column")
                
            if pd.isna(row[price_col]) or pd.isna(row[record_col]):
                continue
            filtered_data.append({
                'Price': float(row[price_col]),
                'Record': row[record_col].strip()
            })
        except Exception as e:
            print(f"Error processing row: {e}")
            
    return filtered_data

def calculate_records_by_price(data):
    price_stats = defaultdict(lambda: {'wins': 0, 'total': 0})

    for row in data:
        if 'Record' in row:
            price = int(row['Price'])
            record_parts = row['Record'].split(' - ')
            wins = int(record_parts[0])
            losses = int(record_parts[1])
            total_games = wins + losses
            
            price_stats[price]['wins'] += wins
            price_stats[price]['total'] += total_games
    
    return dict(price_stats)

def group_by_price_ranges(percentages):
    ranges = {
        '3000': [],
        '3001-5000': [],
        '5001-10000': [],
        '10001-15000': [],
        '15001-20000': [],
        '20001+': []
    }
    
    for price, percentage in percentages.items():
        if price == 3000:
            ranges['3000'].append(percentage)
        elif 3000 < price <= 5000:
            ranges['3001-5000'].append(percentage)
        elif price <= 10000:
            ranges['5001-10000'].append(percentage)
        elif price <= 15000:
            ranges['10001-15000'].append(percentage)
        elif price <= 20000:
            ranges['15001-20000'].append(percentage)
        else:
            ranges['20001+'].append(percentage)
    
    return {
        range_name: sum(percentages)/len(percentages) if percentages else 0 
        for range_name, percentages in ranges.items()
    }

if __name__ == "__main__":
    data = get_spreadsheet_data()
    records = calculate_records_by_price(data)
    
    percentages = {
        price: (stats['wins'] / stats['total']) * 100 
        for price, stats in records.items()
    }

    range_averages = group_by_price_ranges(percentages)
    print("\nAverage win percentages by price range:")
    for range_name, average in range_averages.items():
        print(f"{range_name}: {average:.1f}%")
