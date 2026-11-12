import csv
import sources
import requests

def read_csv_source(source):
    rows = []                                                  
    with open(source["path"], newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:                                     
            row["store"] = source["store"]                     
            rows.append(row)
    return rows

def fetch_api_source(source):
    response = requests.get(source["url"], timeout=sources.API_TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()["orders"]                                             
    rows = []
    for item in data:
        item["store"] = source["store"]
        rows.append(item)
    return rows

def extract_all(sources):
    all_rows = []                                          
    failed_sources = []
    for source in sources:                                 
        try:
            if source["type"] == "csv":                    
                rows = read_csv_source(source)
            else:
                rows = fetch_api_source(source)
            all_rows.extend(rows)                         
            print(f"{source['store']}: {len(rows)} rows read")
        except (FileNotFoundError, requests.exceptions.RequestException):
            failed_sources.append(source["store"])
            print(f"{source['store']}: FAILED")
    return all_rows, failed_sources

if __name__ == "__main__":
    import sources as src
    all_rows, failed = extract_all(src.SOURCES)
    print(all_rows[:1], failed)