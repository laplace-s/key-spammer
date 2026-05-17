import tkinter as tk
from tkinter import ttk
import threading
import time
import keyboard

# Global variables
running = False
typing_thread = None

# Function to start the key press simulation
def start_typing():
    global running
    global typing_thread
    
    key = key_entry.get()
    try:
        interval = int(interval_entry.get()) / 1000.0
    except ValueError:
        result_label.config(text="Please enter a valid number for interval")
        return
    
    if not key:
        result_label.config(text="Please enter a key to press")
        return

    # Function to simulate key presses
    def type_key():
        while running:
            keyboard.write(key)
            time.sleep(interval)
    
    # Start the typing in a new thread
    running = True
    typing_thread = threading.Thread(target=type_key)
    typing_thread.start()
    result_label.config(text="Typing started")

# Function to stop the key press simulation
def stop_typing():
    global running
    running = False
    if typing_thread is not None:
        typing_thread.join()
    result_label.config(text="Typing stopped")

# Function to handle F6 key press
def on_press(event):
    if event.name == 'f6':
        if running:
            stop_typing()
        else:
            start_typing()

# Set up the listener for the F6 key
keyboard.on_press(on_press)

# Set up the GUI
root = tk.Tk()
root.title("Auto Typer")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Key to Press:").grid(column=1, row=1, sticky=(tk.W, tk.E))
key_entry = ttk.Entry(mainframe, width=10)
key_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Interval (ms):").grid(column=1, row=2, sticky=(tk.W, tk.E))
interval_entry = ttk.Entry(mainframe, width=10)
interval_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

start_button = ttk.Button(mainframe, text="Start", command=start_typing)
start_button.grid(column=1, row=3, sticky=tk.W)

stop_button = ttk.Button(mainframe, text="Stop", command=stop_typing)
stop_button.grid(column=2, row=3, sticky=tk.W)

result_label = ttk.Label(mainframe, text="")
result_label.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E))

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# Make the GUI Grid Flexible
for i in range(1, 5):
    mainframe.rowconfigure(i, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)

key_entry.focus()

root.mainloop()
