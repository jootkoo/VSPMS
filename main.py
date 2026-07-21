from serviceLog import dLinkedList
from priorityRepairs import maxHeap

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
        




    pRepairs()
    current_log = repairWorkflow()
    repairWorkflowLog.append(current_log)

    print(repairWorkflowLog)



    print(vehicle1.model)
