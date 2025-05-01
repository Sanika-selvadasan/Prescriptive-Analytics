# create an sqlite file for the dataset i have

import os
import pandas as pd
import sqlite3
from langchain_community.utilities import SQLDatabase

print('this file is running')

def upload_excel_files_to_sqlite(directory, db_name):
  """
  Uploads multiple Excel files from a given directory to an SQLite database.

  Args:
    directory: Path to the directory containing the Excel files.
    db_name: Name of the SQLite database file.
  """
  
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()

  for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
      file_path = os.path.join(directory, filename)
      df = pd.read_excel(file_path)
    elif filename.endswith('.csv'):
      file_path = os.path.join(directory, filename)
      df = pd.read_csv(file_path)
    else:
      print("No files to upload")
      
    # Create table name from filename (optional)
    table_name = os.path.splitext(filename)[0].replace(" ", "_") 

    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Successfully uploaded {filename} to {table_name} table.")
    except Exception as e:
        print(f"Error uploading {filename}: {e}")

  conn.commit()
  conn.close()

# Example usage
if __name__ == "__main__":
  directory_path = r"C:\Code\Techvantage\ile-insurance-analytics\prescriptive-analytics\sample_dataset"
  database_name = 'tca.db'

  upload_excel_files_to_sqlite(directory_path, database_name)
  print('File uploading completed')


db = SQLDatabase.from_uri("sqlite:///tca.db")
print(db.dialect)
print(db.get_usable_table_names())
# print(db.run("SELECT Coverage, COUNT(*) as frequency FROM monthwise_frequency_analysis GROUP BY Coverage ORDER BY frequency DESC LIMIT 3;"))
print('completed loading table data')







