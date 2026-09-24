import json
from datetime import date
import statistics

class Watch:
    def __init__(self, brand, model, ref_no="N/A", serial_no="N/A", movement_type=None, accuracy_day=None, accuracy_month=None, last_reset_date=None):
        self.brand = brand
        self.model = model
        self.ref_no = ref_no
        self.serial_no = serial_no
        self.movement_type = movement_type
        self.accuracy_log = []
        # Tracks the id of the drift logs up until next reset
        self.current_id = 1

        if last_reset_date is not None:
            self.last_reset_date = last_reset_date
        else:
            self.last_reset_date = date.today()
        
        if accuracy_month is not None:
            self.accuracy_sec = accuracy_month / 30
        else:
            self.accuracy_sec = accuracy_day

    # Logging daily drift for watch
    def log_drift(self, drift_sec, as_of=None):
        if as_of is not None:
            check_date = as_of
        else:
            check_date = date.today()

        days_since_reset = (check_date - self.last_reset_date).days
        entry = {
            "run_id": self.current_id,
            "date": check_date.isoformat(),
            "drift_seconds": drift_sec,
            "days_since_reset": days_since_reset
        }
        self.accuracy_log.append(entry)

    # Updates last reset for watch
    def reset(self):
        self.last_reset_date = date.today()
        self.current_id += 1

    # Calculates health score for watch compared to it's rated accuracy spec
    # Note: readings are manually logged so there is room for human erorr in timing
    # treat this as a rough, for fun estimate rather than precise measurement
    # TODO: consider adding a warning if entry is before 24 hours after last entry

    def health_score(self, run_id=None):
        if not run_id:
            run_id = self.current_id

        # Grabs the logs that match the given run_id
        current_logs = [
            entry for entry in self.accuracy_log
            if entry["run_id"] == run_id
        ]

        if len(current_logs) < 2:
            return "Not enough data"

        rates = [
            entry["drift_seconds"] / entry["days_since_reset"]
            for entry in current_logs
            if entry["days_since_reset"] > 0
        ]
        print(f'Rates for current run #{run_id} : {rates}')

        if len(rates) < 2:
            return "Not enough data"

        # Takes the average drift of the rates 
        avg_rate = statistics.mean(rates)
        # Maths the standard deviation to see if the drift rate is consistent
        consistency = statistics.stdev(rates)
    
        if self.accuracy_sec is not None:
            within_avg = abs(avg_rate) <= self.accuracy_sec
            is_consistent = consistency <= self.accuracy_sec
   
            if within_avg and is_consistent:
                return "Performing within spec"
            
            elif within_avg and not is_consistent:
                return "Erractic - inconsistent day to day"

            elif abs(avg_rate) <= self.accuracy_sec * 2:
                return "Slightly out of spec"
            
            else:
                return "Needs service"
        else:
            return "No time accuracy provided."
        
    def to_dict(self):
        watch_db = {'brand': self.brand,
                    'model': self.model,
                    'reference NO': self.ref_no,
                    'serial NO': self.serial_no,
                    'movement_type': self.movement_type,
                    'accuracy_sec': self.accuracy_sec,
                    'current_run_id': self.current_id,
                    'last_reset_date': self.last_reset_date.isoformat(),
                    'accuracy_log': self.accuracy_log
        }

        return watch_db

    def specs(self):
        print(f"Watch: {self.brand} {self.model}")
        print(f"Ref NO: {self.ref_no} \nSerial NO: {self.serial_no}")
        print(f"Movement: {self.movement_type}")
        print(f"Accuracy: {self.accuracy_sec}")

class Collection:
    def __init__(self):
        # Initialize an empty list to store Watch objects
        self.watches = []

    def add(self, watch):
        self.watches.append(watch)

    def remove(self, watch):
        self.watches.remove(watch)

    def show_collection(self):
        # Prints all watched currently in the collection
        if not self.watches:
            return

        print(f"\n--- My Watch Collection ---\n")
        for watch in self.watches:
            watch.specs()
            print("-" * 30)

    def export_to_txt(self):
        try:
            with open('./data/collection.txt', mode='w', encoding='utf-8') as output_file:
                for watch in self.watches:
                    output_file.write(f"{watch.brand} {watch.model} {watch.ref_no} {watch.serial_no}\n")
                    
        except IOError as err:
            print("Error writing file.")
            raise err
        
    def export_to_json(self):
        json_data = []
        for watch in self.watches:
            json_data.append(watch.to_dict())
        try:
            with open('./data/collection.json', mode='w', encoding='utf-8') as output_file:
                json.dump(json_data, output_file, indent=4)
        except IOError as err:
            print("Error writing file.")
            raise err





