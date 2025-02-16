from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os


from operations import operation  # Import the operation class

app = FastAPI()


class TaskRequest(BaseModel):
    task: str


# Helper function to execute tasks based on the task description
def execute_task(task: str):
    # Task A1: Install uv and run datagen.py
    if "install uv" in task:
        email = "shahista.kousar@straive.com"  # Replace with actual user email
        result = operation.install_uv_and_run_script(email)
        return result

    # Task A2: Format contents using prettier
    if "format" in task and "prettier" in task:
        file_path = "/data/format.md"
        operation.format_file_with_prettier(file_path)
        return {"status": "success", "message": "Task A2 executed successfully."}

    # Task A3: Count the number of Wednesdays
    if "Wednesdays" in task:
        input_path = "/data/dates.txt"
        output_path = "/data/dates-wednesdays.txt"
        operation.count_wednesdays(input_path, output_path)
        return {"status": "success", "message": "Task A3 executed successfully."}

    # Task A4: Sort contacts by last_name and first_name
    if "sort contacts" in task:
        input_path = "/data/contacts.json"
        output_path = "/data/contacts-sorted.json"
        operation.sort_contacts(input_path, output_path)
        return {"status": "success", "message": "Task A4 executed successfully."}

    # Task A5: Write first line of the 10 most recent .log files
    if "first line" in task and ".log files" in task:
        logs_dir = "/data/logs"
        output_file = "/data/logs-recent.txt"
        operation.get_most_recent_logs(logs_dir, output_file)
        return {"status": "success", "message": "Task A5 executed successfully."}

    # Task A6: Create index file for Markdown files
    if "Markdown" in task and "index file" in task:
        docs_dir = "/data/docs"
        output_file = "/data/docs/index.json"
        operation.create_index(docs_dir, output_file)
        return {"status": "success", "message": "Task A6 executed successfully."}

    # Task A7: Extract sender's email address from email message
    if "extract" in task and "email address" in task:

        operation.extract_sender_email()
        return {"status": "success", "message": "Task A7 executed successfully."}

    # Task A8: Extract credit card number from image
    if "credit card" in task and "image" in task:
        operation.extract_credit_card_number()
        return {"status": "success", "message": "Task A8 executed successfully."}

    # Task A9: Find most similar pair of comments
    if "similar pair" in task and "comments" in task:
        input_file = "/data/comments.txt"
        output_file = "/data/comments-similar.txt"
        operation.find_most_similar_comments(input_file, output_file)
        return {"status": "success", "message": "Task A9 executed successfully."}

    # Task A10: Calculate total sales of "Gold" ticket type
    if "total sales" in task and "Gold" in task:
        db_path = "/data/ticket-sales.db"
        output_file = "/data/ticket-sales-gold.txt"
        operation.calculate_gold_ticket_sales(db_path, output_file)
        return {"status": "success", "message": "Task A10 executed successfully."}

    return {"status": "error", "message": "Task not recognized."}


@app.post("/run")
async def run_task(request: TaskRequest):
    task = request.task
    if not task:
        raise HTTPException(status_code=400, detail="Task description is required")

    try:
        result = execute_task(task)
        if result["status"] == "success":
            return {"message": result["message"]}
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/read")
async def read_file(path: str):
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(path, "r") as file:
            content = file.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
