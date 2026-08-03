import os
import requests


#initialize API base address
API_BASE = os.getenv(
    "VSPMS_API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

#Create Exception type
class APIError(RuntimeError):
    pass

#functions that every api call can reuse
#get, post, delete, etc
#routes
# * means everything after needs to be called by name
#json data used to send data (post, put , patch)
# params for URL query (order = indorder)
# files for file info
# how long the system will wait for a request before stopping
def _request(
    method,
    path,
    *,
    json=None,
    params=None,
    files=None,
    timeout=30,
):
    #sets up http request
    try: 
        response = requests.request(
            method,
            f"{API_BASE}{path}",
            json=json,
            params=params,
            files=files,
            timeout=timeout,
        )
    #when the run request cant reach fast API
    except requests.RequestException as exc:
        raise APIError(
            f"Could not connect to FastAPI: {exc}"
        ) from exc

    #This checks if fastAPI returned an error 
    # returns True for status codes 200 through 399 otherwise prints the detail
    if not response.ok:
        try:
            detail = response.json().get(
                "detail",
                response.text,
            )
        #when theres no json data and responds with plain txt or html, uses raw response body
        except ValueError:
            detail = response.text
        #send backend error to an API error so it can be displayed
        raise APIError(str(detail))
    #when a request is recieved, the json data is returned 
    return response.json()

#
# front end helper funcitons
# these call the backend routes craeted in main.py
#
def health():
    return _request(
        "GET",
        "/api/health",
    )


def dashboard():
    return _request(
        "GET",
        "/api/dashboard",
    )


# Appointments
def get_appointments():
    return _request(
        "GET",
        "/api/appointments",
    )


def add_appointment(appointment):
    return _request(
        "POST",
        "/api/appointments/add",
        json={"appointment": appointment},
    )


def process_appointment():
    return _request(
        "POST",
        "/api/appointments/process",
    )


def undo_appointment():
    return _request(
        "POST",
        "/api/appointments/undo",
    )


def redo_appointment():
    return _request(
        "POST",
        "/api/appointments/redo",
    )


# Parts inventory
# HASHMAP + BST
# uses return request because getting a post / put, to change and update data
# the return request converts the json response to a dict / list
def add_part(item_num, item):
    #post because creating new part
    return _request(
        "POST",
        "/api/parts",
        json={
            "item_num": item_num,
            "item": item,
        },
    )


def get_parts(order="inorder"):
    return _request(
        "GET",
        "/api/parts",
        params={
            "order": order,
        },
    )


def search_part(item_num):
    return _request(
        "GET",
        f"/api/parts/{item_num}",
    )


def delete_part(item_num):
    return _request(
        "DELETE",
        f"/api/parts/{item_num}",
    )

def get_parts_in_range(
    minimum_item_num,
    maximum_item_num,
):
    return _request(
        "GET",
        (
            "/api/parts/range/"
            f"{minimum_item_num}/"
            f"{maximum_item_num}"
        ),
    )


# Priority repairs
# maxHeap
def get_priority_services():
    return _request(
        "GET",
        "/api/priority-repairs/services",
    )


def get_priority_repairs():
    return _request(
        "GET",
        "/api/priority-repairs",
    )

#the payload info put in a dictionary 
#sends payload as json 
def add_priority_repair(payload):
    return _request(
        "POST",
        "/api/priority-repairs",
        json=payload,
    )


def peek_priority_repair():
    return _request(
        "GET",
        "/api/priority-repairs/next",
    )


def process_priority_repair():
    return _request(
        "POST",
        "/api/priority-repairs/process",
    )



# Repair logs
# linkedlist
def get_repair_logs():
    return _request(
        "GET",
        "/api/repair-logs",
    )


def add_repair_log(payload):
    return _request(
        "POST",
        "/api/repair-logs",
        json=payload,
    )


def insert_repair_log(payload):
    return _request(
        "POST",
        "/api/repair-logs/insert",
        json=payload,
    )


def delete_repair_log(index):
    return _request(
        "DELETE",
        f"/api/repair-logs/{index}",
    )


# Repair process
# Graph
def get_repair_services():
    return _request(
        "GET",
        "/api/repair-process",
    )


def get_repair_process(service_name):
    return _request(
        "GET",
        f"/api/repair-process/{service_name}",
    )


# RAG
# recieves the question and top_k = 5 controls how many relevant chunks qdrant retrieves from given pdf
# post method, being sent to the backend
def ask_rag(question, top_k=5):
    return _request(
        "POST",
        "/api/rag/query",
        json={
            "question": question,
            "top_k": top_k,
        },
        timeout=120,
    )

# grabs the pdf and sends it to the uploads
def upload_pdf(uploaded_file):
    return _request(
        "POST",
        "/api/rag/upload",
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        },
        timeout=120,
    )
