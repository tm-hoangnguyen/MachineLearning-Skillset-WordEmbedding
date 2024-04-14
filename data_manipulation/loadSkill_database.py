## https://stackoverflow.com/questions/62627058/how-to-connect-to-aws-rds-mysql-database-with-python ##
import pymysql
import os
import pandas as pd

# Set environment variable to enable cleartext plugin if needed
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

# Access environment variables for database connection
endpoint = os.environ.get('DB_ENDPOINT')
port = os.environ.get('DB_PORT')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
database = os.environ.get('DB_DATABASE')

## read in test1-output.csv from folder csv_folder_test
skill_input = pd.read_csv('csv_folder_test/Result_OpenRefine.csv')

## Function to capitalize the first letter and not change the rest of the string
def capitalize_first_letter(s):
    return s[0].upper() + s[1:]

# Apply the function to the skill column
skill_input['skill'] = skill_input['skill'].apply(capitalize_first_letter)

# Edit setting to see all rows
# pd.set_option('display.max_rows', None)
# print(skill_input.head(100))

## read skill_input into the linkedin database ##
try:
    # Establish connection to the database
    conn = pymysql.connect(host=endpoint, port=port, user=user, passwd=password, db=database)
    # Create a cursor object
    cursor = conn.cursor()
    
    # Query to delete all records
    delete_query = "DELETE FROM openai_description"
    cursor.execute(delete_query)

    # Iterate over each row in the DataFrame and insert into the database
    for index, row in skill_input.iterrows():
        job_id = row['job_id']
        skill = row['skill']
        # Query to insert data
        query = "INSERT INTO openai_description (job_id, skill) VALUES (%s, %s)"
        # Execute the insert query with parameters
        cursor.execute(query, (job_id, skill))

    # Commit the transaction
    conn.commit()
    print('Data inserted successfully')
    
    # Close cursor and connection
    cursor.close()
    conn.close()

except Exception as e:
    print("Database connection failed due to:", e)