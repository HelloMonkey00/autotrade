import requests
from bs4 import BeautifulSoup
import time

def fetch_data(url, proxy, data_points):
    # Set up the SOCKS5 proxy
    proxies = {
        'http': f'socks5://{proxy}',
        'https': f'socks5://{proxy}',
    }

    # Send the HTTP request
    response = requests.get(url)

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the data points
    data = soup.select(data_points)

    return data

# Example usage:
proxy = '43.130.122.195:9080'  # Replace with your SOCKS5 proxy
url = 'http://www.sca.isr.umich.edu/'  # Replace with the URL you want to fetch
data_points = '#front_table tr'  # Replace with the data points you want to extract
# Start the timer
start_time = time.perf_counter()

rows = fetch_data(url, proxy, data_points)

# Stop the timer
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f'Time taken to fetch the webpage: {elapsed_time:.6f} seconds')
# Initialize an empty list to store the data
data = []

# Iterate over each row
for row in rows:
    # Extract all cells from the row
    cells = row.select('td')

    # Check if the first cell's text is "Index of Consumer Sentiment"
    if cells and cells[0].text.strip() == 'Index of Consumer Sentiment':
        # If it is, add the text of all other cells to the data list
        data.extend(cell.text.strip() for cell in cells[0:])

print(data)