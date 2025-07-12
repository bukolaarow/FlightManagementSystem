import sqlite3

def sample_data():
    conn = sqlite3.connect("FlightManagement.db")
    cur = conn.cursor()

    # Sample Destinations
    destinations = [
        ('London', 'UK', 'LHR', 'GMT', 'Heathrow Airport'),
        ('New York', 'USA', 'JFK', 'EST', 'John F. Kennedy International'),
        ('Dubai', 'UAE', 'DXB', 'GST', 'Dubai International Airport'),
        ('Tokyo', 'Japan', 'HND', 'JST', 'Tokyo Haneda Airport'),
        ('Paris', 'France', 'CDG', 'CET', 'Charles de Gaulle Airport'),
        ('Sydney', 'Australia', 'SYD', 'AEST', 'Sydney Kingsford Smith Airport'),
        ('Frankfurt', 'Germany', 'FRA', 'CET', 'Frankfurt Main Airport'),
        ('Toronto', 'Canada', 'YYZ', 'EST', 'Toronto Pearson Airport'),
        ('Singapore', 'Singapore', 'SIN', 'SGT', 'Changi Airport'),
        ('Johannesburg', 'South Africa', 'JNB', 'SAST', 'OR Tambo International Airport')
    ]

    # Sample Pilots
    pilots = [
        ('Alice', 'Johnson', 'Captain', 'ALC12345', '2026-05-20', 'Commercial', 'A320', '2025-12-01', 'alice.j@example.com', '1234567890'),
        ('Brian', 'Smith', 'First Officer', 'BRS67890', '2027-03-15', 'Commercial', 'B737', '2026-11-22', 'brian.s@example.com', '2345678901'),
        ('Clara', 'Lee', 'Captain', 'CLR54321', '2025-08-30', 'Commercial', 'A380', '2025-07-15', 'clara.l@example.com', '3456789012'),
        ('David', 'Brown', 'First Officer', 'DVB11111', '2028-01-10', 'Commercial', 'B777', '2027-09-05', 'david.b@example.com', '4567890123'),
        ('Evelyn', 'Wilson', 'Captain', 'EVW22222', '2026-12-01', 'Commercial', 'A350', '2025-10-10', 'evelyn.w@example.com', '5678901234'),
        ('Frank', 'Taylor', 'First Officer', 'FRT33333', '2025-11-20', 'Commercial', 'A320', '2025-12-01', 'frank.t@example.com', '6789012345'),
        ('Grace', 'Martins', 'Captain', 'GRM44444', '2026-04-25', 'Commercial', 'B787', '2026-06-15', 'grace.m@example.com', '7890123456'),
        ('Henry', 'Lopez', 'First Officer', 'HNL55555', '2027-07-18', 'Commercial', 'A321', '2026-11-30', 'henry.l@example.com', '8901234567'),
        ('Ivy', 'Nguyen', 'Captain', 'IVN66666', '2025-09-19', 'Commercial', 'B777', '2026-03-22', 'ivy.n@example.com', '9012345678'),
        ('Jack', 'Owen', 'First Officer', 'JKO77777', '2028-02-10', 'Commercial', 'B737', '2027-12-01', 'jack.o@example.com', '9123456789')
    ]

    # Sample Flights — ensure destination and pilot IDs are correct based on inserts
    flights = [
        ('BA101', 1, 1, 2, '2025-07-01', '09:00', '2025-07-01', '13:00', 'Scheduled', 5567),
        ('EK302', 3, 3, 4, '2025-07-02', '23:00', '2025-07-03', '07:30', 'Scheduled', 7930),
        ('AF789', 5, 5, 1, '2025-07-05', '08:30', '2025-07-05', '10:00', 'Delayed', 342),
        ('QF112', 6, 6, 4, '2025-07-06', '15:45', '2025-07-06', '22:00', 'Cancelled', 12000),
        ('DL456', 2, 2, 8, '2025-07-07', '11:00', '2025-07-07', '14:15', 'Departed', 3000),
        ('LH321', 4, 7, 5, '2025-07-08', '07:00', '2025-07-08', '10:00', 'Scheduled', 1100),
        ('SQ918', 8, 9, 4, '2025-07-09', '19:20', '2025-07-10', '05:10', 'Completed', 6500),
        ('AC222', 9, 8, 1, '2025-07-10', '06:00', '2025-07-10', '12:00', 'Scheduled', 5800),
        ('SAA999', 10, 10, 1, '2025-07-11', '16:45', '2025-07-11', '23:30', 'Scheduled', 8700),
        ('VA777', 7, 6, 3, '2025-07-12', '13:00', '2025-07-12', '20:00', 'Scheduled', 14000)
    ]

    cur.executemany("INSERT INTO Destination (city, country, airportCode, timeZone, notes) VALUES (?, ?, ?, ?, ?)", destinations)
    cur.executemany("INSERT INTO Pilot (FirstName, LastName, Rank, LicenseNumber, LicenseExpiry, FlightType, CertifiedAircraftCode, CertificationExpiry, Email, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", pilots)
    cur.executemany("INSERT INTO Flight (flightNumber, pilotID, OriginID, DestinationID, departureDate, departureTime, arrivalDate, arrivalTime, flightStatus, distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", flights)

    conn.commit()
    print("Sample data inserted successfully.")
    conn.close()

if __name__ == "__main__":
    sample_data()
