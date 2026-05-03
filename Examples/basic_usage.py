
from DMO.Core import DMO

# Initialize connection
db = DMO(
    host="localhost",
    port=3306,
    username="root",
    password="your_password",
    database="your_database"
)

# Connect to database
db.Connect()

# Insert data
result = db.Insert(
    table="users",
    keys=["name", "email", "age"],
    values=["John Doe", "john@example.com", 25]
)

# Select data
users = db.Select(
    tablename="users",
    selecteds=["name", "email"],
    wherekey="age",
    wherevalue="25"
)

for user in users:
    print(f"Name: {user['name']}, Email: {user['email']}")

# Update data
db.Update(
    tablename="users",
    keys=["age"],
    values=[26],
    wherekey="name",
    wherevalue="John Doe"
)

# Delete data
db.Delete(
    tablename="users",
    wherekey="age",
    wherevalue="26"
)

# Always disconnect
db.Disconnect()
