# 📘 DariX-MiniORM (DMO) Documentation

**Made by DariXmain**  
📧 darixmain9gmail.com | ariyanminecraft@gmail.com  
📅 Build Date: 5/1/2026 (11/2/1405)

---

## 🚀 Overview

DariX-MiniORM (DMO) is a lightweight, easy-to-use MySQL ORM for Python.  
It simplifies database operations with clean, readable methods.

---

## 📦 Installation & Dependencies

DMO automatically installs required modules:

```python
# Auto-installs mysql-connector-python if missing
from DMO.Core import DMO
```

# Manual install (if needed): 🤖

```python
pip install mysql-connector-python
```

# 🔌 Connection

```python
from DMO.Core import DMO

db = DMO(
    host="localhost",
    port=3306,
    username="root",
    password="your_password",
    database="your_database",
    readtime=30.0,   # optional
    writetime=30.0   # optional
)

db.Connect()
```

## Connection Parameters 💻

Parameter	Type    Required    Description
host	    str	    ✅	       MySQL server host
port	    int	    ✅          MySQL port (usually 3306)
username	str	    ✅	       Database username
password	str	    ✅	       Database password
database	str	    ✅	       Database name
readtime	float   ❌	       Read timeout (seconds)
writetime	float   ❌	       Write timeout (seconds)

# 🛠️ Connection Management

## Disconnect

```python
db.Disconnect()
```

## Reconnect

```python
db.Reconnect()
```

## Ping (Check Connection)

```python
is_alive = db.Ping()  # Returns True/False
```

## Check Connection Status

```python
if db.Isconnected():
    print("Connected!")
```

## Get Raw Connection

```python
raw_conn = db.Connection()  # Returns mysql.connector connection object
```

## Update Config

```python
db.Config({
    "database": "new_database",
    "host": "new_host"
})
```

# 📝 CRUD Operations

## 🔹 Insert
Insert a single row into a table.

```python
result = db.Insert(
    table="users",
    keys=["name", "email", "age"],
    values=["DariX", "darix@example.com", 25]
)

# Returns:
{
    'success': True,
    'rowcount': 1,
    'last_id': 42,      # Auto-increment ID
    'data': {}
}
```

🛑Key	   📢Description
success	    Was the insert successful?
rowcount	Number of affected rows
last_id	    Last inserted auto-increment ID
data	    Reserved for future use

**⚠️ keys and values must have the same length.**

## 🔹 Update
Update rows in a table.

```python
# Simple update
db.Update(
    tablename="users",
    keys=["name", "email"],
    values=["NewName", "new@email.com"],
    wherekey="id",
    wherevalue="1"
)

# Advanced WHERE clause
db.Update(
    tablename="users",
    keys=["status"],
    values=["inactive"],
    advancedwhere="last_login < '2025-01-01'"
)
```

Parameter	    Description
wherekey	    Column name for WHERE clause
wherevalue	    Value for WHERE clause
whereoperation	Operator (default: =)
advancedwhere	Custom WHERE clause (overrides simple WHERE)

## 🔹 Delete
Delete rows from a table.

```python
# Delete specific row
db.Delete(
    tablename="users",
    wherekey="id",
    wherevalue="42"
)

# Delete with condition
db.Delete(
    tablename="users",
    wherekey="status",
    wherevalue="banned",
    whereoperation="="
)

# Advanced WHERE
db.Delete(
    tablename="logs",
    advancedwhere="created_at < NOW() - INTERVAL 30 DAY"
)

# Delete all rows (⚠️ careful!)
db.Delete(tablename="temp_table")
```

## 🔹 Truncate
Quickly remove all rows (faster than DELETE without WHERE):

```python
db.Truncate(tablename="cache_table")
```

## 🔹 Select
Fetch data from a table.

```python
# Select all columns
users = db.Select(tablename="users")

# Select specific columns
users = db.Select(
    tablename="users",
    selecteds=["id", "name", "email"]
)

# With WHERE clause
user = db.Select(
    tablename="users",
    selecteds=["*"],
    wherekey="id",
    wherevalue="1"
)

# Advanced WHERE
active_users = db.Select(
    tablename="users",
    advancedwhere="status = 'active' AND age > 18"
)

# Export as default tuple format (instead of dict)
users = db.Select(
    tablename="users",
    exportdefault=True  # Returns tuples, not dicts
)
```

Parameter	    Default	    Description
selecteds	    ["*"]	    Columns to select
wherekey	    None	    Column for WHERE
wherevalue	    None	    Value for WHERE
whereoperation	"="	        Comparison operator
advancedwhere	None	    Custom WHERE clause
exportdefault	False	    Return as dict (False) or tuple (True)

## 🔹 Raw Query
Execute any custom SQL query.

```python
result = db.Query("SELECT COUNT(*) as total FROM users")
print(result)  # [{'total': 150}]

# Returns tuples instead of dicts
result = db.Query("SELECT * FROM users LIMIT 5", exportdefualt=True)
```

## 🧪 Complete Example

```python
from DMO import DMO

# Initialize
db = DMO(
    host="localhost",
    port=3306,
    username="root",
    password="",
    database="darixshop"
)

# Connect
db.Connect()

# Insert
result = db.Insert(
    table="products",
    keys=["name", "price", "stock"],
    values=["Laptop", 999.99, 10]
)

if result['success']:
    print(f"Product added! ID: {result['last_id']}")

# Select
products = db.Select(tablename="products")
for p in products:
    print(f"{p['name']}: ${p['price']}")

# Update
db.Update(
    tablename="products",
    keys=["price"],
    values=[899.99],
    wherekey="id",
    wherevalue="1"
)

# Delete
db.Delete(
    tablename="products",
    wherekey="stock",
    wherevalue="0"
)

# Custom query
stats = db.Query("SELECT AVG(price) as avg_price FROM products")
print(f"Average price: ${stats[0]['avg_price']}")

# Disconnect
db.Disconnect()
```

# 🐛 Error Handling
## DMO uses Logmanager.Log for logging. All errors are:

** Logged automatically **
** Rolled back (database changes undone) **
** Cursors are always closed (finally blocks) **

# ⚡ Tips

** Always call .Connect() after creating the DMO instance. **
** Use .Ping() to check connection health. **
** .Config() automatically disconnects, updates, and reconnects. **
** For security, always use parameterized queries (automatic in DMO). **

# 📜 License & Credits

## Developer: DariXmain
## Project: DMO (DariX-MiniORM)
## Language: Python
## Database: MySQL

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![MySQL](https://img.shields.io/badge/MySQL-Connector-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)

** "Simple, fast, and clean - the way ORMs should be." **
