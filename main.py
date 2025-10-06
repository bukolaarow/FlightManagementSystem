from services import FlightService
from sample_data import sample_data

def main():
    service = FlightService()

    while True:
        print("\n" + "*" * 60)
        print("***** Welcome to Bukola's Flight Management System *****")
        print("*" * 60)
        print("1. Add a New Flight")
        print("2. View Flights by Status")
        print("3. Update Flight Status")
        print("4. Assign Pilot to Flight")
        print("5. View Pilot Schedule")
        print("6. Add Destination")
        print("7. Update Destination Notes")
        print("8. View Flights with Pilot and Destination")
        print("9. Get Flight Summary by Destination")
        print("10. Delete Flight by Flight Number")
        print("11. Remove Pilot from Flight")
        print("12. View Flights Assigned to Each Pilot")
        print("13. View Average Flight Distance per Destination")
        print("14. View Total Distance Flown by Pilot")
        print("15. View Flight Count by Destination")
        print("16. View All Flights")
        print("17. Insert sample data ")
        print("18. Reset Database")

        print("0. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == '1':
            service.add_new_flight()

        elif choice == '2':
            service.view_flights_by_status()

        elif choice == '3':
            service.update_flight_status()

        elif choice == '4':
            service.assign_pilot_to_flight()

        elif choice == '5':
            service.view_pilot_schedule()

        elif choice == '6':
            service.add_destination()

        elif choice == '7':
            service.update_destination_notes()

        elif choice == '8':
            service.view_flight_details()

        elif choice == '9':
            service.get_flight_summary()

        elif choice == '10':
            service.delete_flight_by_number()

        elif choice == '11':
            service.remove_pilot_from_flight() 

        elif choice == '12':
            service.view_flights_per_pilot()

        elif choice == '13':
            service.view_average_distance_by_destination()

        elif choice == '14':
            service.view_total_distance_by_pilot()
            
        elif choice == '15':
            service.view_flight_count_by_destination()

        elif choice == '16':
            service.view_all_flights()
        
        elif choice == '17':
            try:
                sample_data(service.cursor, service.conn)
            except Exception as e:
                print("Error inserting sample data:", e)

        elif choice == '18':
            service.reset_database()  

        elif choice == '0':
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid input. Please select a valid option.")

         # Ask user if they want to continue
        again = input("\nWould you like to perform another action? (yes/no): ").strip().lower()
        if again != 'yes':
            print("Thank you for using Bukola's Flight Management System. Goodbye!")
            break

if __name__ == "__main__":
    main()
