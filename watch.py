import json

class Watch:
    def __init__(self, brand, model, ref_no="N/A", serial_no="N/A"):
        self.brand = brand
        self.model = model
        self.ref_no = ref_no
        self.serial_no = serial_no
    
    def to_dict(self):
        watch_db = {'brand': self.brand,
                    'model': self.model,
                    'reference NO': self.ref_no,
                    'serial NO': self.serial_no
        }

        return watch_db

    def specs(self):
        print(f"Watch: {self.brand} {self.model}")
        print(f"Ref NO: {self.ref_no} \nSerial NO: {self.serial_no}")

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

if __name__ == "__main__":
    my_vault = Collection()
    watch1 = Watch("Seiko", "Selection", "SBTM325")
    watch2 = Watch("Seiko", "A904 5199")
    watch3 = Watch("Casio", "f91w")
    my_vault.add(watch1)
    my_vault.add(watch2)
    my_vault.add(watch3)
    my_vault.export_to_json()



