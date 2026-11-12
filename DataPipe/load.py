import os
from openpyxl import Workbook, load_workbook
from sources import SALES_COLUMNS, REJECTED_COLUMNS, HISTORY_COLUMNS

def open_workbook(path):
    if os.path.exists(path):
        return load_workbook(path)
    wb = Workbook()
    sales = wb.active
    sales.title = "Sales"
    sales.append(SALES_COLUMNS)
    rejected = wb.create_sheet("Rejected")
    rejected.append(REJECTED_COLUMNS)
    wb.create_sheet("Summary")
    history = wb.create_sheet("Run_History")
    history.append(HISTORY_COLUMNS)
    return wb

def existing_order_ids(sheet):
    ids = set()
    for (value,) in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
        if value is not None:
            ids.add(str(value))
    return ids

def rejected_key(values):
    return tuple("" if v is None else str(v) for v in values)

def add_sales_rows(sheet, rows):
    seen = existing_order_ids(sheet)
    loaded=0
    skipped=0
    for row in rows:
        order_id = str(row["order_id"])
        if order_id in seen:
            skipped += 1
        else:
            sheet.append([row[column] for column in SALES_COLUMNS])
            seen.add(order_id)             
            loaded += 1
    return loaded, skipped

def save_workbook(workbook, path):
    temp_path = path + ".tmp"
    workbook.save(temp_path)
    os.replace(temp_path, path)

def existing_rejected_keys(sheet):
    keys = set()
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not any(row):
                    continue
        else:
            keys.add(rejected_key(row))
    return keys

def add_rejected_rows(sheet, rows):
    seen = existing_rejected_keys(sheet)
    for row in rows:
        values = [row[column] for column in REJECTED_COLUMNS]
        key = rejected_key(values)
        if key not in seen:
            sheet.append(values)
            seen.add(key)
    return None

def load(path, good_rows, bad_rows):
    workbook = open_workbook(path)
    loaded, skipped = add_sales_rows(workbook["Sales"], good_rows)
    add_rejected_rows(workbook["Rejected"], bad_rows)
    return workbook, loaded, skipped