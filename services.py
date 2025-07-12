
import sqlite3

class FlightService:
    def __init__(self):
        """Initializes the database connection and ensures tables are created."""
        self.conn = sqlite3.connect("FlightManagement.db")
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Creates Pilot, Destination, and Flight tables if they do not already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pilot (
                PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Rank TEXT NOT NULL,
                LicenseNumber TEXT NOT NULL UNIQUE,
                LicenseExpiry DATE NOT NULL,
                FlightType TEXT NOT NULL,
                CertifiedAircraftCode TEXT NOT NULL,
                CertificationExpiry DATE NOT NULL,
                Email TEXT,
                PhoneNumber TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Destination (
                DestinationID INTEGER PRIMARY KEY AUTOINCREMENT,
                City TEXT NOT NULL,
                Country TEXT NOT NULL,
                AirportCode TEXT NOT NULL UNIQUE,
                TimeZone TEXT,
                Notes TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Flight (
                FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
                FlightNumber TEXT NOT NULL UNIQUE,
                PilotID INTEGER,
                OriginID INTEGER NOT NULL,
                DestinationID INTEGER NOT NULL,
                DepartureDate DATE NOT NULL,
                DepartureTime TIME NOT NULL,
                ArrivalDate DATE NOT NULL,
                ArrivalTime TIME NOT NULL,
                FlightStatus TEXT NOT NULL CHECK (FlightStatus IN 
                    ('Scheduled', 'Departed', 'Delayed', 'Cancelled', 'Completed')),
                Distance INTEGER NOT NULL,
                FOREIGN KEY (PilotID) REFERENCES Pilot(PilotID),
                FOREIGN KEY (OriginID) REFERENCES Destination(DestinationID),
                FOREIGN KEY (DestinationID) REFERENCES Destination(DestinationID)
            );
        """)
        self.conn.commit()

    def add_new_flight(self):
        """Prompts user for flight information and inserts a new flight into the database."""
        try:
            flight_data = (
                input("Flight Number: "),
                input("Pilot ID (can be blank): ") or None,
                input("Origin Destination ID: "),
                input("Destination ID: "),
                input("Departure Date (YYYY-MM-DD): "),
                input("Departure Time (HH:MM): "),
                input("Arrival Date (YYYY-MM-DD): "),
                input("Arrival Time (HH:MM): "),
                input("Flight Status (Scheduled, Departed, etc.): "),
                int(input("Distance in km: "))
            )
            self.cursor.execute("""
                INSERT INTO Flight (
                    FlightNumber, PilotID, OriginID, DestinationID,
                    DepartureDate, DepartureTime, ArrivalDate, ArrivalTime,
                    FlightStatus, Distance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, flight_data)
            self.conn.commit()
            print("Flight added successfully.")
        except Exception as e:
            print("Error adding flight:", e)

    def view_flights_by_status(self):
        """Displays all flights filtered by a specific status, including flight number,
        pilot name, origin, destination and departure/arrival info using JOINS.
        """
        status = input("Enter flight status: ").strip().capitalize()
        self.cursor.execute("""
            SELECT 
                f.FlightNumber,
                IFNULL(p.FirstName || ' ' || p.LastName, 'Unassigned') AS Pilot,
                o.City AS Origin,
                d.City AS Destination,
                f.DepartureDate,
                f.DepartureTime,
                f.ArrivalDate,
                f.ArrivalTime,
                f.FlightStatus
            FROM Flight f
            LEFT JOIN Pilot p ON f.PilotID = p.PilotID
            JOIN Destination o ON f.OriginID = o.DestinationID
            JOIN Destination d ON f.DestinationID = d.DestinationID
            WHERE f.FlightStatus = ?
            ORDER BY f.DepartureDate, f.DepartureTime
        """, (status,))

        rows = self.cursor.fetchall()

        if rows:
            print("\n********** Flights with Status:", status, "**********")
            print(f"{'Flight':<10} | {'Pilot':<20} | {'From':<12} | {'To':<12} | {'Depart':<10} | {'Time':<5} | {'Arrive':<10} | {'Time':<5}")
            print("-" * 100)
            for row in rows:
                print(f"{row[0]:<10} | {row[1]:<20} | {row[2]:<12} | {row[3]:<12} | {row[4]:<10} | {row[5]:<5} | {row[6]:<10} | {row[7]:<5}")
            print("*" * 100)
        else:
            print(f"No flights found with status '{status}'.")

    def update_flight_status(self):
        """Updates the flight status for a given flight ID."""
        flight_id = input("Enter Flight ID: ")
        new_status = input("Enter new status: ")
        self.cursor.execute("UPDATE Flight SET FlightStatus = ? WHERE FlightID = ?", (new_status, flight_id))
        self.conn.commit()
        print("Flight status updated.")

    def assign_pilot_to_flight(self):
        """Assigns a pilot to a flight based on IDs."""
        flight_id = input("Enter Flight ID: ")
        pilot_id = input("Enter Pilot ID: ")
        self.cursor.execute("UPDATE Flight SET PilotID = ? WHERE FlightID = ?", (pilot_id, flight_id))
        self.conn.commit()
        print("Pilot assigned to flight.")

    def remove_pilot_from_flight(self):
        """Removes a pilot assignment from a specific flight."""
        flight_id = input("Enter Flight ID to remove pilot from: ")
        self.cursor.execute("UPDATE Flight SET PilotID = NULL WHERE FlightID = ?", (flight_id,))
        self.conn.commit()
        print("Pilot removed from flight.")

    def view_pilot_schedule(self):
        """Displays all flights assigned to a particular pilot."""
        pilot_id = input("Enter Pilot ID: ").strip()

        self.cursor.execute("""
            SELECT 
                f.FlightNumber,
                f.DepartureDate,
                f.DepartureTime,
                f.ArrivalDate,
                f.ArrivalTime,
                o.City AS Origin,
                d.City AS Destination,
                f.FlightStatus
            FROM Flight f
            JOIN Destination o ON f.OriginID = o.DestinationID
            JOIN Destination d ON f.DestinationID = d.DestinationID
            WHERE f.PilotID = ?
            ORDER BY f.DepartureDate, f.DepartureTime
        """, (pilot_id,))

        results = self.cursor.fetchall()

        if results:
            print("\n********** Pilot Flight Schedule **********")
            print(f"{'Flight':<10} | {'Depart':<10} | {'Time':<5} | {'Arrive':<10} | {'Time':<5} | {'From':<12} | {'To':<12} | {'Status':<10}")
            print("-" * 90)
            for row in results:
                print(f"{row[0]:<10} | {row[1]:<10} | {row[2]:<5} | {row[3]:<10} | {row[4]:<5} | {row[5]:<12} | {row[6]:<12} | {row[7]:<10}")
            print("*" * 90)
        else:
            print("No flights assigned to this pilot.")

    def add_destination(self):
        """Prompts for and adds a new destination to the database."""
        destination_data = (
            input("City: "),
            input("Country: "),
            input("Airport Code: "),
            input("Time Zone: "),
            input("Notes: ")
        )
        try:
            self.cursor.execute("""
                INSERT INTO Destination (City, Country, AirportCode, TimeZone, Notes)
                VALUES (?, ?, ?, ?, ?)
            """, destination_data)
            self.conn.commit()
            print("Destination added.")
        except Exception as e:
            print("Error adding destination:", e)

    def update_destination_notes(self):
        """Updates the notes for a specific destination by ID."""
        dest_id = input("Enter Destination ID: ")
        notes = input("Enter updated notes: ")
        self.cursor.execute("UPDATE Destination SET Notes = ? WHERE DestinationID = ?", (notes, dest_id))
        self.conn.commit()
        print("Destination notes updated.")

    def view_flight_details(self):
        """Displays detailed info of all flights including pilot, origin, and destination."""
        self.cursor.execute("""
            SELECT 
                f.FlightNumber,
                f.DepartureDate,
                IFNULL(p.FirstName || ' ' || p.LastName, 'Unassigned') AS Pilot,
                o.City AS OriginCity,
                d.City AS DestinationCity,
                f.FlightStatus
            FROM 
                Flight f
            LEFT JOIN 
                Pilot p ON f.PilotID = p.PilotID
            JOIN 
                Destination o ON f.OriginID = o.DestinationID
            JOIN 
                Destination d ON f.DestinationID = d.DestinationID
        """)
        for row in self.cursor.fetchall():
            print(row)

    def get_flight_summary(self):
        """Displays a summary of how many flights go to each destination."""
        self.cursor.execute("""
            SELECT 
                d.City,
                COUNT(f.FlightID) AS TotalFlights
            FROM 
                Flight f
            JOIN 
                Destination d ON f.DestinationID = d.DestinationID
            GROUP BY 
                d.City
            ORDER BY 
                TotalFlights DESC
        """)
        results = self.cursor.fetchall()
        if results:
            print("\n********** Flight Summary by Destination **********")
            print(f"{'Destination':<20} | {'Total Flights':<15}")
            print("-" * 40)
            for city, total in results:
                print(f"{city:<20} | {str(total):<15}")
            print("*" * 40)
        else:
            print("No flight summary available.")

    
    def delete_flight_by_number(self):
            """Deletes a flight record from the database using the flight number."""
            flight_number = input("Enter Flight Number to delete: ")
        # Step 1: Check if the flight exists
            self.cursor.execute("SELECT * FROM Flight WHERE FlightNumber = ?", (flight_number,))
            flight = self.cursor.fetchone()

            if not flight:
                print(f"No flight found with flight number '{flight_number}'.")
                return

            # Step 2: Display flight info to confirm
            print("\nFlight found:")
            print(f"Flight ID: {flight[0]}")
            print(f"Flight Number: {flight[1]}")
            print(f"Status: {flight[9]}")
            
        # Step 3: Confirm deletion
            confirm = input("Are you sure you want to delete this flight? (yes/no): ").strip().lower()
            if confirm == "yes":
                self.cursor.execute("DELETE FROM Flight WHERE FlightNumber = ?", (flight_number,))
                self.conn.commit()
                print("Flight deleted.")
            else:
                print("Deletion cancelled.")
    
    def view_flights_per_pilot(self):
        """
        Displays the number of flights assigned to each pilot.
        Uses JOIN and GROUP BY to count assignments.
        """
        self.cursor.execute("""
            SELECT 
                IFNULL(p.FirstName || ' ' || p.LastName, 'Unassigned') AS Pilot,
                COUNT(f.FlightID) AS FlightCount
            FROM Flight f
            LEFT JOIN Pilot p ON f.PilotID = p.PilotID
            GROUP BY f.PilotID
            ORDER BY FlightCount DESC
        """)
        rows = self.cursor.fetchall()
        print(f"\n{'Pilot':<25} | {'Flights Assigned'}")
        print("-" * 45)
        for row in rows:
            print(f"{row[0]:<25} | {row[1]}")
    
    def view_average_distance_by_destination(self):
        """
        Shows average flight distance to each destination city.
        Uses JOIN and AVG to calculate route trends.
        """
        self.cursor.execute("""
            SELECT 
                d.City,
                ROUND(AVG(f.Distance), 2) AS AvgDistance
            FROM Flight f
            JOIN Destination d ON f.DestinationID = d.DestinationID
            GROUP BY d.City
            ORDER BY AvgDistance DESC
        """)
        rows = self.cursor.fetchall()
        print(f"\n{'Destination':<20} | {'Avg Distance (km)'}")
        print("-" * 45)
        for row in rows:
            print(f"{row[0]:<20} | {row[1]}")

    def view_total_distance_by_pilot(self):
        """
        Displays total distance flown by each pilot.
        Useful for tracking workload or performance.
        """
        self.cursor.execute("""
            SELECT 
                IFNULL(p.FirstName || ' ' || p.LastName, 'Unassigned') AS Pilot,
                SUM(f.Distance) AS TotalDistance
            FROM Flight f
            LEFT JOIN Pilot p ON f.PilotID = p.PilotID
            GROUP BY f.PilotID
            ORDER BY TotalDistance DESC
        """)
        rows = self.cursor.fetchall()
        print(f"\n{'Pilot':<25} | {'Total Distance (km)'}")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:<25} | {row[1]}")
       
    def view_flight_count_by_destination(self):
        """
        Shows how many flights go to each destination.
        Uses COUNT and GROUP BY for basic demand analysis.
        """
        self.cursor.execute("""
            SELECT 
                d.City,
                COUNT(f.FlightID) AS FlightCount
            FROM Flight f
            JOIN Destination d ON f.DestinationID = d.DestinationID
            GROUP BY d.City
            ORDER BY FlightCount DESC
        """)
        rows = self.cursor.fetchall()
        print(f"\n{'Destination':<20} | {'Flight Count'}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<20} | {row[1]}")
            