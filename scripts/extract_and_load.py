import pandas as pd
import snowflake.connector
from pathlib import Path
import os 
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()  # Load variables from .env file

# ====================================
# Step-1: Connect to Snowflake
# ====================================
print("Connecting to Snowflake...")

try:
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse='COMPUTE_WH',
        database='ANALYTICS_DB',
        schema='RAW'
    )
    cursor = conn.cursor()
    print('✓ Connected to Snowflake successfully!\n')

except Exception as e:
    print(f"✗ Connection failed to Snowflake: {e}")
    exit()


# ======================================
# Step-2: Define CSV files to load
# ======================================
print("Preparing CSV files to load...")
csv_files = [
    'data/olist_customers_dataset.csv', 
    'data/olist_orders_dataset.csv', 
    'data/olist_order_items_dataset.csv', 
    'data/olist_products_dataset.csv'
]
print(f"Total files to load: {len(csv_files)}\n")


# ======================================
# Step-3: Load CSV files into Snowflake
# ======================================
print("Loading CSV files into Snowflake...")
print("="*60)

for csv_file in csv_files:
    if Path(csv_file).exists():
        print(f"\nProcessing: {csv_file}")

        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Clean column names (remove quotes, convert to lowercase)
        df.columns = df.columns.str.strip('"').str.lower()
        
        print(f"  ✓ Read {len(df):,} rows")
        print(f"  Columns: {list(df.columns)}")

        # Create table name from file name
        table_name = Path(csv_file).stem.upper()
        print(f"  Target table: {table_name}")

        # Write to Snowflake (let it create the table)
        try:
            success, nchunks, nrows, _ = write_pandas(
                conn, 
                df, 
                table_name,
                auto_create_table=True,  # ← Key: Let write_pandas create table
                overwrite=False
            )
            print(f"  ✓ Successfully loaded {nrows:,} rows to {table_name}")

        except Exception as e:
            print(f"  ✗ Error loading {table_name}: {e}")

    else:
        print(f"\n✗ File not found: {csv_file}")

print("\n" + "="*60)

# ======================================
# Step-4: Verify data was loaded
# ======================================
print("\nVERIFICATION - Row counts by table")
print("="*60)

all_successful = True
for csv_file in csv_files:
    table_name = Path(csv_file).stem.upper()
    try:
        result = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchall()
        count = result[0][0]
        status = "✓" if count > 0 else "✗"
        print(f"{status} {table_name:<40} {count:>10,} rows")
        if count == 0:
            all_successful = False
    except Exception as e:
        print(f"✗ {table_name:<40} Error: {e}")
        all_successful = False

print("="*60)


# ======================================
# Step-5: Close connection
# ======================================
cursor.close()
conn.close()

if all_successful:
    print("\n✓ SUCCESS: All CSV files loaded to Snowflake!")
else:
    print("\n⚠ WARNING: Some tables may not have loaded correctly. Check errors above.")

print("✓ Connection closed.\n")