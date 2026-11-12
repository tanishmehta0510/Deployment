from datetime import datetime
from sources import REJECTED_COLUMNS

def clean_text(value):
    if value is None:
        return ""
    else:
        value = str(value)
        value = value.strip()
        return value

def parse_date(value):
    try:
        for i in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]:
            try:
                return datetime.strptime(value, i)
            except ValueError:
                continue
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None
    
def parse_quantity(text):
    text = text.strip()
    if text.isdigit() and int(text) > 0:
        return int(text)
    else:
        return None

def parse_price(text):
    try:
        text = text.strip()
        if float(text) > 0:
            return float(text)
        else:
            return None
    except ValueError:
        return None

def clean_row(row):

    order_id = clean_text(row.get("order_id"))
    store = clean_text(row.get("store"))
    date_text = clean_text(row.get("date"))
    product = clean_text(row.get("product"))
    qty_text = clean_text(row.get("qty"))
    price_text = clean_text(row.get("price"))

    order_id = order_id.upper()
    product = product.title()
    date = parse_date(date_text)
    qty = parse_quantity(qty_text)
    price = parse_price(price_text)

    reasons = []
    if order_id == "":
        reasons.append("Missing order_id")
    if date is None:
        reasons.append("Invalid date")
    if product == "":
        reasons.append("Missing product")
    if qty is None:
        reasons.append("Invalid quantity")
    if price is None:
        reasons.append("Invalid price")

    if reasons:
        return None, reasons

    clean = {
        "order_id": order_id,
        "store": store,
        "date": date,
        "product": product,
        "qty": qty,
        "price": price,
        "amount": round(qty * price, 2),
    }
    return clean, []

def make_bad_row(row, reason):
    bad = {}
    for column in REJECTED_COLUMNS:
        if column == "reason":
            bad[column] = reason
        elif column == "store":
            bad[column] = row.get("store")
        else:
            bad[column] = clean_text(row.get(column))
    return bad

def transform(raw_rows):
    good_rows = []                                   
    bad_rows = []
    seen_ids = set()

    for row in raw_rows:
        clean, reasons = clean_row(row)              
        if reasons:                                  
            bad_rows.append(make_bad_row(row, "; ".join(reasons)))
        elif clean["order_id"] in seen_ids:          
            bad_rows.append(make_bad_row(row, "Duplicate order_id in this run"))
        else:                                        
            seen_ids.add(clean["order_id"])
            good_rows.append(clean)

    return good_rows, bad_rows