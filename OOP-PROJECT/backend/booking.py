import csv
import os

BOOKING_FILE = "bookings.csv"

def load_bookings():
    # Load bookings from the CSV file and return a list of booking dictionaries
    bookings = []
    if os.path.exists(BOOKING_FILE):
        with open(BOOKING_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bookings.append({
                    "id": row["ID"],
                    "user": row["User"],
                    "vehicle": row["Vehicle"],
                    "start": row["Pick Up"],      
                    "end": row["Drop Off"],      
                    "distance": row["Distance"],
                    "cost": row["Cost"],
                    "status": row["Status"]
                })
    return bookings

def save_bookings(bookings):
    # Save the list of booking dictionaries to the CSV file
    with open(BOOKING_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "User", "Vehicle", "Pick Up", "Drop Off", "Distance", "Cost", "Status"
        ])  # Write header row
        for b in bookings:
            writer.writerow([
                b["id"], b["user"], b["vehicle"],
                b["start"], b["end"],
                b["distance"], b["cost"], b["status"]
            ])