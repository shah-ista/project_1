import subprocess
import requests
import platform  # Import the platform module
from fastapi import HTTPException
import datetime
import json
import os
import glob
import base64
import sqlite3
from sentence_transformers import SentenceTransformer, util
import os

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")


class operation:
    def install_uv_and_run_script(email):
        try:
            subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            subprocess.run(["pip", "install", "uv"], check=True)

        # Install required dependencies (Pillow) in the same environment
        datagen_path = os.path.join(os.getcwd(), "datagen.py")  # Corrected path
        url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
        if not os.path.exists(datagen_path):
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(datagen_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("datagen.py downloaded successfully.")
            except requests.RequestException as e:
                raise RuntimeError(f"Error downloading datagen.py: {e}")
        else:
            print("datagen.py already exists.")

        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(datagen_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print("datagen.py downloaded successfully.")
        except requests.RequestException as e:
            raise RuntimeError(f"Error downloading datagen.py: {e}")

        try:
            # Detect Python executable correctly on Windows vs. Linux/Mac
            if platform.system() == "Windows":
                python_executable = (
                    subprocess.run(["where", "python"], capture_output=True, text=True)
                    .stdout.strip()
                    .split("\n")[0]
                )
            else:
                python_executable = subprocess.run(
                    ["which", "python"], capture_output=True, text=True
                ).stdout.strip()

            # Run datagen.py
            result = subprocess.run(
                [python_executable, datagen_path, email],  # Use the email argument
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"datagen.py output:\n{result.stdout}")
            return {"status": "success", "message": "Task A1 completed successfully."}
        except subprocess.CalledProcessError as e:
            error_message = f"Error running datagen.py: {e.stderr}"
            print(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    def format_file_with_prettier(file_path):
        try:
            # Check if npx is available
            subprocess.run(["npx", "--version"], check=True, capture_output=True, text=True)
            subprocess.run(["npx", "prettier@3.4.2", "--write", file_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to format file: {str(e)}")
        except FileNotFoundError:
            raise RuntimeError("npx is not installed or not available in the system's PATH.")
        print(f"Formatted file: {file_path}")

    def count_wednesdays(file_path, output_path):
        date_formats = ["%Y-%m-%d", "%Y/%m/%d %H:%M:%S", "%b %d, %Y", "%d-%b-%Y"]

        def parse_date(date_str):
            for date_format in date_formats:
                try:
                    return datetime.datetime.strptime(date_str, date_format)
                except ValueError:
                    continue
            raise ValueError(f"time data '{date_str}' does not match any known format")

        with open(file_path, "r") as file:
            dates = file.readlines()

        wednesday_count = 0
        for date in dates:
            try:
                if parse_date(date.strip()).weekday() == 2:
                    wednesday_count += 1
            except ValueError as e:
                print(f"Skipping invalid date: {e}")

        print(wednesday_count)
        with open(output_path, "w") as output_file:
            output_file.write(str(wednesday_count))

    def sort_contacts(input_path, output_path):
        try:
            # Read the contacts from the input file
            with open(input_path, "r", encoding="utf-8") as file:
                contacts = json.load(file)

            # Sort the contacts by last_name and then by first_name
            sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

            # Write the sorted contacts to the output file
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(sorted_contacts, file, indent=4)
        except Exception as e:
            print(e)

    def get_most_recent_logs(logs_dir, output_file, num_logs=10):
        try:
            # Get a list of all .log files in the directory
            log_files = glob.glob(os.path.join(logs_dir, "*.log"))

            # Sort the log files by modification time, most recent first
            log_files.sort(key=os.path.getmtime, reverse=True)

            # Get the first line of the most recent log files
            recent_lines = []
            for log_file in log_files[:num_logs]:
                with open(log_file, "r", encoding="utf-8") as file:
                    first_line = file.readline().strip()
                    recent_lines.append(first_line)

            # Write the recent lines to the output file
            with open(output_file, "w", encoding="utf-8") as file:
                for line in recent_lines:
                    file.write(line + "\n")
        except Exception as e:
            print(e)

    # Define the logs directory and output file path
    # logs_dir = r"D:\data_Science\project_1\data\logs"
    # output_file = r"D:\data_Science\project_1\data\logs-recent.txt"

    # # Get the most recent logs and write to the output file
    # get_most_recent_logs(logs_dir, output_file)

    def create_index(docs_dir, output_file):
        try:
            index = {}

            # Find all Markdown files in the directory
            md_files = glob.glob(os.path.join(docs_dir, "*.md"))

            for md_file in md_files:
                with open(md_file, "r", encoding="utf-8") as file:
                    for line in file:
                        if line.startswith("#"):
                            title = line[2:].strip()
                            filename = os.path.basename(md_file)
                            index[filename] = title
                            print(
                                f"Found title '{title}' in file '{filename}'"
                            )  # Debugging statement
                            break

            # Write the index to the output file
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(index, file, indent=4)
            print(f"Index written to '{output_file}'")  # Debugging statement
        except Exception as e:
            print(e)

    # Define the docs directory and output file path
    # docs_dir = r"D:\data_Science\project_1\data\docs"
    # output_file = r"D:\data_Science\project_1\data\docs\index.json"

    # # Create the index file
    # create_index(docs_dir, output_file)

    def request_llm(prompt=None, url=None):
        try:
            # Construct the messages based on the presence of the URL
            if url:
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": url, "details": "low"},
                            },
                        ],
                    },
                ]
            else:
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt},
                ]

            json_body = {
                "messages": messages,
                "temperature": 0,
            }

            response = requests.post(
                "https://llmfoundry.straive.com/azure/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview",
                headers={
                    "Authorization": f"Bearer {AIPROXY_TOKEN}:llmproxy",
                },
                json=json_body,
            )
            response_data = response.json()
            output = response_data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(e)
            output = None
        return output

    def extract_sender_email():
        input_file = "/data/email.txt"
        output_file = "/data/email-sender.txt"

        if not os.path.exists(input_file):
            raise HTTPException(status_code=404, detail=f"Input file {input_file} does not exist.")
        with open(input_file, "r") as file:
            email_content = file.read()
            prompt = (
                f"Extract the sender's email address from the following email:\n\n{email_content}"
            )
            email_address = operation.request_llm(prompt, None)
        with open(output_file, "w") as outputfile:
            outputfile.write(email_address)

    # extract_sender_email()

    def encode_image_as_data_url(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"

    def extract_credit_card_number():
        input_image = "/data/credit_card.png"
        output_file = "/data/credit-card.txt"

        if not os.path.exists(input_image):
            raise HTTPException(
                status_code=404, detail=f"Input image {input_image} does not exist."
            )

        prompt = "Extract the  number from the following image if the number is 16 digit and provide only the numbers"

        data_url = operation.encode_image_as_data_url(input_image)
        card_number = operation.request_llm(prompt, data_url)

        if card_number:
            # Remove spaces from the card number
            card_number = card_number.replace(" ", "")
            with open(output_file, "w", encoding="utf-8") as outputfile:
                outputfile.write(card_number)
            print(f"Credit card number written to '{output_file}'")
        else:
            print("Failed to extract credit card number.")

    # extract_credit_card_number()

    def find_most_similar_comments(input_file, output_file):
        model = SentenceTransformer("all-MiniLM-L6-v2")
        # Read the comments from the input file
        with open(input_file, "r", encoding="utf-8") as file:
            comments = file.readlines()

        # Generate embeddings for each comment
        embeddings = model.encode(comments, convert_to_tensor=True)

        # Compute the cosine similarity between each pair of comments
        similarities = util.pytorch_cos_sim(embeddings, embeddings)

        # Find the most similar pair of comments
        max_similarity = -1
        most_similar_pair = (None, None)
        for i in range(len(comments)):
            for j in range(i + 1, len(comments)):
                if similarities[i][j] > max_similarity:
                    max_similarity = similarities[i][j]
                    most_similar_pair = (comments[i].strip(), comments[j].strip())

        # Write the most similar pair of comments to the output file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(most_similar_pair[0] + "\n")
            file.write(most_similar_pair[1] + "\n")

        print(f"Most similar comments written to '{output_file}'")

    # input_file = r"D:\data_Science\project_1\data\comments.txt"
    # output_file = r"D:\data_Science\project_1\data\comments-similar.txt"
    # find_most_similar_comments(input_file, output_file)

    def calculate_gold_ticket_sales(db_path, output_file):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            print(f"Connected to database: {db_path}")

            # Query to calculate the total sales for "Gold" ticket type
            query = """
            SELECT SUM(units * price) AS total_sales
            FROM tickets
            WHERE type = 'Gold'
            """

            cursor.execute(query)
            result = cursor.fetchone()
            total_sales = result[0] if result[0] is not None else 0
            print(f"Total sales for 'Gold' ticket type: {total_sales}")

            # Write the total sales to the output file
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(str(total_sales))
            print(f"Total sales written to file: {output_file}")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            # Close the database connection
            if conn:
                conn.close()
                print("Database connection closed")

    # Define the database path and output file path
    # db_path = r"D:\data_Science\project_1\data\ticket-sales.db"
    # output_file = r"D:\data_Science\project_1\data\ticket-sales-gold.txt"

    # # Calculate the total sales for "Gold" ticket type and write to the output file
    # calculate_gold_ticket_sales(db_path, output_file)
    #
