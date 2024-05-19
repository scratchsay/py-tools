import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import threading
from faker import Faker
import datetime
import os
import subprocess

fake = Faker()

def get_suburls(base_url):
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            return set()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        anchor_tags = soup.find_all('a', href=True)
        
        sub_urls = set()
        for tag in anchor_tags:
            href = tag['href']
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                sub_urls.add(full_url)
        return sub_urls
    except requests.RequestException as e:
        return set()

def crawl_website(start_url, output_text):
    to_visit = deque([start_url])
    visited = set()
    
    while to_visit:
        current_url = to_visit.popleft()
        if current_url not in visited:
            output_text.insert(tk.END, f"Visiting: {current_url}\n")
            output_text.see(tk.END)
            visited.add(current_url)
            
            sub_urls = get_suburls(current_url)
            for url in sub_urls:
                if url not in visited:
                    to_visit.append(url)
    
    output_text.insert(tk.END, f"\nAll sub-URLs found on {start_url}:\n")
    for sub_url in sorted(visited):
        output_text.insert(tk.END, f"{sub_url}\n")
    output_text.see(tk.END)

def website_scan():
    scan_window = tk.Toplevel(root)
    scan_window.title("Website Scan")
    scan_window.geometry("500x400")
    
    url_label = tk.Label(scan_window, text="Enter URL to scan:")
    url_label.pack(pady=5)
    
    url_entry = tk.Entry(scan_window, width=50)
    url_entry.pack(pady=5)
    
    output_text = scrolledtext.ScrolledText(scan_window, width=60, height=20)
    output_text.pack(pady=10)
    
    def on_scan_button():
        url = url_entry.get().strip()
        if url:
            output_text.delete('1.0', tk.END)  # Clear previous output
            scan_thread = threading.Thread(target=crawl_website, args=(url, output_text))
            scan_thread.start()
    
    scan_button = tk.Button(scan_window, text="Scan", command=on_scan_button)
    scan_button.pack(pady=10)

def generate_fake_data(num_entries=10):
    fake_data_list = []

    for _ in range(num_entries):
        full_name = fake.name()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
        age = (datetime.date.today() - date_of_birth).days // 365
        address = fake.address().replace('\n', ', ')
        password = fake.password()
        phone_number = fake.phone_number()
        email_address = fake.email()

        fake_data = {
            "Full Name": full_name,
            "Date of Birth": date_of_birth,
            "Age": age,
            "Address": address,
            "Password": password,
            "Phone Number": phone_number,
            "Email Address": email_address
        }

        fake_data_list.append(fake_data)

    return fake_data_list

def identity_spoof():
    spoof_window = tk.Toplevel(root)
    spoof_window.title("Identity Spoof")
    spoof_window.geometry("500x400")
    
    num_label = tk.Label(spoof_window, text="Enter number of fake identities to generate:")
    num_label.pack(pady=5)
    
    num_entry = tk.Entry(spoof_window, width=20)
    num_entry.pack(pady=5)
    
    output_text = scrolledtext.ScrolledText(spoof_window, width=60, height=20)
    output_text.pack(pady=10)
    
    def on_generate_button():
        try:
            num_entries = int(num_entry.get().strip())
            fake_data_list = generate_fake_data(num_entries)
            output_text.delete('1.0', tk.END)
            for entry in fake_data_list:
                for key, value in entry.items():
                    output_text.insert(tk.END, f"{key}: {value}\n")
                output_text.insert(tk.END, "\n")
            output_text.see(tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    generate_button = tk.Button(spoof_window, text="Generate", command=on_generate_button)
    generate_button.pack(pady=10)

def run_pylint(file_or_directory):
    """Run pylint on the specified file or directory."""
    try:
        result = subprocess.run(['pylint', file_or_directory], capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

def analyze_code(base_path, output_text):
    """Analyze Python code in the given directory or file."""
    if not os.path.exists(base_path):
        output_text.insert(tk.END, f"Error: The path '{base_path}' does not exist.\n")
        output_text.see(tk.END)
        return
    
    if os.path.isdir(base_path):
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    output_text.insert(tk.END, f"\nAnalyzing {file_path}:\n")
                    stdout, stderr = run_pylint(file_path)
                    if stdout:
                        output_text.insert(tk.END, stdout)
                    if stderr:
                        output_text.insert(tk.END, f"Error: {stderr}\n")
                    output_text.see(tk.END)
    else:
        if base_path.endswith(".py"):
            output_text.insert(tk.END, f"\nAnalyzing {base_path}:\n")
            stdout, stderr = run_pylint(base_path)
            if stdout:
                output_text.insert(tk.END, stdout)
            if stderr:
                output_text.insert(tk.END, f"Error: {stderr}\n")
            output_text.see(tk.END)
        else:
            output_text.insert(tk.END, "Error: The specified file is not a Python file (.py).\n")
            output_text.see(tk.END)

def code_analyzer():
    analyzer_window = tk.Toplevel(root)
    analyzer_window.title("Code Analyzer")
    analyzer_window.geometry("500x400")
    
    path_label = tk.Label(analyzer_window, text="Enter path to Python file or directory:")
    path_label.pack(pady=5)
    
    path_entry = tk.Entry(analyzer_window, width=50)
    path_entry.pack(pady=5)
    
    output_text = scrolledtext.ScrolledText(analyzer_window, width=60, height=20)
    output_text.pack(pady=10)
    
    def on_analyze_button():
        path = path_entry.get().strip()
        if path:
            output_text.delete('1.0', tk.END)
            analyze_thread = threading.Thread(target=analyze_code, args=(path, output_text))
            analyze_thread.start()
    
    analyze_button = tk.Button(analyzer_window, text="Analyze", command=on_analyze_button)
    analyze_button.pack(pady=10)

root = tk.Tk()
root.title("Security Tools")
root.geometry("300x200")

scan_button = tk.Button(root, text="Website Scan", command=website_scan, width=25, height=2)
scan_button.pack(pady=10)

spoof_button = tk.Button(root, text="Identity Spoof", command=identity_spoof, width=25, height=2)
spoof_button.pack(pady=10)

analyzer_button = tk.Button(root, text="Code Analyzer", command=code_analyzer, width=25, height=2)
analyzer_button.pack(pady=10)

root.mainloop()
