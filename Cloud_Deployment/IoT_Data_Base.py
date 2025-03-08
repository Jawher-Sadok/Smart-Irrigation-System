# Step 1: Install the MySQL connector
!pip install mysql-connector-python

# Step 2: Import Libraries
import mysql.connector
import pandas as pd

# Function to connect to the MySQL database and fetch data
def fetch_sensor_data():
    try:
        # Step 3: Establish Connection to the MySQL Database
        db_connection = mysql.connector.connect(
            host="localhost",  # Change this if your MySQL server is hosted elsewhere
            user="new_user",
            password="your-password",
            database="GaiaBase"
        )

        # Step 4: Query the Database
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM sensor_data")
        data = cursor.fetchall()

        # Step 5: Get Column Names and Convert to DataFrame
        column_names = [i[0] for i in cursor.description]
        sensor_data_df = pd.DataFrame(data, columns=column_names)

        # Close the cursor and connection
        cursor.close()
        db_connection.close()

        # Return the DataFrame for visualization
        return sensor_data_df

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Fetch and visualize the data
sensor_data_df = fetch_sensor_data()

# Check if data was retrieved successfully
if sensor_data_df is not None:
    # Display the DataFrame
    display(sensor_data_df)  # Use display for better formatting in Jupyter Notebook
else:
    print("Failed to retrieve data.")
