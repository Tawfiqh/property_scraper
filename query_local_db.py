import sqlite3

#Connecting to sqlite
conn = sqlite3.connect('property_db.sqlite3')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute("DROP TABLE properties")
print("Table dropped... ")

#Commit your changes in the database
conn.commit()

cursor.execute("""UPDATE urls_to_scrape
SET scraped_yet = False;""")

#Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()