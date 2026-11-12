from sources import SOURCES, OUTPUT_FILE
from extract import extract_all
from transform import transform
from load import save_workbook, load
from report import add_run_history, write_summary, get_status, print_run_report

print("Step 1/4: Extracting data")
raw_rows, failed_sources = extract_all(SOURCES)
print("Step 2/4: Cleaning data")
good_rows, bad_rows = transform(raw_rows)
print("Step 3/4: Loading into Excel")
workbook, loaded, skipped = load(OUTPUT_FILE, good_rows, bad_rows)
stats = {
"status": get_status(failed_sources),
"rows_read": len(raw_rows),
"loaded": loaded,
"rejected": len(bad_rows),
"skipped": skipped,
"failed_sources": failed_sources,
}
print("Step 4/4: Writing report")
write_summary(workbook)
add_run_history(workbook, stats)
try:
    save_workbook(workbook, OUTPUT_FILE)
    print_run_report(stats)
except PermissionError:
    print(f"Could not save {OUTPUT_FILE}. Close it in Excel and run the program again.")