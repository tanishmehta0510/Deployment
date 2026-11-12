from load import SALES_COLUMNS
from datetime import datetime
import sources

STORE_IDX = SALES_COLUMNS.index("store")
PRODUCT_IDX = SALES_COLUMNS.index("product")
AMOUNT_IDX = SALES_COLUMNS.index("amount")

def calculate_summary(sales_sheet):
    total_revenue = 0
    store_totals = {}
    product_totals = {}

    for row in sales_sheet.iter_rows(min_row=2, values_only=True):
        amount = row[AMOUNT_IDX]
        if amount is None:
            continue
        store, product = row[STORE_IDX], row[PRODUCT_IDX]

        total_revenue += amount
        store_totals[store] = store_totals.get(store, 0) + amount
        product_totals[product] = product_totals.get(product, 0) + amount

    return total_revenue, store_totals, product_totals

def write_summary(workbook):
    sheet = workbook["Summary"]
    sheet.delete_rows(1, sheet.max_row)

    total, store_totals, product_totals = calculate_summary(workbook["Sales"])

    sheet.append(["Total revenue", total])
    sheet.append([])

    sheet.append(["Store", "Revenue"])
    for store, amount in sorted(store_totals.items(), key=lambda item: item[1], reverse=True):
        sheet.append([store, amount])
    sheet.append([])

    sheet.append(["Product", "Revenue"])
    for product, amount in sorted(product_totals.items(), key=lambda item: item[1], reverse=True):
        sheet.append([product, amount])

def get_status(failed_sources):
    return "Success" if not failed_sources else "PARTIAL"

def add_run_history(workbook, stats):
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {"run_time": run_time, **stats, "failed_sources": ", ".join(stats["failed_sources"])}
    workbook["Run_History"].append([row[c] for c in sources.HISTORY_COLUMNS])

def print_run_report(stats):
    print("=" * 50)
    print("DATAPIPE RUNTIME REPORT")
    print(f"Status: {stats['status']}")
    print(f"Rows read: {stats['rows_read']}")
    print(f"Loaded: {stats['loaded']}")
    print(f"Rejected: {stats['rejected']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Failed Sources: {', '.join(stats['failed_sources']) or 'None'}")
    print("=" * 50)