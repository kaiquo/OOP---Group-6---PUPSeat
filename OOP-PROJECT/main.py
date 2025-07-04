import customtkinter as ctk
from frontend.app import RideBookingApp

ctk.set_appearance_mode("light")
root = ctk.CTk()
app = RideBookingApp(root)
root.mainloop()
