import openpyxl
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="runtime_terror_db",
    user="postgres",
    password="admin123"
)

# Load the workbook
workbook = openpyxl.load_workbook('C:\\Users\\sanjo\\Desktop\\Hb\\H-1B_Disclosure_Data_FY16_csv.xlsx')

# Select the worksheet (replace 'Sheet1' with the name of your sheet)
worksheet = workbook['H-1B_Disclosure_Data_FY16_csv']

# Access the first row (header row)
header_row = worksheet[1]

# Extract column names from the header row
column_names = [cell.value for cell in header_row]

# Now 'column_names' contains the names of the columns
print(column_names)

columns_to_extract = ['CASE_NUMBER', 'PREVAILING_WAGE', 'PW_UNIT_OF_PAY','TOTAL_SALARY'] 
# Create a list to store data from each column
column_data = [[] for _ in range(len(columns_to_extract))]

# Get data from each column and store it in 'column_data'
for col_idx, column in enumerate(columns_to_extract):
    for row in worksheet.iter_rows(min_row=2, values_only=True):
        column_data[col_idx].append(row[col_idx])

# Create a cursor and execute SQL commands
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS data_2016 (CASE_NUMBER VARCHAR(255), PREVAILING_WAGE VARCHAR(255), PW_UNIT_OF_PAY VARCHAR(100), TOTAL_SALARY DOUBLE)")

insert_query = "INSERT INTO data_2016 (CASE_NUMBER, PREVAILING_WAGE, PW_UNIT_OF_PAY, T) VALUES (%s, %s, %s)"
insert_data = list(zip(column_data[0], column_data[1], column_data[2]))
cur.executemany(insert_query, insert_data)

# Commit the changes and close the cursor and database connection
conn.commit()
cur.close()
conn.close()
