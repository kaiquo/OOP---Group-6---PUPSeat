import os
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
from tkintermapview import TkinterMapView

from backend.vehicle import create_vehicle
from backend.booking import load_bookings, save_bookings
from backend.distance import get_coords_and_distance

class RideBookingApp:
    def __init__(self, root):
        
#Initialize the main application window, set up the UI, and load bookings.
        
        self.root = root
        self.root.title("PUPSeat")
        ico_path = os.path.join(os.path.dirname(__file__), "app_logo.ico")
        try:
            self.root.iconbitmap(ico_path)
        except Exception:
            pass
        self.root.state('zoomed')
        self.root.configure(bg="#400000")

        self.bookings = load_bookings()
        self.active_paths = []
        self.create_widgets()

    def create_widgets(self):
        
#Create and layout all widgets for the main application interface.
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)

        outer_frame = ctk.CTkFrame(self.root, fg_color="#400000")
        outer_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=3)
        outer_frame.grid_columnconfigure(1, weight=2)

        left_frame = ctk.CTkFrame(outer_frame, fg_color="#400000")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.grid_rowconfigure(2, weight=1)

        title_frame = ctk.CTkFrame(
            left_frame,
            fg_color="#400000",
            corner_radius=15,
            border_color="#f4bb00",
            border_width=2
        )
        title_frame.pack(pady=(5, 0), padx=130, fill="x")
        ctk.CTkLabel(
            title_frame,
            text="🚌 PUPSeat: Ride Booking System",
            font=("Lucida Console", 22, "bold"),
            text_color="#f4bb00",
        ).pack(pady=8)

        form_panel = ctk.CTkFrame(left_frame, fg_color="#400000", corner_radius=0)
        form_panel.pack(fill="x", padx=5, pady=(0,15))
        inner = ctk.CTkFrame(form_panel, fg_color="#d3d3d3")
        inner.pack(fill="x", padx=5, pady=5)
        inner.grid_columnconfigure((0,1), weight=1)

        entry_font = ctk.CTkFont(family="Courier New", size=16)
        label_font = ctk.CTkFont(family="Courier New", size=16, weight="bold")

        li = ctk.CTkFrame(inner, fg_color="#d3d3d3")
        li.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(li, text="Username:", font=label_font, text_color="#400000", fg_color="#d3d3d3").pack(anchor="w", padx=5, pady=(5,0))
        self.username_entry = ctk.CTkEntry(li, font=entry_font, fg_color="white", text_color="black")
        self.username_entry.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(li, text="Vehicle Type:", font=label_font, text_color="#400000", fg_color="#d3d3d3").pack(anchor="w", padx=5, pady=(5,0))
        self.vehicle_var = ctk.StringVar(value="Sedan")
        self.vehicle_menu = ctk.CTkOptionMenu(
            li,
            variable=self.vehicle_var,
            values=[
                "Horse","Motorcycle","Sedan","SUV","Van","Monster Truck",
                "Helicopter","Elevator of Willy Wonka","Magic Carpet","Tardis","Dragon","UFO"
            ],
            fg_color="white", text_color="black",
            button_color="#f4bb00", button_hover_color="#c46b02",
            font=entry_font
        )
        self.vehicle_menu.pack(fill="x", padx=5, pady=5)

        ri = ctk.CTkFrame(inner, fg_color="#d3d3d3")
        ri.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(ri, text="Start Location:", font=label_font, text_color="#400000", fg_color="#d3d3d3").pack(anchor="w", padx=5, pady=(5,0))
        self.start_entry = ctk.CTkEntry(ri, font=entry_font, fg_color="white", text_color="black")
        self.start_entry.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(ri, text="End Location:", font=label_font, text_color="#400000", fg_color="#d3d3d3").pack(anchor="w", padx=5, pady=(5,0))
        self.end_entry = ctk.CTkEntry(ri, font=entry_font, fg_color="white", text_color="black")
        self.end_entry.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(
            left_frame,
            text="Book Ride",
            command=self.book_ride,
            width=300,
            fg_color="#fdde54",
            hover_color="#c46b02",
            text_color="black",
            font=ctk.CTkFont(family="Courier New", size=16, weight="bold")
        ).pack(pady=(0,15))

        tw = ctk.CTkFrame(left_frame, fg_color="#400000", corner_radius=0)
        tw.pack(fill="both", expand=True, padx=5, pady=(0,15))

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            font=("Courier New", 13),
            foreground="black",
            background="white",
            fieldbackground="white",
            rowheight=25
        )
        style.map("Treeview", background=[("selected", "#3399ff")])

        self.tree = ttk.Treeview(
            tw,
            columns=("ID","User","Vehicle","Pick Up","Drop Off","Distance (km)","Cost","Status"),
            show="headings",
            height=12
        )
        for col, width in {
            "ID": 60, "User": 100, "Vehicle": 120, "Pick Up": 150, "Drop Off": 150,
            "Distance (km)": 100, "Cost": 100, "Status": 100
        }.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("Finished", background="#90EE90", foreground="black")
        self.tree.tag_configure("Cancelled", background="#F62222", foreground="white")
        self.tree.tag_configure("Active", background="#FFFACD", foreground="black")

        for b in self.bookings:
            tag = b["status"]
            self.tree.insert(
                "", "end",
                values=(b["id"], b["user"], b["vehicle"], b["start"], b["end"], b["distance"], f"₱{b['cost']}", b["status"]),
                tags=(tag,)
            )

        af = ctk.CTkFrame(left_frame, fg_color="#400000")
        af.pack(fill="x", padx=5, pady=(0,15))
        afont = ctk.CTkFont(family="Courier New", size=15, weight="bold")
        for txt, cmd in [("Finish Booking", self.finish_booking),
                         ("Cancel Booking", self.cancel_booking),
                         ("Clear Finished/Cancelled", self.clear_finished_cancelled)]:
            ctk.CTkButton(
                af,
                text=txt,
                command=cmd,
                fg_color="#fdde54",
                hover_color="#c46b02",
                text_color="black",
                font=afont
            ).pack(side="left", expand=True, fill="x", padx=5)

        right_frame = ctk.CTkFrame(outer_frame, fg_color="#400000")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        self.map_widget = TkinterMapView(right_frame, corner_radius=0)
        self.map_widget.grid(row=0, column=0, sticky="nsew")
        self.map_widget.configure(background="#400000")

        self.update_map_view()

    def get_next_id(self):
        
#Generate the next booking ID based on the current number of bookings.
        
        return f"00{len(self.bookings)+1:03d}"

    def book_ride(self):
        
#Handle the booking process: validate input, calculate fare, confirm, and save booking.
        
        username = self.username_entry.get().strip()
        vehicle_type = self.vehicle_var.get()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        if not username or not start or not end:
            showerror("Input Error", "Please fill in all fields.")
            return

        if start.lower() == end.lower():
            showerror("Input Error", "Start and end locations cannot be the same.")
            return

        start_coords, end_coords, distance = get_coords_and_distance(start, end)
        if not start_coords or not end_coords:
            showerror("Location Error", "Invalid start or end location.")
            return

        vehicle = create_vehicle(vehicle_type)
        cost = vehicle.calculate_fare(distance)

        confirm = askyesno(
            "Confirm Booking",
            f"Vehicle: {vehicle.get_type()}\nDistance: {distance:.2f} km\nFare: ₱{cost:.2f}\n\nDo you want to confirm the booking?"
        )
        if not confirm:
            return

        booking_id = self.get_next_id()
        booking_data = {
            "id": booking_id, "user": username, "vehicle": vehicle.get_type(),
            "start": start, "end": end, "distance": f"{distance:.2f}",
            "cost": f"{cost:.2f}", "status": "Active"
        }

        self.bookings.append(booking_data)
        self.tree.insert("", "end", values=(
            booking_id, username, vehicle.get_type(), start, end,
            f"{distance:.2f}", f"₱{cost:.2f}", "Active"
        ), tags=("Active",))

        save_bookings(self.bookings)
        self.update_map_view()
        showinfo("Booked", "Ride has been booked.")

    def finish_booking(self):
        
#Mark the selected booking(s) as 'Finished'.
        
        self.update_status("Finished")
        self.tree.selection_remove(self.tree.selection())

    def cancel_booking(self):
        
#Mark the selected booking(s) as 'Cancelled'.
        
        self.update_status("Cancelled")
        self.tree.selection_remove(self.tree.selection())

    def update_status(self, new_status):
        
#Update the status of selected booking(s) in the tree and backend data.
        
        selected = self.tree.selection()
        if not selected:
            showwarning("No Selection", f"Select a booking to mark as {new_status}.")
            return

        updated = False
        for item in selected:
            values = self.tree.item(item, "values")
            booking_id, current_status = values[0], values[-1]

            if current_status in ["Finished", "Cancelled"]:
                showinfo("Action Blocked", f"Booking {booking_id} is already {current_status}.")
                continue

            confirm = askyesno(f"Confirm {new_status}", f"Are you sure you want to mark booking {booking_id} as {new_status}?")
            if not confirm:
                continue

            for booking in self.bookings:
                if booking["id"] == booking_id:
                    booking["status"] = new_status
                    break

            self.tree.item(item, values=(*values[:-1], new_status), tags=(new_status,))
            updated = True

        if updated:
            save_bookings(self.bookings)
            self.update_map_view()

    def update_map_view(self):
        
#Update the map to show active bookings with markers and paths.
        
        for item in self.active_paths:
            item.delete()
        self.active_paths.clear()

        self.map_widget.set_position(14.5995, 120.9842)
        self.map_widget.set_zoom(10)

        for booking in self.bookings:
            if booking["status"] != "Active":
                continue
            coords = get_coords_and_distance(booking["start"], booking["end"])
            if coords[0] and coords[1]:
                m1 = self.map_widget.set_marker(*coords[0], text="Start", text_color="black")
                m2 = self.map_widget.set_marker(*coords[1], text="End", text_color="black")
                path = self.map_widget.set_path([coords[0], coords[1]])
                self.active_paths.extend([m1, m2, path])

    def clear_finished_cancelled(self):
        
#Remove finished and cancelled bookings from the tree view (UI only).
        
        confirm = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to remove all finished and cancelled bookings from the list? (This won't affect saved data.)"
        )
        if not confirm:
            return

        for item in self.tree.get_children():
            status = self.tree.item(item, "values")[-1]
            if status in ["Finished", "Cancelled"]:
                self.tree.delete(item)