import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

class CreateDb:
    
    def create_database(self):
        connection = None   
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),   
                password=os.getenv('DB_PASSWORD'),  
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS sql_ramen")
                print("Database created or already exists.")

                cursor.execute("USE sql_ramen")
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Ramen (
                        Ramen_id INT AUTO_INCREMENT PRIMARY KEY,
                        Soup VARCHAR(20) NOT NULL,
                        Meat VARCHAR(20) NOT NULL,
                        Spicy INT NOT NULL,
                        Typeid INT
                    )
                ''')
                print("Ramen table created.")

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Orders (
                        Order_id INT AUTO_INCREMENT PRIMARY KEY,
                        Ramen_id INT,
                        Price DECIMAL(10, 2) DEFAULT 12,  -- default price to 12
                        Status VARCHAR(20) NOT NULL,
                        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (Ramen_id) REFERENCES Ramen(Ramen_id)
                    )
                ''')
                print("Orders table created.")

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Inventory (
                        Ramen_Type_id INT PRIMARY KEY,
                        Description  VARCHAR(20) NOT NULL,
                        Quantity INT NOT NULL
                    )
                ''')
                print("Inventory table created.")
                connection.commit()
                
        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def add_inventory(self):
        connection = None   
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),   
                password=os.getenv('DB_PASSWORD'),  
                database='sql_ramen'   
            )
            if connection.is_connected():
                print("Connected to MySQL Server")
                cursor = connection.cursor()
          
                cursor.execute('''
                    INSERT INTO Inventory (Ramen_Type_id, Description, Quantity) VALUES 
                    (1, "Miso", 50),
                    (2, "Shoyu", 30),
                    (3, "Tonkatso", 10);
                ''')
                print("Sample data inserted into Inventory.")
                connection.commit()  

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()


    def addSampleData(self):
        connection = None   
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),   
                password=os.getenv('DB_PASSWORD'),  
                database='sql_ramen'  
            )

            if connection.is_connected():
                print("Connected to MySQL Server")
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO Ramen (Soup, Meat, Spicy) VALUES 
                    ('Miso', 'Pork', 2),
                    ('Shoyu', 'Chicken', 1),
                    ('Tonkotsu', 'Beef', 3),
                    ('Shio', 'Seafood', 1);
                ''')
                print("Sample data inserted into Ramen.")
                connection.commit()   

                cursor.execute('SELECT * FROM Ramen;')
                ramen_data = cursor.fetchall()  
                print("Ramen Data:")
                for row in ramen_data:
                    print(row)



        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

if __name__ == "__main__":
    instance = CreateDb()
    
    instance.create_database()
    instance.add_inventory()
    #instance.addSampleData()
