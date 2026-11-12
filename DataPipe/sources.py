OUTPUT_FILE = "datapipe_output.xlsx"
API_TIMEOUT_SECONDS = 5
SOURCES = [
{"store": "Pune", "type": "csv", "path": "data/pune.csv"},
{"store": "Nagpur", "type": "csv", "path": "data/nagpur.csv"},
{"store": "Mumbai", "type": "api", "url": "https://pythongurukool.com/api/datapipe/mumbai/sales"},
{"store": "Nashik", "type": "api", "url": "https://pythongurukool.com/api/datapipe/nashik/sales"},
]

SALES_COLUMNS = ["order_id", "store", "date", "product", "qty", "price", "amount"]
REJECTED_COLUMNS = ["store", "order_id", "date", "product", "qty", "price", "reason"]
HISTORY_COLUMNS = ["run_time", "status", "rows_read", "loaded", "rejected", "skipped", "failed_sources"]