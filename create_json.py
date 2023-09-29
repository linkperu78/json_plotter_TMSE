import sqlite3
import json

# Connect to the SQLite database (Change the database name as needed)
conn = sqlite3.connect("aesa.db")
cursor = conn.cursor()

# Execute a SELECT query to retrieve data from the "salud" table
cursor.execute("SELECT * FROM salud")

# Fetch all the rows as a list of tuples
rows = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the rows to a list of dictionaries
data_list = []
for row in rows:
    data_dict = {
        "ID": row[0],
        "P": row[1],
        "I": row[2],
        "F": row[3]
    }
    data_list.append(data_dict)

# Save the data as a JSON file
with open("salud_data.json", "w") as json_file:
    json.dump(data_list, json_file, indent=4)

print("Data from the 'salud' table has been saved as 'salud_data.json'.")
