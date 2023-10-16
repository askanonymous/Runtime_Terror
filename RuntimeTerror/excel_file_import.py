import openpyxl
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nahee3",
)

# Load the workbook
workbook = openpyxl.load_workbook('C:\\Users\\Anjum\\Desktop\\STGI\\H-1B_Disclosure_Data_FY16_1111111111111.xlsx')

# Select the worksheet (replace 'Sheet1' with the name of your sheet)
worksheet = workbook['H-1B_Disclosure_Data_FY16_csv']

# Access the first row (header row)
header_row = worksheet[1]

# Extract column names from the header row
column_names = [cell.value for cell in header_row]

# Now 'column_names' contains the names of the columns
print(column_names)

columns_to_extract = ['CASE_NUMBER', 'PREVAILING_WAGE', 'PW_UNIT_OF_PAY',] 
# Create a list to store data from each column
column_data = [[] for _ in range(len(columns_to_extract))]

# Get data from each column and store it in 'column_data'
for col_idx, column in enumerate(columns_to_extract):
    for row in worksheet.iter_rows(min_row=2, values_only=True):
        column_data[col_idx].append(row[col_idx])
    else :
        pass
print(column_data[1:20])
# Establish a cursor and execute SQL commands
mycursor = db.cursor()
mycursor.execute("USE STGI_1")
mycursor.execute("CREATE TABLE EMPLOYEE_09515 (CASE_NUMBER VARCHAR(255), PREVAILING_WAGE VARCHAR(255), PW_UNIT_OF_PAY VARCHAR(100))")

insert_query = "INSERT INTO EMPLOYEE_09515 (CASE_NUMBER, PREVAILING_WAGE, PW_UNIT_OF_PAY) VALUES (%s, %s, %s)"
insert_data = list(zip(column_data[0], column_data[1], column_data[2]))
mycursor.executemany(insert_query, insert_data)

#start
count_query = "SELECT COUNT(CASE_NUMBER) FROM EMPLOYEE_09515 "
mycursor.execute(count_query)

# Fetch the result (a single row with a single column)
count_value = mycursor.fetchone()[0]

# Print or use the count value
print("Count:",count_value)
# Commit the changes and close the cursor and database connection
db.commit()
mycursor.close()
db.close()