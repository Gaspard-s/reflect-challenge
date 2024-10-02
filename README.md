# Reflect Challenge

Author : Gaspard Saliou

# Project Overview

The Reflect Challenge project automates the process of fetching user and department data from the Lucca API, transforming the data for storage, and managing the data within a local SQLite database. This setup ensures that only new data is inserted, avoiding duplication and maintaining data integrity.

# Installation

To set up the project on your local machine, follow these steps:


1. **Create a Virtual Environment**

    It's recommended to use a virtual environment to manage dependencies.

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. **Install Dependencies**

    ```
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**

    Create a `.env` file in the root directory with the following content:

    ```
    API_URL=https://reflect2-sandbox.ilucca-demo.net
    LUCCA_API_TOKEN=your_lucca_api_token_here
    DATABASE_URI=sqlite:///reflect_db.sqlite
    ```

    - **API_URL**: Base URL for the Lucca API.
    - **LUCCA_API_TOKEN**: Your Lucca API token.
    - **DATABASE_URI**: URI for the SQLite database. Defaults to `sqlite:///reflect_db.sqlite` if not provided.

4. **Initialize the Database**

    The database will be initialized automatically when you run the main script if it does not already exist.


# Usage

Once the installation and configuration steps are complete, you can run the project to fetch and store data.

1. **Run the Main Script**

    ```
    python src/main.py
    ```

    This script will:
    - Initialize the SQLite database if it doesn't exist.
    - Fetch users and departments from the Lucca API.
    - Process and transform the fetched data.
    - Insert new records into the SQLite database, ensuring no duplicates.
    - Log the operations to both the console and a log file located at `data/app.log`.

2. **Logging**

    The project is configured to log detailed information about its operations. Logs are written to both the console and the `data/app.log` file. This includes information about API requests, data processing steps, and any errors encountered.

# Testing

To ensure the reliability of each component, the project includes unit tests.

1. **Run the Tests**

    ```
    pytest
    ```

    This command will discover and run all tests located in the `tests/` directory. Ensure that your virtual environment is activated before running the tests.

2. **Test Coverage**

    The tests cover various aspects of the project, including API interactions, data processing, and database operations. They help in verifying that each module functions correctly and that the overall workflow is reliable.