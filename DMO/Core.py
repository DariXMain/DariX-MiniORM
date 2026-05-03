# Made by DariXmain
# Email : DariXMain9gmail.com || ariyanminecraft@gmail.com
# Name : DMO (DariX-MiniORM)
# Build Date : 5/1/2026 (11/2/1405)

import os 
import subprocess
import sys

from typing import Optional
from json import dumps, loads

from Logmanager import Log

try: 
    import mysql.connector
    from mysql.connector.errors import Error
except ModuleNotFoundError:
    Log(
        log="Required modules not found. Installing...",
        type="module"
    )
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
    import mysql.connector
    
    Log(
        log="Required modules installed.",
        type="module"
    )

# Main Source Code

class DMO:
    def __init__(self, host : str, port: int, username: str, password : str, database : str, readtime : Optional[float] = None, writetime : Optional[float] = None):
        self.config = {
            "host" : host,
            "port" : port,
            "user" : username,
            "password" : password,
            "database" : database,
            "read_timeout" : readtime,
            "write_timeout" : writetime
        }
        self.connection = None

    def Connect(self):
        self.Disconnect()
        try:
            self.connection = mysql.connector.connect(**self.config)
            Log(
                "Sql Connected / We have successfully connected.",
                "connection"
            )
            Log(
                dumps(self.config),
                "configs"
            )
        except Exception as e:
            Log(
                f"Connection Error / {e}",
                "connection"
            )

    def Disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
            Log(
                "Sql Connected / Server successfully disconnected.",
                "connection"
            )

    def Reconnect(self):
        if self.connection and self.connection.is_connected():
            try:
                self.connection.reconnect()
                Log(
                    log="SQL Reconnected / Successfully reconnected.",
                    type="reconnect"
                )
            except Exception as e:
                Log(
                    log=f"Reconnect Error / {e}",
                    type="reconnect"
                )
        else:
            self.Connect()

    def Config(self, new_config: dict):
        if self.connection and self.connection.is_connected():
            self.Disconnect()

        self.config.update(new_config)
        self.Connect()
        
        Log(
            log=f"Config updated: {dumps(new_config)}",
            type="configs"
        )

    def Ping(self):
        try:
            if self.connection:
                self.connection.ping(reconnect=True, attempts=3, delay=1)
                Log(
                    log="SQL Ping / Connection is alive.",
                    type="connection"
                )
                return True
            else:
                Log(
                    log="SQL Ping / No connection exists.",
                    type="connection"
                )
                return False
        except Exception as e:
            Log(
                log=f"Ping Error / {e}",
                type="reconnect"
            )
            return False
        
    def Isconnected(self) -> bool:
        return self.connection is not None and self.connection.is_connected()
    
    def Connection(self):
        return self.connection
    
    def Insert(self, table : str, keys : list, values : list):
        cursor = self.connection.cursor()

        if len(keys) != len(values):
            raise ValueError("Failure to read key and value")

        if not keys:
            raise ValueError("Keys list cannot be empty")
        
        result = {
            'success': False,
            'rowcount': 0,
            'last_id': None,
            'data' : {}
        }

        try:
            key_str = ",".join(keys)
            value_str = ",".join(["%s"] * len(values))

            cursor.execute(f"INSERT INTO {table} ({key_str}) VALUES ({value_str})", tuple(values))
            self.connection.commit()

            result['rowcount'] = cursor.rowcount
            result['last_id'] = cursor.lastrowid
            result['success'] = cursor.rowcount > 0
        except Exception as e:
            Log(
                f"Insert Error / {e}", "insert"
            )
            self.connection.rollback()
        finally:
            cursor.close()

        return result
    
    def Update(self, tablename : str, keys : list, values : list, wherekey : Optional[str] = None, wherevalue : Optional[str] = None, whereoperation : str = "=", advancedwhere : Optional[str] = None):
        cursor = self.connection.cursor()

        if len(keys) != len(values):
            raise ValueError("Failure to read key and value")

        if not keys:
            raise ValueError("Keys list cannot be empty")
        
        if wherekey and not wherevalue:
            raise ValueError("where value not found !")
        
        if wherevalue and not wherekey:
            raise ValueError("where key not found !")
        
        try:
            for key, value in enumerate(keys):
                keys[key] = f"{value}=%s"
            key_str = ", ".join(keys)
            
            if advancedwhere: 
                cursor.execute(f"UPDATE {tablename} SET {key_str} WHERE {advancedwhere}", tuple(values))
            else:
                if wherekey:
                    cursor.execute(f"UPDATE {tablename} SET {key_str} WHERE {wherekey}{whereoperation}{wherevalue}", tuple(values))
                else:
                    cursor.execute(f"UPDATE {tablename} SET {key_str}", tuple(values))

            self.connection.commit()
        except Exception as e:
            Log(
                f"Update Error / {e}", "update"
            )
            self.connection.rollback()
        finally:
            cursor.close()

    def Delete(self, tablename : str, wherekey : Optional[str] = None, wherevalue : Optional[str] = None, whereoperation : str = "=", advancedwhere : Optional[str] = None):
        cursor = self.connection.cursor()

        if wherekey and not wherevalue:
            raise ValueError("where value not found !")
        
        if wherevalue and not wherekey:
            raise ValueError("where key not found !")
        
        try:
            if advancedwhere: 
                cursor.execute(f"DELETE FROM {tablename} WHERE {advancedwhere}")
            else:
                if wherekey:
                    cursor.execute(f"DELETE FROM {tablename} WHERE {wherekey}{whereoperation}{wherevalue}")
                else:
                    cursor.execute(f"DELETE FROM {tablename}")

            self.connection.commit()
        except Exception as e:
            Log(
                f"Delete Error / {e}", "delete"
            )
            self.connection.rollback()
        finally:
            cursor.close()

    def Truncate(self, tablename : str):
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(f"TRUNCATE TABLE {tablename}")
            self.connection.commit()
        except Exception as e:
            Log(
                f"TRUNCATE Error / {e}", "delete"
            )
            self.connection.rollback()
        finally:
            cursor.close()

    def Select(self, tablename : str, selecteds : Optional[list] = ["*"], wherekey : Optional[str] = None, wherevalue : Optional[str] = None, whereoperation : Optional[str] = "=", advancedwhere : Optional[str] = None, exportdefault : Optional[bool] = False):

        if wherekey and not wherevalue:
            raise ValueError("where value not found !")
        
        if wherevalue and not wherekey:
            raise ValueError("where key not found !")
        
        cursor = self.connection.cursor(dictionary=not exportdefault)

        try:
            selecteds_str = ", ".join(selecteds)

            if advancedwhere:
                cursor.execute(f"SELECT {selecteds_str} FROM {tablename} WHERE {advancedwhere}")
            else:
                if wherekey:
                    cursor.execute(f"SELECT {selecteds_str} FROM {tablename} WHERE {wherekey}{whereoperation}{wherevalue}")
                else:
                    cursor.execute(f"SELECT {selecteds_str} FROM {tablename}")

            result = cursor.fetchall()

            return result

        except Exception as e:
            Log(
                f"Select Error / {e}", "select"
            )
        finally:
            cursor.close()

    def Query(self, query : str, exportdefualt : Optional[bool] = False):
        cursor = self.connection.cursor(dictionary=not exportdefualt)

        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            Log(
                f"QUERY Error / {e}", "query"
            )
        finally:
            cursor.close()
    
sql = DSS(
    host="localhost",
    port=3306,
    username="root",
    password="",
    database="darixshop"
)
sql.Connect()
