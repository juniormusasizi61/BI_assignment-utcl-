import mysql.connector
import csv
import os

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Juniormusasizi6',
    'database': 'retail_sales_dw'
}

# Define CSV file paths (all in E:\Web)
csv_files = {
    'DimProduct': 'E:/Web/ProductDim.csv',  # ProductID,ProductName,Category,SubCategory
    'DimCustomer': 'E:/Web/CustomerDim.csv',  # CustomerID,CustomerName,Segment,City,District,Country
    'DimDate': 'E:/Web/DateDim.csv',  # DateID,FullDate,Month,Quarter,Year
    'FactSales': 'E:/Web/SalesFact.csv'  # SaleID,ProductID,CustomerID,DateID,Quantity,SalesAmount
}

# Connect to MySQL
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Failed to connect to MySQL: {err}")
    exit(1)

# Validate file existence
for table, file_path in csv_files.items():
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        cursor.close()
        conn.close()
        exit(1)
    print(f"Found file: {file_path}")

# Load data into tables
try:
    # Load DimProduct
    row_count = 0
    with open(csv_files['DimProduct'], 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            try:
                cursor.execute("""
                    INSERT INTO DimProduct (ProductID, ProductName, Category, SubCategory)
                    VALUES (%s, %s, %s, %s)
                """, (int(row[0]), row[1], row[2], row[3]))
                row_count += 1
            except (ValueError, mysql.connector.Error) as e:
                print(f"Error loading row {row} into DimProduct: {e}")
                continue
        print(f"Loaded DimProduct: {row_count} rows")

    # Load DimCustomer
    row_count = 0
    with open(csv_files['DimCustomer'], 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            try:
                cursor.execute("""
                    INSERT INTO DimCustomer (CustomerID, CustomerName, Segment, City, District, Country)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (int(row[0]), row[1], row[2], row[3], row[4], row[5]))
                row_count += 1
            except (ValueError, mysql.connector.Error) as e:
                print(f"Error loading row {row} into DimCustomer: {e}")
                continue
        print(f"Loaded DimCustomer: {row_count} rows")

    # Load DimDate
    row_count = 0
    with open(csv_files['DimDate'], 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            try:
                year = int(row[4])
                if year < 1000:  # Validate Year
                    print(f"Invalid Year in row {row}: {row[4]}")
                    continue
                cursor.execute("""
                    INSERT INTO DimDate (DateID, FullDate, Month, Quarter, Year)
                    VALUES (%s, %s, %s, %s, %s)
                """, (int(row[0]), row[1], row[2], int(row[3]), year))
                row_count += 1
            except (ValueError, mysql.connector.Error) as e:
                print(f"Error loading row {row} into DimDate: {e}")
                continue
        print(f"Loaded DimDate: {row_count} rows")

    # Load FactSales (disable foreign key checks)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    row_count = 0
    missing_date_ids = set()
    with open(csv_files['FactSales'], 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            try:
                date_id = int(row[3])
                # Check if DateID exists in DimDate
                cursor.execute("SELECT DateID FROM DimDate WHERE DateID = %s", (date_id,))
                if not cursor.fetchone():
                    missing_date_ids.add(date_id)
                cursor.execute("""
                    INSERT INTO FactSales (SaleID, ProductID, CustomerID, DateID, Quantity, SalesAmount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (int(row[0]), int(row[1]), int(row[2]), date_id, int(row[4]), float(row[5])))
                row_count += 1
            except (ValueError, mysql.connector.Error) as e:
                print(f"Error loading row {row} into FactSales: {e}")
                continue
        print(f"Loaded FactSales: {row_count} rows")

    # Insert missing DateID values into DimDate
    if missing_date_ids:
        print(f"Missing DateID values: {missing_date_ids}")
        for date_id in missing_date_ids:
            try:
                cursor.execute("""
                    INSERT INTO DimDate (DateID, FullDate, Month, Quarter, Year)
                    VALUES (%s, NULL, 'Unknown', 0, 0)
                """, (date_id,))
            except mysql.connector.Error as e:
                print(f"Error inserting DateID {date_id} into DimDate: {e}")
        print(f"Inserted {len(missing_date_ids)} missing DateID values into DimDate")

    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Commit the transaction
    conn.commit()
    print("Data loaded successfully into retail_sales_dw")

except mysql.connector.Error as err:
    print(f"Database error during data loading: {err}")
except Exception as e:
    print(f"General error during data loading: {e}")
finally:
    cursor.close()
    conn.close()