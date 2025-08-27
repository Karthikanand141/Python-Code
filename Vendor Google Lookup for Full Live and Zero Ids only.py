import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"D:\python for listing ids-20-08-2025\domestic-ids-a1f721ebc4f7.json", scope
)
client = gspread.authorize(creds)

# Open sheet
sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1ljyQiFv-VkDK5BddTelEU2NnhXynaK9AfNDBpoqvad0/edit"
)
worksheet = sheet.sheet1

# Fetch all data
records = worksheet.get_all_records()

# Ask user choice
choice = input("Do you want 1. Full Live ids  2. Full Zero Ids ? Enter 1 or 2: ").strip()

# Columns to check
columns = {
    1: "Export",
    2: "India",
    3: "Bookswagon/Booksbay Website",
    4: "UK",
    5: "UK-2",
    6: "DB Stauts",
}

# Collect results
results = {col: [] for col in columns.values()}

for record in records:
    vendor_id = record.get("Vendor _id")  # exact header name
    if vendor_id is None or str(vendor_id).strip() == "":
        continue  # skip rows with no ID

    vendor_id = str(vendor_id).strip()  # clean spaces

    for col_key in columns.values():
        value = str(record.get(col_key, "")).strip().upper()
        if choice == "1":  # Live
            if value == "LIVE":
                results[col_key].append(vendor_id)
        elif choice == "2":  # Zero or blank
            if value in ("ZERO", ""):
                results[col_key].append(vendor_id)

# Submenu
print("\nSelect which column you want to see:")
for num, col in columns.items():
    label = "Live IDS" if choice == "1" else "Zero IDS"
    print(f"{num}. {col} {label}")
print("7. ALL")  # new option

sub_choice = input("\nEnter option number: ").strip()

label = "Live IDS" if choice == "1" else "Zero IDS"

if sub_choice == "7":  # Print ALL
    print(f"\n=== FULL {label.upper()} ===")
    for col_name in columns.values():
        ids = results[col_name]
        if ids:
            print(f"{col_name} {label}: {','.join(ids)}")
            print(f"Total {col_name} {label}: {len(ids)}\n")
        else:
            print(f"{col_name} {label}: None")
            print(f"Total {col_name} {label}: 0\n")

elif sub_choice.isdigit() and int(sub_choice) in columns:
    col_name = columns[int(sub_choice)]
    ids = results[col_name]
    if ids:
        print(f"\n{col_name} {label}: {','.join(ids)}")
        print(f"Total {col_name} {label}: {len(ids)}")
    else:
        print(f"\n{col_name} {label}: None")
        print(f"Total {col_name} {label}: 0")
else:
    print("Invalid choice.")
