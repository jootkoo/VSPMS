# Vehicle Service and Parts Management System

The Vehicle Service and Parts Management System, or **VSPMS**, is a Python-based application that combines custom data-structure implementations with a Retrieval-Augmented Generation system.

The application is designed to manage vehicles, parts, repair requests, technicians, appointments, and repair procedures while also allowing users to upload vehicle manuals and ask questions about their contents.

The project demonstrates:

- Practical implementation of core data structures
- Object-oriented programming
- REST API development
- Background workflow processing
- PDF ingestion and text chunking
- OpenAI embeddings and language-model integration
- Vector similarity search
- Docker containerization
- A planned Streamlit user interface

---

## Project Goals

The main goals of VSPMS are to:

1. Demonstrate how data structures can solve real vehicle-service management problems.
2. Create a working vehicle and parts management application.
3. Build a RAG assistant that answers questions using uploaded vehicle manuals.
4. Keep AI responses grounded in retrieved manual content rather than relying only on general model knowledge.
5. Eventually provide the entire system through a Streamlit web interface.

---

# Core System
- Custom data-structure classes
- Vehicle repair workflow
- Parts inventory using a BST
- Exact part lookup using a hash map
- Appointment queue
- Undo and redo stacks
- Priority-based service-request processing
- PDF loading
- PDF chunking
- Batched OpenAI embeddings
- Qdrant vector storage
- Batched Qdrant uploads
- Inngest ingestion workflow
- FastAPI backend setup
- Semantic document search

---

## Data Structures

The project uses custom implementations of the following data structures.

### Hash Map

Used for fast exact-key lookup.

Examples:

- Find a vehicle by VIN
- Find a part by part number
- Retrieve technician information by technician ID

---

### Queue

Used to process regular appointments in first-in, first-out order.

```text
First appointment scheduled
        ↓
First appointment processed
```

The queue can also support operations at both ends when restoring appointments through undo and redo actions.

---

### Priority Queue / Max Heap

Used to process urgent repair requests before routine maintenance requests.

Example priorities:

```text
Fuel leak                  → Highest priority
Complete brake failure     → Critical priority
Engine overheating         → High priority
Oil change                 → Routine priority
Cosmetic repair            → Low priority
```

The service request with the highest urgency is processed first.

---

### Stack

Used to implement undo and redo functionality.

```text
New action → Undo stack
Undo action → Redo stack
Redo action → Undo stack
```


### Linked List

Used to represent repair workflows in which steps can be inserted, removed, or reordered.

Example:

```text
Diagnose problem
    ↓
Inspect components
    ↓
Replace damaged part
    ↓
Test repair
    ↓
Complete service
```

A linked list makes it possible to change the repair process without shifting every remaining step.

---

### Binary Search Tree
Used to maintain parts in sorted order by part number.

The tree supports:

- Adding parts
- Searching by part number
- Deleting parts
- In-order traversal
- Pre-order traversal
- Post-order traversal
- Finding minimum and maximum part numbers
- Finding parts within a part-number range

Example sorted output:

```text
P100
P205
P350
P700
```

The binary search tree and hash map can reference the same part records:
```text
Hash Map → Fast exact lookup
BST      → Sorted and range-based access
```

---

### Graph

Used to represent connected relationships within the service system.

Possible uses include:

- Dependencies between repair procedures
- Relationships between vehicle systems
- Routes between service-shop locations
- Required ordering of repair tasks
- Compatible parts and vehicle configurations

Example dependency:

```text
Disconnect battery
        ↓
Remove electrical component
        ↓
Install replacement
        ↓
Reconnect battery
        ↓
Run diagnostic test
```

---

# Retrieval-Augmented Generation

VSPMS includes a RAG system that allows users to upload vehicle manuals and ask document-specific questions.

Example:

```text
How does electric power steering work?

What oil specification does this engine require?

How do I release the electric parking brake?

What is the recommended maintenance interval?
```

Instead of asking the language model to answer only from its general knowledge, the application retrieves relevant sections from the uploaded vehicle manual first.

---

## RAG Workflow
```text
Vehicle manual PDF
        ↓
Extract page text
        ↓
Split text into chunks
        ↓
Generate embedding vectors
        ↓
Store vectors and payloads in Qdrant
        ↓
Embed the user's question
        ↓
Retrieve the most relevant manual chunks
        ↓
Send the question and retrieved context to the language model
        ↓
Return a grounded answer with sources
```

---
# Planned Project Structure

```text
VSPMS/
│
├── main.py
├── ragAI.py
├── data_loader.py
├── vector_db.py
├── custom_types.py
├── streamlit_app.py
│
├── data_structures/
│   ├── stack.py
│   ├── queue.py
│   ├── hash_map.py
│   ├── binary_search_tree.py
│   ├── max_heap.py
│   ├── linked_list.py
│   └── graph.py
│
├── models/
│   ├── vehicle.py
│   ├── part.py
│   ├── technician.py
│   └── service_request.py
│
├── manuals/
├── qdrant_storage/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 3. Install dependencies

Dependencies include:

```text
fastapi
uvicorn
streamlit
openai
python-dotenv
qdrant-client
llama-index
llama-index-readers-file
pydantic
inngest
requests
python-multipart
```

---

# Running the Application

The complete application requires several services.

## 1. Start Docker Desktop

Make sure Docker Desktop is running before starting Qdrant.

## 2. Start Qdrant

```powershell
docker run -d `
  --name qdrant `
  -p 6333:6333 `
  -v "${PWD}/qdrant_storage:/qdrant/storage" `
  qdrant/qdrant
```

If the container already exists:

```powershell
docker start qdrant
```

Verify it:

```powershell
docker ps
```

Qdrant dashboard:

```text
http://localhost:6333/dashboard
```

## 3. Start FastAPI

Open a new terminal:

```powershell
uvicorn ragAI:app 
```

## 4. Start Inngest

Open another terminal:

```powershell
npx inngest-cli@latest dev `
  -u http://127.0.0.1:8000/api/inngest `
  --no-discovery
```

## 5. Start Streamlit

Open another terminal:

```powershell
streamlit run streamlit_app.py
```

Streamlit should open at:

```text
http://localhost:8501
```

---