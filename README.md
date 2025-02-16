# Project 1: Data Science Tools API

This project provides a FastAPI-based API for performing various data science tasks. It includes endpoints for running tasks, reading files, and generating data.

## Overview

The project consists of two main components:

*   **`app.py`:** The main FastAPI application that defines the API endpoints and handles requests.
*   **`operations.py`:** Contains the functions that perform the actual data science tasks.

## Files

*   **`app.py`:**
    *   Defines the FastAPI application.
    *   Handles routing and request processing.
    *   Includes endpoints:
        *   `/run`: Executes a specified task.
        *   `/read`: Reads the content of a file.
    *   Uses `operations.py` to perform the tasks.
*   **`operations.py`:**
    *   Contains functions for various data science tasks, including:
        *   Installing `uv` and running a data generation script.
        *   Formatting Markdown files with Prettier.
        *   Counting Wednesdays in a list of dates.
        *   Sorting contacts.
        *   Extracting data from log files, emails, and images.
        *   Calculating ticket sales.
    *   Includes security measures to prevent accessing files outside the `/data` directory.
*   **`datagen.py`:** (Attached File)
    *   A script to generate various data files required for the tasks.
    *   Generates Markdown files, date lists, contact lists, log files, email files, credit card images, comments, and a ticket sales database.
*   **`requirements.txt`:** Lists the Python dependencies required to run the application.
*   **`Dockerfile`:** Defines the steps to build a Docker image for the application.
*   **`.dockerignore`:** Specifies files and directories to exclude from the Docker image.
*   **`README.md`:** This file, providing an overview of the project.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application (Development)

1.  **Run the FastAPI application:**

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```

    This will start the server on `http://localhost:8000`. The `--reload` flag enables automatic reloading upon code changes.

## Running the Application (Docker)

1.  **Build the Docker image:**

    ```bash
    docker build -t your-dockerhub-username/your-repo-name .
    ```

2.  **Run the Docker image:**

    ```bash
    docker run --rm -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000 your-dockerhub-username/your-repo-name
    ```

    *   Replace `your-dockerhub-username/your-repo-name` with your Docker Hub username and repository name.
    *   Ensure the `AIPROXY_TOKEN` environment variable is set on your host machine.

## API Endpoints

### `/run` (POST)

Executes a specified task.

*   **Method:** POST
*   **Request Body:**

    ```json
    {
      "task": "task description"
    }
    ```

*   **Example:**

    ```bash
    curl -X "POST" "http://localhost:8000/run" -H "accept: application/json" -H "Content-Type: application/json" -d '{"task": "install uv"}'
    ```

*   **Tasks:**
    *   `install uv`: Installs `uv` and runs the `datagen.py` script.
    *   `format prettier`: Formats the `format.md` file using Prettier.
    *   `Wednesdays`: Counts the number of Wednesdays in the `dates.txt` file.
    *   `sort contacts`: Sorts the contacts in the `contacts.json` file.
    *   `first line .log files`: Writes the first line of the 10 most recent `.log` files to `logs-recent.txt`.
    *   `Markdown index file`: Creates an index file for Markdown files in the `docs` directory.
    *   `extract email address`: Extracts the sender's email address from the `email.txt` file.
    *   `credit card image`: Extracts the credit card number from the `credit_card.png` image.
    *   `similar pair comments`: Finds the most similar pair of comments in the `comments.txt` file.
    *   `total sales Gold`: Calculates the total sales of "Gold" tickets in the `ticket-sales.db` database.

### `/read` (GET)

Reads the content of a file.

*   **Method:** GET
*   **Query Parameter:**
    *   `path`: The path to the file to read (must be within the `/data` directory).
*   **Example:**

    ```bash
    curl -X "GET" "http://localhost:8000/read?path=/data/format.md"
    ```

## Data Generation

The `datagen.py` script generates the data files required for the tasks.  To run it:

1.  Make sure you have the dependencies installed (see "Setup and Installation").
2.  Run the script, providing your email address as an argument:

    ```bash
    python datagen.py your.email@example.com
    ```

    This will create the necessary files in the `/data` directory.  If you are running in Docker, this directory is *inside the container*.  See the "Docker" section for how to copy files into the container.

## Security

The application implements security measures to prevent accessing files outside the `/data` directory. The `ensure_safe_path` function in `operations.py` validates all file paths before they are used.

## Environment Variables

*   `AIPROXY_TOKEN`: Required for accessing the LLM API.  Pass this as an environment variable when running the Docker container (e.g., `-e AIPROXY_TOKEN=$AIPROXY_TOKEN`).

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Test your changes thoroughly.
5.  Submit a pull request.

## License

[Specify the license for your project, e.g., MIT License]
