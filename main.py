from serviceLog import dLinkedList
from priorityRepairs import maxHeap
from repairProcess import Graph
from appointments import Stack


class Vehicle:
    def __init__(self, vin, make, model, year):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year

if __name__ == '__main__':
    repairWorkflowLog = dLinkedList()

    vehicle1 = Vehicle(
        "1FTFW1E50MFA12345",
        "Ford",
        "F-150",
        2021
    )

    def repairWorkflow():
        log = []
        print("REPAIR WORKFLOW")
        month = int(input("Enter month :"))
        if (month > 12) or (month < 1):
            month = int(input("Invalid input, Please input valid month :"))
        log.append(month)
        day = int(input("Enter day :"))
        if (day > 31) or (day< 1):
            day = int(input("Invalid input, Please input valid day :"))
        log.append(day)
        year = int(input("Enter year :"))
        if (year < 1):
            year = int(input("Invalid input, Please input valid year :"))
        log.append(year)
        repair = str(input("Enter in repair to be logged :"))
        log.append(repair)
        return log

    def pRepairs():
        SERVICE_URGENCY = {
            "fuel leak": 100,
            "complete brake failure": 99,
            "engine overheating": 98,
            "tire sidewall_bulge": 97,
            "flashing check engine light": 95,
            "brake pad replacement": 75,
            "transmission slipping": 88,
            "steady check engine light": 65,
            "wheel alignment": 45,
            "oil change": 35,
            "tire rotation": 30,
            "air filter replacement": 25,
            "ac repair": 25,
            "cosmetic": 5,
        }

        priority = 0
        queue = maxHeap()

        #UI
        print("SERVICE LOG")
        name = str(input("Enter in name :"))
        vehicle = str(input("Enter vehicle :"))
        print("SERVICES:")
        for key in SERVICE_URGENCY:
            print(key)
        #Service
        while True:
            service = input("Enter service: ").strip().lower()
            if service in SERVICE_URGENCY:
                break
            print("Service not found. Please choose from the list.")
        priority += SERVICE_URGENCY[service]
        #Drivability
        while True:
            drivable = input("Is the vehicle drivable? (yes/no): ").strip().lower()
            if drivable == "yes":
                is_drivable = True
                break
            elif drivable == "no":
                is_drivable = False
                priority += 25
                break
            else:
                print("Please enter yes or no.")
        #Active Leak
        while True:
            activeleak = input("Does this vehicle have an active leak? (yes/no): ").strip().lower()
            if activeleak == "yes":
                is_activeleak = True
                priority += 25
                break
            elif activeleak == "no":
                is_activeleak = False
                break
            else:
                print("Please enter yes or no.")


        requests = {
            "name": name,
            "service": service,
            "is_drivable": is_drivable,
            "is_activeleak": is_activeleak
        }
        
        queue.insert(priority, requests)

        print(queue)
         
    def RepairProcess():
        

        repair_workflows = {
            "fuel leak": [
                ("Confirm fuel leak", 10),
                ("Shut vehicle off and isolate ignition sources", 2),
                ("Identify fuel type and leak location", 10),
                ("Relieve fuel-system pressure", 15),
                ("Inspect fuel lines, hoses, tank, rail, injectors, and seals", 10),
                ("Replace damaged component", 90),
                ("Reconnect fuel system", 20),
                ("Pressurize fuel system", 10),
                ("Check for additional leaks", 10),
                ("Clear related diagnostic codes", 5),
                ("Road test and recheck", 15),
            ],

            "complete brake failure": [
                ("Do not drive vehicle", 2),
                ("Tow vehicle into service bay", 30),
                ("Inspect brake fluid level", 10),
                ("Check for external brake fluid leaks", 10),
                ("Inspect master cylinder", 10),
                ("Inspect brake lines and hoses", 10),
                ("Inspect calipers and wheel cylinders", 10),
                ("Inspect brake booster and pedal linkage", 10),
                ("Repair failed brake component", 90),
                ("Refill brake fluid", 5),
                ("Bleed brake system", 30),
                ("Verify brake pedal pressure", 10),
                ("Perform low-speed brake test", 10),
                ("Perform final leak inspection", 10),
            ],

            "engine overheating": [
                ("Allow engine to cool", 30),
                ("Check coolant level", 10),
                ("Inspect for coolant leaks", 10),
                ("Pressure-test cooling system", 30),
                ("Inspect radiator", 10),
                ("Inspect cooling system hoses and reservoir", 10),
                ("Test radiator fan", 20),
                ("Test thermostat", 20),
                ("Test water pump", 20),
                ("Check radiator cap", 10),
                ("Check for combustion gases in coolant", 20),
                ("Repair failed cooling system component", 90),
                ("Refill and bleed cooling system", 30),
                ("Run engine to operating temperature", 15),
                ("Verify engine temperature stability", 10),
                ("Road test vehicle", 15),
            ],

            "tire sidewall bulge": [
                ("Do not drive vehicle at high speed", 2),
                ("Inspect damaged tire", 10),
                ("Confirm tire sidewall damage", 10),
                ("Inspect wheel for impact damage", 10),
                ("Remove wheel", 8),
                ("Remove damaged tire", 10),
                ("Inspect valve stem or TPMS sensor", 10),
                ("Mount replacement tire", 15),
                ("Balance wheel", 10),
                ("Reinstall wheel", 8),
                ("Torque lug nuts", 5),
                ("Set tire pressure", 5),
                ("Verify TPMS operation", 10),
            ],

            "flashing check engine light": [
                ("Reduce engine load and stop driving if engine is shaking", 2),
                ("Scan diagnostic trouble codes", 10),
                ("Record freeze-frame data", 5),
                ("Inspect for active engine misfire", 10),
                ("Inspect ignition coils", 10),
                ("Inspect spark plugs", 10),
                ("Inspect fuel injectors", 10),
                ("Check fuel pressure", 10),
                ("Check engine compression if required", 45),
                ("Repair cause of engine misfire", 60),
                ("Clear diagnostic trouble codes", 5),
                ("Run misfire monitor", 10),
                ("Road test vehicle", 15),
                ("Rescan for diagnostic trouble codes", 10),
            ],

            "brake pad replacement": [
                ("Inspect brake system", 10),
                ("Measure brake pad thickness", 10),
                ("Measure brake rotor condition", 10),
                ("Lift vehicle", 10),
                ("Remove wheel", 8),
                ("Remove brake caliper", 15),
                ("Remove old brake pads", 10),
                ("Inspect caliper and slide pins", 10),
                ("Service caliper slide pins", 10),
                ("Retract caliper piston", 10),
                ("Replace or machine brake rotor if required", 45),
                ("Install new brake pads", 10),
                ("Reinstall brake caliper", 15),
                ("Reinstall wheel", 8),
                ("Torque lug nuts", 5),
                ("Pump brake pedal", 3),
                ("Check brake fluid level", 10),
                ("Bed in brake pads", 20),
                ("Road test brakes", 15),
            ],

            "transmission slipping": [
                ("Confirm transmission slipping symptom", 10),
                ("Scan engine and transmission codes", 10),
                ("Check transmission fluid level", 10),
                ("Inspect transmission fluid condition", 10),
                ("Check transmission for leaks", 10),
                ("Inspect shift linkage and electronic controls", 10),
                ("Review live transmission data", 20),
                ("Perform transmission pressure tests if required", 30),
                ("Inspect transmission solenoids and valve body", 10),
                ("Determine internal or external transmission fault", 30),
                ("Repair or replace failed transmission component", 240),
                ("Refill correct transmission fluid", 20),
                ("Perform transmission adaptation or relearn", 30),
                ("Road test vehicle", 15),
                ("Recheck transmission fluid and codes", 10),
            ],

            "steady check engine light": [
                ("Scan diagnostic trouble codes", 10),
                ("Record freeze-frame data", 5),
                ("Inspect wiring, connectors, and vacuum lines", 10),
                ("Test system identified by diagnostic code", 30),
                ("Determine whether fault is current or intermittent", 15),
                ("Repair root cause", 60),
                ("Clear diagnostic trouble codes", 5),
                ("Complete required drive cycle", 30),
                ("Verify emissions monitors", 10),
                ("Rescan for diagnostic trouble codes", 10),
            ],

            "wheel alignment": [
                ("Check tire pressure", 10),
                ("Inspect tire wear", 10),
                ("Inspect wheel condition", 10),
                ("Inspect steering components", 10),
                ("Inspect suspension components", 10),
                ("Check vehicle ride height", 10),
                ("Replace worn steering or suspension components if required", 120),
                ("Mount alignment sensors", 15),
                ("Measure caster, camber, and toe", 15),
                ("Adjust rear alignment if applicable", 20),
                ("Adjust front alignment", 20),
                ("Center steering wheel", 10),
                ("Record final alignment measurements", 10),
                ("Road test vehicle", 15),
            ],

            "oil change": [
                ("Confirm engine oil specification and capacity", 10),
                ("Warm engine slightly", 5),
                ("Lift or secure vehicle", 10),
                ("Remove oil drain plug", 5),
                ("Drain old engine oil", 10),
                ("Replace drain plug washer if required", 10),
                ("Reinstall and torque drain plug", 5),
                ("Remove old oil filter", 5),
                ("Install new oil filter", 5),
                ("Add new engine oil", 5),
                ("Start engine", 2),
                ("Verify oil pressure warning turns off", 10),
                ("Check for oil leaks", 10),
                ("Shut engine off", 2),
                ("Recheck engine oil level", 10),
                ("Reset maintenance reminder", 3),
            ],

            "tire rotation": [
                ("Inspect tires", 10),
                ("Check tire tread depth", 10),
                ("Check tire pressure", 10),
                ("Determine correct tire rotation pattern", 10),
                ("Lift vehicle", 10),
                ("Remove wheels", 15),
                ("Move wheels to assigned positions", 10),
                ("Inspect brakes while wheels are removed", 10),
                ("Reinstall wheels", 15),
                ("Torque lug nuts", 5),
                ("Adjust tire pressures", 5),
                ("Reset or relearn TPMS if required", 15),
                ("Road test vehicle", 15),
            ],

            "air filter replacement": [
                ("Identify correct engine air filter", 10),
                ("Open air filter housing", 5),
                ("Remove old air filter", 5),
                ("Inspect air filter housing and intake duct", 10),
                ("Clean loose debris from housing", 5),
                ("Install new air filter in correct orientation", 5),
                ("Close and secure air filter housing", 5),
                ("Inspect intake connections", 10),
                ("Start engine", 2),
                ("Verify normal engine operation", 10),
            ],

            "ac repair": [
                ("Confirm air conditioning complaint", 10),
                ("Inspect drive belt and compressor operation", 10),
                ("Check blower motor operation", 10),
                ("Scan HVAC control module if applicable", 10),
                ("Measure vent temperature", 10),
                ("Check refrigerant system pressures", 15),
                ("Leak-test air conditioning system", 25),
                ("Recover refrigerant using approved equipment", 30),
                ("Repair leaking or failed component", 120),
                ("Replace receiver-drier or accumulator if required", 60),
                ("Evacuate air conditioning system", 30),
                ("Verify system vacuum holds", 15),
                ("Recharge correct amount of refrigerant", 20),
                ("Add correct compressor oil if required", 10),
                ("Test vent temperature and system pressures", 20),
                ("Perform final refrigerant leak check", 10),
            ],

            "cosmetic": [
                ("Inspect and photograph cosmetic damage", 10),
                ("Identify affected panels and trim", 10),
                ("Estimate required labor and materials", 20),
                ("Remove damaged trim or panel if required", 30),
                ("Repair dents, scratches, or cracks", 90),
                ("Sand damaged area", 30),
                ("Apply body filler if required", 30),
                ("Sand and shape repaired area", 30),
                ("Apply primer", 25),
                ("Match paint color", 20),
                ("Apply base coat", 30),
                ("Apply clear coat", 30),
                ("Cure paint", 120),
                ("Polish and blend repaired area", 45),
                ("Reinstall trim or panels", 30),
                ("Perform final quality inspection", 10),
            ],
        }

        def add_workflow_to_graph(graph, service_name):
            procedures = repair_workflows[service_name]

            for index in range(len(procedures) - 1):
                current_step, current_time = procedures[index]
                next_step, next_time = procedures[index + 1]

                current_node = f"{service_name}: {current_step}"
                next_node = f"{service_name}: {next_step}"

                graph.add_edge(
                    current_node,
                    next_node,
                    next_time
                )

        def add_all_workflows_to_graph(graph):
            for service_name in repair_workflows:
                add_workflow_to_graph(graph, service_name)


        #####################
        SERVICES = [
            "fuel leak",
            "complete brake failure",
            "engine overheating",
            "tire sidewall bulge",
            "flashing check engine light",
            "brake pad replacement",
            "transmission slipping",
            "steady check engine light",
            "wheel alignment",
            "oil change",
            "tire rotation",
            "air filter replacement",
            "ac repair",
            "cosmetic",
        ]
        #declare graph
        g = Graph(directed=True)
        add_all_workflows_to_graph(g)
        print(g)

        for service in SERVICES:
            print(service)
        while True:
            service_name = str(input("Enter in service :"))
            if service_name in SERVICES:
                break
            else:
                print("Service does not exist, please RE-Enter in service")
            

        #starts at 0
        current_index = 0
        #looks through dict and grab the service the user chose
        procedures = repair_workflows[service_name]

        def timeToComplete():
            current_index = 0
            step, minutes = procedures[current_index]
            time = 0

            while current_index < len(procedures):
                time += minutes
                current_index += 1
            print("Total Service Time: ")
            print(f"{time//60} hours and {time % 60} minutes")


        timeToComplete()

        def print_current_step():
            step, minutes = procedures[current_index] #grabs the two perameters in the procedure
        
            print(f"Step {current_index + 1}: {step}")
            print(f"Estimated time: {minutes} minutes")

        #while loop to loop through procedures
        while current_index < len(procedures):
            step, minutes = procedures[current_index] #grabs the two perameters in the procedure

            print(f"\nStep {current_index + 1}: {step}")
            print(f"Estimated time: {minutes} minutes")

            user_input = input(
                "Enter 'next' when complete or 'quit' to stop: ").strip().lower()

            if user_input == "next":
                current_index += 1

            elif user_input == "quit":
                print("Workflow stopped.")
                break

            else:
                print("Invalid input. Enter 'next' or 'quit'.")

        else:
            print(f"\n{service_name.title()} workflow is complete.")

        print(g.bfs("fuel leak"))
        
    def schedule():
        undo_stack = Stack() #initialize the stack
        redo_stack = Stack()
        appointments = []

        while True:
            command = input("add, undo, redo, show, or quit: ").strip().lower()

            if command == "add": #append appointment to stack
                appointment = input("Enter appointment: ")

                appointments.append(appointment)
                undo_stack.push(("add", appointment))

                #new action clears redo history
                redo_stack = Stack()

            elif command == "undo": 
                if undo_stack.is_empty():
                    print("Nothing to undo.")
                    continue
                action, appointment = undo_stack.pop()
                if action == "add":
                    appointments.remove(appointment) #removes recent addition 
                    redo_stack.push((action, appointment)) #adds the recent deletion to the redo stack

            elif command == "redo":
                if redo_stack.is_empty():
                    print("Nothing to redo.") #if empty
                    continue
                action, appointment = redo_stack.pop() #initialize tuple , "action , appointment"
                if action == "add":
                    appointments.append(appointment)
                    undo_stack.push((action, appointment))

            elif command == "show":
                print(appointments)

            elif command == "quit":
                break
            else:
                print("Invalid command.")

    schedule()
    RepairProcess()
    pRepairs()
    current_log = repairWorkflow()
    repairWorkflowLog.append(current_log)

    print(repairWorkflowLog)



    print(vehicle1.model)
