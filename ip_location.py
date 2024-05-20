import tkinter as tk
from tkinter import messagebox
import socket
import requests

def get_ip_location():
    ip_address = entry.get()
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        
        ip_address = socket.gethostbyname(hostname)
        
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        
        data = response.json()
        country = data.get('country', 'Unknown')
        city = data.get('city', 'Unknown')
        latitude = data.get('loc', 'Unknown').split(',')[0]
        longitude = data.get('loc', 'Unknown').split(',')[1]
        
        info_str = f"IP Address: {ip_address}\nCountry: {country}\nCity: {city}\nLatitude: {latitude}\nLongitude: {longitude}"
        
        messagebox.showinfo("Location Information", info_str)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("IP Location Finder")

label = tk.Label(root, text="Enter IP Address:")
label.pack()
entry = tk.Entry(root)
entry.pack()

submit_btn = tk.Button(root, text="Find Location", command=get_ip_location)
submit_btn.pack()

root.mainloop()
