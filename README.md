# Analysis of Player Value in Competitive Pokemon Leagues

## Overview
This notebook analyzes the relationship between auction prices and player performance across multiple competitive Pokemon leagues:
- SPL (Smogon Premier League): 2016-2025
- SCL (Smogon Championship League): 2021-2025
- UUPL (UnderUsed Premier League): 2020-2025

The analysis aims to determine whether there's a correlation between the auction price paid for players and their win percentage in matches. This can help evaluate:
- Return on investment for team managers
- Player valuation efficiency in auctions
- Historical trends in player performance relative to cost

## Methodology
We aggregate data from multiple seasons using Google Sheets, extracting win percentages and auction prices for each player. The visualization shows the relationship between these variables to identify any patterns or trends.

## Limitations
Player value is often an subjective metric and does not exclusively depend on win percentage. A player's value also includes their effect on the team with respect to teambuilding support and morale, amongst other factors. Furthermore, auction prices are not always indicative of a player's true value, as they can be influenced by factors such as team needs, market demand, and other extraneous factors. For example, a team may spend a lot of money on a player that they value at the minimum value because they only have one roster spot left so they might as well spend all their remaining money.

A 5 year sample size is also likely too small to draw any meaningful conclusions. Unfortunately, in many cases, the data is not available for a longer time period.



```python
from grouped import aggregate_multiple_spreadsheets
from visualization import plot_results

def extract_sheet_id(url):
    start = url.find('/d/') + 3
    end = url.find('/', start)
    return url[start:end]

```


```python
with open('spreadsheet_links/spreadsheets_spl.txt', 'r') as f:
    sheet_ids = [extract_sheet_id(line.strip()) 
                for line in f 
                if line.strip()]

spl_results = aggregate_multiple_spreadsheets(sheet_ids)
plot_results(spl_results, 'SPL Win Percentage by Price (2016-2025)')
```


    
![png](README_files/README_2_0.png)
    


    
    SPL Win Percentage by Price (2016-2025):
    3000: 43.6%
    3001-5000: 47.9%
    5001-10000: 50.9%
    10001-15000: 52.4%
    15001-20000: 54.1%
    20001+: 59.4%
    


```python
with open('spreadsheet_links/spreadsheets_scl.txt', 'r') as f:
    sheet_ids = [extract_sheet_id(line.strip()) 
                for line in f 
                if line.strip()]

scl_results = aggregate_multiple_spreadsheets(sheet_ids)
plot_results(scl_results, 'SCL Win Percentage by Price (2021-2025)')
```


    
![png](README_files/README_3_0.png)
    


    
    SCL Win Percentage by Price (2021-2025):
    3000: 46.9%
    3001-5000: 44.2%
    5001-10000: 50.0%
    10001-15000: 50.8%
    15001-20000: 52.0%
    20001+: 51.3%
    


```python
with open('spreadsheet_links/spreadsheets_uupl.txt', 'r') as f:
    uupl_sheet_ids = [extract_sheet_id(line.strip()) 
                for line in f 
                if line.strip()]
uupl_results = aggregate_multiple_spreadsheets(uupl_sheet_ids)
plot_results(uupl_results, 'UUPL Win Percentage by Price (2020-2025)')
```

    ['1FvKxEzomLGD2eAHvp5fOHpH_NRJeJrXHIw7Mg8mIdEg', '1H1RBUL5wfuBjPOMW6FG3S0BHT58jPV-gtV7Vt4LnZYI', '1eJRkmYTg8K3ddKO98pdqQqD9pTb2nZlvei-0dAqG6ow', '1z0KW3HKt17X_RUd1GBOcAKMMKbqyEbo6Qk57uOgsSOo', '1RtBBR7OnMA-cujWgEd39aB1zAS_npzI4mHEZ8jmOL24']
    


    
![png](README_files/README_4_1.png)
    


    
    UUPL Win Percentage by Price (2020-2025):
    3000: 40.9%
    3001-5000: 44.8%
    5001-10000: 51.8%
    10001-15000: 54.3%
    15001-20000: 45.8%
    20001+: 58.4%
    
