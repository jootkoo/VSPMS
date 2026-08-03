from pathlib import Path
import shutil
from threading import RLock

import inngest
import inngest.fast_api
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

#data structure imports
from data_structures.bst import BinarySearchTree 
from data_structures.graph import Graph
from data_structures.hashmap import HashMap
from data_structures.linkedList import dLinkedList
from data_structures.maxHeap import maxHeap
from data_structures.queue import Queue
from data_structures.stack import Stack

from rag_ai.ragAI import (
    inngest_client,
    query_manual,
    rag_ingest_pdf,
    rag_query_pdf_ai,
)


# -----------------------------------------------------------------------
# Shared in-memory data-structure instances
# -----------------------------------------------------------------------

#reentrant lock, locks if the api recieves a bunch of request at the same time, multiple routes will modify at the same time
state_lock = RLock()

#initializing the data structures from the data structures folder
appointments = Queue()
appointment_undo = Stack()
appointment_redo = Stack()

parts_hashmap = HashMap(30000)
parts_tree = BinarySearchTree()

priority_repairs = maxHeap()
repair_logs = dLinkedList()


# -----------------------------------------------------------------------
# API response helpers
# -----------------------------------------------------------------------

# reads the Queue from front to rear without changing the Queue class
def get_appointment_values():
    values = []
    #start from the front
    current_node = appointments.front
    #goes all the way until it reaches the end which should be none
    while current_node is not None:
        values.append(current_node.value)
        current_node = current_node.next

    return values



#Empty a Stack by popping all elements unitl empty
def clear_stack(stack):
    while not stack.is_empty():
        stack.pop()

#The root of the MaxHeap is the largest value, but the entire heap
#array is not guaranteed to be in descending order
#returns in sorted order
def get_ordered_priority_repairs():
    return sorted(
        priority_repairs.heap,
        key=lambda repair: repair[0],
        reverse=True,
    )

#Read the doubly linked list from head to tail without changing it
def get_repair_log_values():
    values = []
    current_node = repair_logs.head

    while current_node is not None:
        values.append(current_node.value)
        current_node = current_node.next

    return values


#iterate through dlinkedlist to remove at index
def remove_repair_log_at_index(index):
    #Validate the requested linked-list position
    if index < 0 or index >= len(repair_logs):
        raise IndexError("Repair log not found")

    # move from the head to the requested node
    current_node = repair_logs.head

    #iterate to the index
    for _ in range(index):
        current_node = current_node.next

    
    removed_value = current_node.value

    #Reconnect the node before the removed node
    if current_node.previous is None:
        repair_logs.head = current_node.next
    else:
        current_node.previous.next = current_node.next

    #Reconnect the node after the removed node
    if current_node.next is None:
        repair_logs.tail = current_node.previous
    else:
        current_node.next.previous = current_node.previous

    #Detach the removed node and update the linked-list size
    current_node.next = None
    current_node.previous = None
    repair_logs.size -= 1

    return removed_value

#initialize the workflows existing (would be replaced with items inside a database)
REPAIR_WORKFLOWS = {'fuel leak': [('Confirm fuel leak', 10), ('Shut vehicle off and isolate ignition sources', 2), ('Identify fuel type and leak location', 10), ('Relieve fuel-system pressure', 15), ('Inspect fuel lines, hoses, tank, rail, injectors, and seals', 10), ('Replace damaged component', 90), ('Reconnect fuel system', 20), ('Pressurize fuel system', 10), ('Check for additional leaks', 10), ('Clear related diagnostic codes', 5), ('Road test and recheck', 15)], 'complete brake failure': [('Do not drive vehicle', 2), ('Tow vehicle into service bay', 30), ('Inspect brake fluid level', 10), ('Check for external brake fluid leaks', 10), ('Inspect master cylinder', 10), ('Inspect brake lines and hoses', 10), ('Inspect calipers and wheel cylinders', 10), ('Inspect brake booster and pedal linkage', 10), ('Repair failed brake component', 90), ('Refill brake fluid', 5), ('Bleed brake system', 30), ('Verify brake pedal pressure', 10), ('Perform low-speed brake test', 10), ('Perform final leak inspection', 10)], 'engine overheating': [('Allow engine to cool', 30), ('Check coolant level', 10), ('Inspect for coolant leaks', 10), ('Pressure-test cooling system', 30), ('Inspect radiator', 10), ('Inspect cooling system hoses and reservoir', 10), ('Test radiator fan', 20), ('Test thermostat', 20), ('Test water pump', 20), ('Check radiator cap', 10), ('Check for combustion gases in coolant', 20), ('Repair failed cooling system component', 90), ('Refill and bleed cooling system', 30), ('Run engine to operating temperature', 15), ('Verify engine temperature stability', 10), ('Road test vehicle', 15)], 'tire sidewall bulge': [('Do not drive vehicle at high speed', 2), ('Inspect damaged tire', 10), ('Confirm tire sidewall damage', 10), ('Inspect wheel for impact damage', 10), ('Remove wheel', 8), ('Remove damaged tire', 10), ('Inspect valve stem or TPMS sensor', 10), ('Mount replacement tire', 15), ('Balance wheel', 10), ('Reinstall wheel', 8), ('Torque lug nuts', 5), ('Set tire pressure', 5), ('Verify TPMS operation', 10)], 'flashing check engine light': [('Reduce engine load and stop driving if engine is shaking', 2), ('Scan diagnostic trouble codes', 10), ('Record freeze-frame data', 5), ('Inspect for active engine misfire', 10), ('Inspect ignition coils', 10), ('Inspect spark plugs', 10), ('Inspect fuel injectors', 10), ('Check fuel pressure', 10), ('Check engine compression if required', 45), ('Repair cause of engine misfire', 60), ('Clear diagnostic trouble codes', 5), ('Run misfire monitor', 10), ('Road test vehicle', 15), ('Rescan for diagnostic trouble codes', 10)], 'brake pad replacement': [('Inspect brake system', 10), ('Measure brake pad thickness', 10), ('Measure brake rotor condition', 10), ('Lift vehicle', 10), ('Remove wheel', 8), ('Remove brake caliper', 15), ('Remove old brake pads', 10), ('Inspect caliper and slide pins', 10), ('Service caliper slide pins', 10), ('Retract caliper piston', 10), ('Replace or machine brake rotor if required', 45), ('Install new brake pads', 10), ('Reinstall brake caliper', 15), ('Reinstall wheel', 8), ('Torque lug nuts', 5), ('Pump brake pedal', 3), ('Check brake fluid level', 10), ('Bed in brake pads', 20), ('Road test brakes', 15)], 'transmission slipping': [('Confirm transmission slipping symptom', 10), ('Scan engine and transmission codes', 10), ('Check transmission fluid level', 10), ('Inspect transmission fluid condition', 10), ('Check transmission for leaks', 10), ('Inspect shift linkage and electronic controls', 10), ('Review live transmission data', 20), ('Perform transmission pressure tests if required', 30), ('Inspect transmission solenoids and valve body', 10), ('Determine internal or external transmission fault', 30), ('Repair or replace failed transmission component', 240), ('Refill correct transmission fluid', 20), ('Perform transmission adaptation or relearn', 30), ('Road test vehicle', 15), ('Recheck transmission fluid and codes', 10)], 'steady check engine light': [('Scan diagnostic trouble codes', 10), ('Record freeze-frame data', 5), ('Inspect wiring, connectors, and vacuum lines', 10), ('Test system identified by diagnostic code', 30), ('Determine whether fault is current or intermittent', 15), ('Repair root cause', 60), ('Clear diagnostic trouble codes', 5), ('Complete required drive cycle', 30), ('Verify emissions monitors', 10), ('Rescan for diagnostic trouble codes', 10)], 'wheel alignment': [('Check tire pressure', 10), ('Inspect tire wear', 10), ('Inspect wheel condition', 10), ('Inspect steering components', 10), ('Inspect suspension components', 10), ('Check vehicle ride height', 10), ('Replace worn steering or suspension components if required', 120), ('Mount alignment sensors', 15), ('Measure caster, camber, and toe', 15), ('Adjust rear alignment if applicable', 20), ('Adjust front alignment', 20), ('Center steering wheel', 10), ('Record final alignment measurements', 10), ('Road test vehicle', 15)], 'oil change': [('Confirm engine oil specification and capacity', 10), ('Warm engine slightly', 5), ('Lift or secure vehicle', 10), ('Remove oil drain plug', 5), ('Drain old engine oil', 10), ('Replace drain plug washer if required', 10), ('Reinstall and torque drain plug', 5), ('Remove old oil filter', 5), ('Install new oil filter', 5), ('Add new engine oil', 5), ('Start engine', 2), ('Verify oil pressure warning turns off', 10), ('Check for oil leaks', 10), ('Shut engine off', 2), ('Recheck engine oil level', 10), ('Reset maintenance reminder', 3)], 'tire rotation': [('Inspect tires', 10), ('Check tire tread depth', 10), ('Check tire pressure', 10), ('Determine correct tire rotation pattern', 10), ('Lift vehicle', 10), ('Remove wheels', 15), ('Move wheels to assigned positions', 10), ('Inspect brakes while wheels are removed', 10), ('Reinstall wheels', 15), ('Torque lug nuts', 5), ('Adjust tire pressures', 5), ('Reset or relearn TPMS if required', 15), ('Road test vehicle', 15)], 'air filter replacement': [('Identify correct engine air filter', 10), ('Open air filter housing', 5), ('Remove old air filter', 5), ('Inspect air filter housing and intake duct', 10), ('Clean loose debris from housing', 5), ('Install new air filter in correct orientation', 5), ('Close and secure air filter housing', 5), ('Inspect intake connections', 10), ('Start engine', 2), ('Verify normal engine operation', 10)], 'ac repair': [('Confirm air conditioning complaint', 10), ('Inspect drive belt and compressor operation', 10), ('Check blower motor operation', 10), ('Scan HVAC control module if applicable', 10), ('Measure vent temperature', 10), ('Check refrigerant system pressures', 15), ('Leak-test air conditioning system', 25), ('Recover refrigerant using approved equipment', 30), ('Repair leaking or failed component', 120), ('Replace receiver-drier or accumulator if required', 60), ('Evacuate air conditioning system', 30), ('Verify system vacuum holds', 15), ('Recharge correct amount of refrigerant', 20), ('Add correct compressor oil if required', 10), ('Test vent temperature and system pressures', 20), ('Perform final refrigerant leak check', 10)], 'cosmetic': [('Inspect and photograph cosmetic damage', 10), ('Identify affected panels and trim', 10), ('Estimate required labor and materials', 20), ('Remove damaged trim or panel if required', 30), ('Repair dents, scratches, or cracks', 90), ('Sand damaged area', 30), ('Apply body filler if required', 30), ('Sand and shape repaired area', 30), ('Apply primer', 25), ('Match paint color', 20), ('Apply base coat', 30), ('Apply clear coat', 30), ('Cure paint', 120), ('Polish and blend repaired area', 45), ('Reinstall trim or panels', 30), ('Perform final quality inspection', 10)]}
#states that the graph is directed, instructions point to another in order
repair_graph = Graph(directed=True)

#creates the graph structure with current repairflows and steps. (would be replaced with database)
def build_repair_graph():
    for service_name, procedures in REPAIR_WORKFLOWS.items():
        for index in range(len(procedures) - 1):
            current_step, _ = procedures[index]
            next_step, next_minutes = procedures[index + 1]

            repair_graph.add_edge(
                f"{service_name}: {current_step}",
                f"{service_name}: {next_step}",
                next_minutes,
            )


build_repair_graph()


# -----------------------------------------------------------------------
# Request models
# describes json structure that fastAPI expects from the frontend - type checking convert json to python obj etc.
# -----------------------------------------------------------------------

#meains appointment must contain ONE field, string 
class AppointmentRequest(BaseModel):
    appointment: str


class PartRequest(BaseModel):
    item_num: int
    item: str


class PriorityRepairRequest(BaseModel):
    name: str
    vehicle: str
    service: str
    is_drivable: bool
    is_activeleak: bool


class RepairLogRequest(BaseModel):
    month: int
    day: int
    year: int
    repair: str


class InsertRepairLogRequest(RepairLogRequest):
    index: int


class RAGQueryRequest(BaseModel):
    question: str
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

#would be replaced with database
SERVICE_URGENCY = {
    "fuel leak": 100,
    "complete brake failure": 99,
    "engine overheating": 98,
    "tire sidewall bulge": 97,
    "flashing check engine light": 95,
    "transmission slipping": 88,
    "brake pad replacement": 75,
    "steady check engine light": 65,
    "wheel alignment": 45,
    "oil change": 35,
    "tire rotation": 30,
    "air filter replacement": 25,
    "ac repair": 25,
    "cosmetic": 5,
}


# -----------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------

# creates fastAPI app object 
# uvicorn main:app <- file , api app
app = FastAPI(
    title="VSPMS API",
    description=(
        "Vehicle service, parts inventory, repair workflows, "
        "and vehicle-manual RAG"
    ),
    version="1.0.0",
)

# CORS - Cross origin resource sharing middleware
# controls whether one app is allowed to send request to another at a different origin
# allows origins 8501 and 8000 to connect to fastAPI
#allow credentials allows cookies auth info etc.
#allow methods allows get post put delete etc.abs
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#creates route for (health) and groups the route in fastAPIs doc page
#used to confirm backend is online
@app.get("/api/health", tags=["System"])
def health():
    return {
        "status": "running",
        "service": "VSPMS API",
    }

#creates route, has state lock on functions shown on the dashboard
@app.get("/api/dashboard", tags=["System"])
def dashboard():
    with state_lock:
        return {
            "appointments": len(appointments),
            "parts": len(parts_hashmap),
            "priority_repairs": len(priority_repairs),
            "repair_logs": len(repair_logs),
        }


# -----------------------------------------------------------------------
# Appointments: Queue + Stacks
# -----------------------------------------------------------------------


#shows summary of current appointment system
def appointment_snapshot():
    return {
        "appointments": get_appointment_values(),
        "queue_size": len(appointments),
        "undo_count": len(appointment_undo),
        "redo_count": len(appointment_redo),
    }

#route initialized get
@app.get("/api/appointments", tags=["Appointments"])
def show_appointments():
    with state_lock:
        return appointment_snapshot()

#route init post
@app.post("/api/appointments/add", tags=["Appointments"])
#function has appointment request as the payload
def add_appointment(payload: AppointmentRequest):
    clean_appointment = payload.appointment.strip()
    #removes whitespace from beginning and end 

    #checks if string is empty
    if not clean_appointment:
        raise HTTPException(
            status_code=400,
            detail="Appointment is required",
        )

    with state_lock:
        appointments.enqueue(clean_appointment)
        appointment_undo.push(
            ("add", clean_appointment)
        )
        clear_stack(appointment_redo)
        return appointment_snapshot()


@app.post("/api/appointments/process", tags=["Appointments"])
def process_appointment():
    with state_lock:
        if appointments.is_empty():
            raise HTTPException(
                status_code=400,
                detail="No appointments to process",
            )

        appointment = appointments.dequeue()
        appointment_undo.push(
            ("process", appointment)
        )
        clear_stack(appointment_redo)

        result = appointment_snapshot()
        result["processed"] = appointment
        return result


@app.post("/api/appointments/undo", tags=["Appointments"])
def undo_appointment():
    with state_lock:
        if appointment_undo.is_empty():
            raise HTTPException(
                status_code=400,
                detail="Nothing to undo",
            )

        action, appointment = appointment_undo.pop()

        if action == "add":
            appointments.dequeue_rear()
        elif action == "process":
            appointments.enqueue_front(appointment)

        appointment_redo.push(
            (action, appointment)
        )
        return appointment_snapshot()


@app.post("/api/appointments/redo", tags=["Appointments"])
def redo_appointment():
    with state_lock:
        if appointment_redo.is_empty():
            raise HTTPException(
                status_code=400,
                detail="Nothing to redo",
            )

        action, appointment = appointment_redo.pop()

        if action == "add":
            appointments.enqueue(appointment)
        elif action == "process":
            if appointments.is_empty():
                raise HTTPException(
                    status_code=400,
                    detail="No appointment is available to process",
                )
            appointments.dequeue()

        appointment_undo.push(
            (action, appointment)
        )
        return appointment_snapshot()


# -----------------------------------------------------------------------
# Parts inventory: HashMap + BinarySearchTree
# -----------------------------------------------------------------------

@app.post("/api/parts", tags=["Parts Inventory"])
def add_part(payload: PartRequest):
    clean_item = payload.item.strip()

    if not clean_item:
        raise HTTPException(
            status_code=400,
            detail="Part name is required",
        )

    with state_lock:
        #Use the HashMap to check whether the exact part number exists
        if payload.item_num in parts_hashmap:
            raise HTTPException(
                status_code=400,
                detail="That part number already exists",
            )

        #Store the same part in both structures
        #HashMap is used for exact lookup
        parts_hashmap.put(
            payload.item_num,
            clean_item,
        )

        #BinarySearchTree is used for ordered traversal
        parts_tree.insert(
            payload.item_num,
            clean_item,
        )

        return {
            "item_num": payload.item_num,
            "item": clean_item,
        }


@app.get("/api/parts", tags=["Parts Inventory"])
def show_parts(
    order: str = Query(default="inorder")
):
    normalized = order.strip().lower()

    with state_lock:
        #Display the HashMap entries
        if normalized == "hashmap":
            items = parts_hashmap.items()

        #Use the existing BST traverse method
        elif normalized in {
            "inorder",
            "preorder",
            "postorder",
        }:
            items = list(
                parts_tree.traverse(normalized)
            )

        #The BST __iter__ method already performs inorder traversal
        elif normalized == "showall":
            items = list(parts_tree)

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid display order",
            )

        return {
            "order": normalized,
            "items": [
                {
                    "item_num": key,
                    "item": value,
                }
                for key, value in items
            ],
            "count": len(parts_hashmap),
        }


@app.get(
    "/api/parts/range/{minimum_item_num}/{maximum_item_num}",
    tags=["Parts Inventory"],
)
def parts_in_range(
    minimum_item_num: int,
    maximum_item_num: int,
):
    if minimum_item_num > maximum_item_num:
        raise HTTPException(
            status_code=400,
            detail=(
                "Minimum part number cannot be greater "
                "than maximum part number"
            ),
        )

    with state_lock:
        #The existing BST does not have a range_search method.
        #Use its existing inorder traversal, then filter the sorted results.
        sorted_parts = list(
            parts_tree.traverse("inorder")
        )

        matching_parts = [
            {
                "item_num": key,
                "item": value,
            }
            for key, value in sorted_parts
            if minimum_item_num <= key <= maximum_item_num
        ]

        return {
            "minimum": minimum_item_num,
            "maximum": maximum_item_num,
            "items": matching_parts,
            "count": len(matching_parts),
        }


@app.get(
    "/api/parts/{item_num}",
    tags=["Parts Inventory"],
)
def search_part(item_num: int):
    with state_lock:
        #Use the HashMap for fast exact lookup by part number
        try:
            item = parts_hashmap.get(item_num)

        except KeyError as exc:
            raise HTTPException(
                status_code=404,
                detail="Part not found",
            ) from exc

        return {
            "item_num": item_num,
            "item": item,
        }


@app.delete(
    "/api/parts/{item_num}",
    tags=["Parts Inventory"],
)
def delete_part(item_num: int):
    with state_lock:
        if item_num not in parts_hashmap:
            raise HTTPException(
                status_code=404,
                detail="Part not found",
            )

        item = parts_hashmap.get(item_num)

        #Remove the same part from both structures
        parts_hashmap.remove(item_num)
        parts_tree.delete(item_num)

        return {
            "item_num": item_num,
            "item": item,
        }


# -----------------------------------------------------------------------
# Priority repairs: MaxHeap
# -----------------------------------------------------------------------

@app.get(
    "/api/priority-repairs/services",
    tags=["Priority Repairs"],
)
def priority_services():
    return {
        "services": list(SERVICE_URGENCY)
    }


@app.get(
    "/api/priority-repairs",
    tags=["Priority Repairs"],
)
def show_priority_repairs():
    with state_lock:
        return {
            "repairs": [
                {
                    "priority": priority,
                    **request,
                }
                for priority, request
                in get_ordered_priority_repairs()
            ]
        }


@app.post(
    "/api/priority-repairs",
    tags=["Priority Repairs"],
)
def add_priority_repair(
    payload: PriorityRepairRequest
):
    name = payload.name.strip()
    vehicle = payload.vehicle.strip()
    service = (
        payload.service
        .strip()
        .lower()
        .replace("_", " ")
    )

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Customer name is required",
        )

    if not vehicle:
        raise HTTPException(
            status_code=400,
            detail="Vehicle is required",
        )

    if service not in SERVICE_URGENCY:
        raise HTTPException(
            status_code=400,
            detail="Service not found",
        )

    priority = SERVICE_URGENCY[service]

    if not payload.is_drivable:
        priority += 25

    if payload.is_activeleak:
        priority += 25

    request = {
        "name": name,
        "vehicle": vehicle,
        "service": service,
        "is_drivable": payload.is_drivable,
        "is_activeleak": payload.is_activeleak,
    }

    with state_lock:
        priority_repairs.insert(
            priority,
            request,
        )

    return {
        "priority": priority,
        **request,
    }


@app.get(
    "/api/priority-repairs/next",
    tags=["Priority Repairs"],
)
def peek_priority_repair():
    with state_lock:
        try:
            priority, request = (
                priority_repairs.peek_max()
            )
        except IndexError as exc:
            raise HTTPException(
                status_code=404,
                detail=str(exc),
            ) from exc

        return {
            "priority": priority,
            **request,
        }


@app.post(
    "/api/priority-repairs/process",
    tags=["Priority Repairs"],
)
def process_priority_repair():
    with state_lock:
        try:
            priority, request = (
                priority_repairs.extract_max()
            )
        except IndexError as exc:
            raise HTTPException(
                status_code=404,
                detail=str(exc),
            ) from exc

        return {
            "priority": priority,
            **request,
        }


# -----------------------------------------------------------------------
# Repair logs: Doubly linked list
# -----------------------------------------------------------------------

def validate_repair_log(
    month,
    day,
    year,
    repair,
):
    import datetime

    try:
        repair_date = datetime.date(
            year,
            month,
            day,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid repair date: {exc}",
        ) from exc

    clean_repair = repair.strip()

    if not clean_repair:
        raise HTTPException(
            status_code=400,
            detail="Repair description is required",
        )

    return {
        "date": repair_date.isoformat(),
        "month": month,
        "day": day,
        "year": year,
        "repair": clean_repair,
    }


@app.get("/api/repair-logs", tags=["Repair Logs"])
def show_repair_logs():
    with state_lock:
        return {
            "logs": get_repair_log_values()
        }


@app.post("/api/repair-logs", tags=["Repair Logs"])
def add_repair_log(payload: RepairLogRequest):
    log = validate_repair_log(
        payload.month,
        payload.day,
        payload.year,
        payload.repair,
    )

    with state_lock:
        repair_logs.append(log)

    return log


@app.post(
    "/api/repair-logs/insert",
    tags=["Repair Logs"],
)
def insert_repair_log(
    payload: InsertRepairLogRequest
):
    log = validate_repair_log(
        payload.month,
        payload.day,
        payload.year,
        payload.repair,
    )

    with state_lock:
        try:
            repair_logs.insert(
                log,
                payload.index,
            )
        except IndexError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

    return log


@app.delete(
    "/api/repair-logs/{index}",
    tags=["Repair Logs"],
)
def delete_repair_log(index: int):
    with state_lock:
        try:
            removed_log = remove_repair_log_at_index(index)

        except IndexError as exc:
            raise HTTPException(
                status_code=404,
                detail="Repair log not found",
            ) from exc

        return removed_log


# -----------------------------------------------------------------------
# Repair process: Graph
# -----------------------------------------------------------------------

@app.get(
    "/api/repair-process",
    tags=["Repair Process"],
)
def repair_process_services():
    return {
        "services": list(REPAIR_WORKFLOWS)
    }


@app.get(
    "/api/repair-process/{service_name}",
    tags=["Repair Process"],
)
def get_repair_process(service_name: str):
    normalized = (
        service_name
        .strip()
        .lower()
        .replace("_", " ")
    )

    if normalized not in REPAIR_WORKFLOWS:
        raise HTTPException(
            status_code=404,
            detail="Service does not exist",
        )

    procedures = REPAIR_WORKFLOWS[normalized]
    total_minutes = sum(
        minutes
        for _, minutes in procedures
    )

    first_node = (
        f"{normalized}: {procedures[0][0]}"
    )

    return {
        "service": normalized,
        "steps": [
            {
                "step_number": index + 1,
                "step": step,
                "minutes": minutes,
                "graph_node": (
                    f"{normalized}: {step}"
                ),
            }
            for index, (step, minutes)
            in enumerate(procedures)
        ],
        "total_minutes": total_minutes,
        "hours": total_minutes // 60,
        "remaining_minutes": total_minutes % 60,
        "bfs_order": repair_graph.bfs(first_node),
        "dfs_order": repair_graph.dfs(first_node),
    }


# -----------------------------------------------------------------------
# RAG
# -----------------------------------------------------------------------

#this route sends question to RAG system 
@app.post("/api/rag/query", tags=["RAG"])
def ask_manual(payload: RAGQueryRequest):
    try:
        return query_manual(
            payload.question,
            payload.top_k,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"RAG query failed: {exc}",
        ) from exc


UPLOAD_DIR = (
    Path(__file__).resolve().parent
    / "rag_ai"
    / "uploads"
)
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@app.post("/api/rag/upload", tags=["RAG"])
async def upload_manual(
    file: UploadFile = File(...)
):
    filename = Path(
        file.filename or "manual.pdf"
    ).name

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted",
        )

    destination = UPLOAD_DIR / filename

    with destination.open("wb") as output:
        shutil.copyfileobj(
            file.file,
            output,
        )

    event_ids = await inngest_client.send(
        inngest.Event(
            name="rag/ingest_pdf",
            data={
                "pdf_path": str(
                    destination.resolve()
                ),
                "source_id": filename,
            },
        )
    )

    return {
        "message": (
            "PDF uploaded and ingestion was triggered"
        ),
        "filename": filename,
        "event_ids": event_ids,
    }

# connects inngest workflows to existing fastAPI
inngest.fast_api.serve(
    app,
    inngest_client,
    [
        rag_ingest_pdf,
        rag_query_pdf_ai,
    ],
)
