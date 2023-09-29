import json
import sqlite3

folder_path = "json_files/file_"



# Connect to the SQLite database (Change the database name as needed)
conn = sqlite3.connect("aesa.db")
cursor = conn.cursor()

# Create a table to store the data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS salud (
        ID INTEGER PRIMARY KEY,
        P FLOAT,
        I VARCHAR(20),
        F FLOAT
    )
""")


for i in range(3,101):
    new_path = folder_path + f"{i}" + ".json"
    print(f"- {new_path}")
    # Read the JSON data
    with open(new_path, "r") as file:
        data = json.load(file)

    # Extract values from the "registro" list of dictionaries
    extracted_data = []
    for item in data.get("registro", []):
        if "P" in item and "I" in item and "F" in item:
            P = item["P"]
            I = item["I"]
            F = item["F"]
            extracted_data.append((P, I, F))


    # Insert the extracted data into the table
    cursor.executemany("INSERT INTO salud (P, I, F) VALUES (?, ?, ?)", extracted_data)

    # Commit the changes and close the connection
    conn.commit()
conn.close()

print("Data has been stored in the SQL table.")
