import csv
import os

table = [
    {'number': 1, 'seats': 2},
    {'number': 2, 'seats': 4},
    {'number': 3, 'seats': 6},
    {'number': 4, 'seats': 4},
    {'number': 5, 'seats': 6}
]

class Reservation:
    def __init__(self, tables, reservation_file):
        self.__reservation_file = reservation_file
        self.__tables = tables

    @property
    def tables(self):
        return self.__tables

    def make_reservation(self):
        name = input("Enter your name: ")
        contact = input('Enter your contact number: ')
        party_size = int(input("Enter number of people: "))
        date = input("Enter reservation date (DD/MM/YYYY): ")
        start_time = input("Enter the start time: ")
        end_time = input("Enter the end time: ")

        available_tables = [table for table in self.tables if table['seats'] >= party_size]

        if not available_tables:
            print("No available tables for your party size.")
            return

        print("Available Tables:")
        for table in available_tables:
            print(f"Table {table['number']} - seats {table['seats']}")

        table_number = int(input("Enter table number to reserve: "))

        if table_number not in [table['number'] for table in available_tables]:
            print("Invalid table number")
            return

        new_row = [table_number, name, party_size, date, start_time, end_time]
        header = ['table_number', 'name', 'party_size', 'date', 'start_time', 'end_time']

        try:
            file_exist = os.path.exists(self.__reservation_file) and os.path.getsize(self.__reservation_file) > 0
            with open(self.__reservation_file, "a", newline="") as file:
                writer = csv.writer(file)
                if not file_exist:
                    writer.writerow(header)
                writer.writerow(new_row)
                print(f"Table {table_number} reserved successfully for {name} on {date}")
        except Exception as e:
            print(f"Error found: {e}")

    def view_reservation(self):
        try:
            with open(self.__reservation_file, "r") as file:
                reader = csv.reader(file)
                for reservation in reader:
                    print(reservation)
        except Exception as e:
            print("Error:", e)

    def cancel_reservation(self):
        name = input("Enter your name: ")
        date = input("Enter the date of reservation (DD/MM/YYYY): ")
        table_number = int(input("Enter table number: "))

        try:
            with open(self.__reservation_file, "r", newline="") as file:
                reader = csv.reader(file)
                header = next(reader)
                reserves = list(reader)

            found_reservation = False

            with open(self.__reservation_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)

                for reserve in reserves:
                    if (reserve[1] == name and 
                        reserve[3] == date and 
                        int(reserve[0]) == table_number):
                        found_reservation = True
                        print(f"Reservation for {name} on {date} at table {table_number} cancelled successfully.")
                    else:
                        writer.writerow(reserve)

            if not found_reservation:
                print("Reservation not found.")

        except Exception as e:
            print("Error:", e)

    def modify_reservation(self):
        date = input("Enter the date of the reservation to modify (DD/MM/YYYY): ")
        name = input("Enter the name of the reservation to modify: ")

        try:
            with open(self.__reservation_file, "r", newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                reservations = list(reader)

            found_reservation = False

            for row in reservations:
                if row[1] == name and row[3] == date:
                    found_reservation = True
                    print("Current reservation details:", row)
                    print("\n You can go ahead and make your Modifications.")
                    new_name = input(f"\n Enter new name (leave blank to keep '{row[1]}'): ")
                    if new_name:
                        row[1] = new_name

                    new_date = input(f"Enter new date (leave blank to keep '{row[3]}'): ")
                    if new_date:
                        row[3] = new_date

                    new_party_size = int(input(f"Enter your party size (leave blank to keep '{row[2]}'): "))
                    
                    if new_party_size > int(row[2]):
                        row[2] = new_party_size
                        print("Please select a new table")
                        available_tables = [table for table in self.tables if table['seats'] >= new_party_size]

                        if not available_tables:
                            print("No available tables for your party size.")
                            return

                        print("Available Tables:")
                        for table in available_tables:
                            print(f"Table {table['number']} - seats {table['seats']}")

                        table_number = int(input("Enter table number to reserve: "))
                        row[0] = table_number

                        if table_number not in [table['number'] for table in available_tables]:
                            print("Invalid table number")
                            return

  
            if found_reservation:
                with open(self.__reservation_file, "w", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writer.writerows(reservations)
                        print("Reservation updated successfully.")
            else:
                    print("No reservation found for the given details.")

        except Exception as e:
            print("Error:", e)

    def daily_summary(self):
        date = input("Enter date of reservation (DD/MM/YYYY): ")
        try:
            with open(self.__reservation_file, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                reservations = list(reader)
                right_reservations = [row for row in reservations if row[3] == date]
                
                if right_reservations:
                    print("Daily Summary for", date)
                    for reservation in right_reservations:
                        print(reservation)
                else:
                    print("No reservations found for the date:", date)

        except Exception as e:
            print("Error:", e)

# Example usage:
def menu():
    reservation_file = 'reserved_seats.csv'
    reservation_system = Reservation(table, reservation_file)
    
    while True:
        print("\n1. Make Reservation")
        print("2. View Reservations")
        print("3. Cancel Reservation")
        print("4. Modify Reservation")
        print("5. Daily Summary")
        print("6. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            reservation_system.make_reservation()
        elif choice == '2':
            reservation_system.view_reservation()
        elif choice == '3':
            reservation_system.cancel_reservation()
        elif choice == '4':
            reservation_system.modify_reservation()
        elif choice == '5':
            reservation_system.daily_summary()
        elif choice == '6':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.")

menu()
