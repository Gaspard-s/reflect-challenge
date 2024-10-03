# Reflect Challenge

Author : Gaspard Saliou

# Installation

To set up the project on your local machine, follow these steps:


1. **Create a Virtual Environment**

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. **Install Dependencies**

    ```
    pip install -r requirements.txt
    ```

4. **Initialize the Database**

    The database will be initialized automatically when you run the main script if it does not already exist.


# Usage

Once the installation and configuration steps are complete, you can run the project to fetch and store data.

**replace the token and url used to access the url in launch.sh with the correct values**
    
    export API_URL= url
    export LUCCA_API_TOKEN= token

**If the launch file has not the permission to be executed**

    chmod chmod 755 launch.sh

**Run the Main Script**
    
    
    ./launch.sh
    

This script will:
- Initialize the SQLite database if it doesn't exist.
- Fetch users and departments from the Lucca API.
- Process and transform the fetched data.
- Insert new records into the SQLite database, ensuring no duplicates.
- Log the operations to the console.


# Testing

To ensure the reliability of each function, the project includes unit tests.

**Run the Tests**
    
    pytest
    
This command will discover and run all tests located in the `tests/` directory.

# Database access

**To see if data is incorporate in the db**
  

    sqlite3 reflect_db.sqlite


**To List the tables**

    
    .tables
    

**If you wanna see Users Table**

    
    SELECT * FROM users LIMIT 5;
    