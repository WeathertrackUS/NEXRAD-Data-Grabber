"""
The NEXRAD File Grabber Frontend is a graphical user interface (GUI) application built using the CustomTkinter library. It allows users to select a year and month to download NEXRAD weather data files.

The `update_months` function updates the available months in the month dropdown based on the selected year. It retrieves the available months from the `main.Question` class and updates the dropdown values accordingly.

The GUI consists of two frames: an input frame and an output frame. The input frame contains a year dropdown, a year selection button, and a month dropdown. The output frame is currently empty but could be used to display the downloaded files or other output.

The application is initialized with the CustomTkinter appearance mode set to "System" and the default color theme set to "blue". The main window is set to a size of 800x600 pixels and titled "NEXRAD Downloader".
"""
# NEXRAD File Grabber Frontend
import customtkinter, tkinter as ttk, logging as log, datetime, time, threading, main, os, concurrent.futures
from CTkScrollableDropdown import *

log_directory = 'C:\\log'

if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
log.basicConfig(
    level = log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_directory, 'Nexrad_Downloader.log'),
    filemode='w'
)

def update_download_path(path):
    # This function will be called with the new download path
    # You can update the GUI or perform other actions here
    print(f"Download path set to: {path}")


downloader = main.NexradDownloader(update_download_path)
questions = main.Question()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("540x800")
root.title("NEXRAD Downloader")

available_months = []
selection_text = ['Select Year First', 'Select Month First', 'Select Day First', 'Select Radar Site First']

# Create a global event object
download_event = threading.Event()

# Frames
path_frame = customtkinter.CTkFrame(master=root)
path_frame.grid(row=0, column=0, pady=10, padx=10, columnspan=2)

input_frame = customtkinter.CTkFrame(master=root)
input_frame.grid(row=1, column=0, pady=20, padx=60, columnspan=2)

output_frame = customtkinter.CTkScrollableFrame(master=root, width=230)
output_frame.grid(row=2, column=0, pady=10, padx=10)

output_frame_2 = customtkinter.CTkFrame(master=root, width=230)
output_frame_2.grid(row=2, column=1, pady=10, padx=10)

status_frame = customtkinter.CTkFrame(master=root, width=510, height=45)
status_frame.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

# Functions

def update_months():
    global month_dropdown
    year = year_dropdown.get()
    month_dropdown['values'] = [] # Clear the current values
    available_months = questions.get_available_months(year)
    month_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Month'] + available_months)
    CTkScrollableDropdown(month_dropdown, values=available_months)
    month_label.grid(row=1, column=0, padx=10, pady=10)
    month_dropdown.grid(row=1, column=1, padx=10, pady=10)
    month_button.grid(row=1, column=2, padx=10, pady=10)

def update_days():
    global day_dropdown
    year = year_dropdown.get()
    month = month_dropdown.get()
    day_dropdown['values'] = [] # Clear the current values
    available_days = questions.get_available_days(year, month)
    day_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Day'] + available_days)
    CTkScrollableDropdown(day_dropdown, values=available_days)
    day_label.grid(row=2, column=0, padx=10, pady=10)
    day_dropdown.grid(row=2, column=1, padx=10, pady=10)
    day_buttion.grid(row=2, column=2, padx=10, pady=10)

def update_radars():
    global radar_dropdown
    year = year_dropdown.get()
    month = month_dropdown.get()
    day = day_dropdown.get()
    radar_dropdown['values'] = [] # Clear the current values
    available_radars = questions.get_available_radars(year, month, day)
    radar_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Radar Site'] + available_radars)
    CTkScrollableDropdown(radar_dropdown, values=available_radars)
    radar_label.grid(row=3, column=0, padx=10, pady=10)
    radar_dropdown.grid(row=3, column=1, padx=10, pady=10)
    radar_button.grid(row=3, column=2, padx=10, pady=10)

def generate_time_list():
    """Generate a list of times in the format 'HHMM' every 15 minutes from 0000 to 2345."""
    time_list = []
    for hour in range(24):
        for minute in range(0, 60, 15): # Start at 0, end at 60, step by 15
            time_list.append(f"{hour:02d}{minute:02d}") # Format as 'HHMM'
    time_list.append('2359')
    return time_list

def time_range_selection():
    global start_time_dropdown, end_time_dropdown
    time_list = generate_time_list()
    start_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Start Time'])
    CTkScrollableDropdown(start_time_dropdown, values=time_list)
    end_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select End Time'])
    CTkScrollableDropdown(end_time_dropdown, values=time_list)
    start_time_label.grid(row=4, column=0, padx=10, pady=10)
    start_time_dropdown.grid(row=4, column=1, padx=10, pady=10)
    end_time_label.grid(row=5, column=0, padx=10, pady=10)
    end_time_dropdown.grid(row=5, column=1, padx=10, pady=10)

def find_scans():
    output_label = customtkinter.CTkLabel(master=output_frame, text="")
    year = year_dropdown.get()
    month = month_dropdown.get()
    day = day_dropdown.get()
    start_time = start_time_dropdown.get()
    end_time = end_time_dropdown.get()
    radar_site = radar_dropdown.get()

    if not year:
        log.error(selection_text[0])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[0])
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not month:
        log.error(selection_text[1])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[1])
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not day:
        log.error(selection_text[2])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[2])
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not radar_site:
        log.error(selection_text[3])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[3])
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not start_time or not end_time:
        log.error("Select Start/ End Time First")
        status_label = customtkinter.CTkLabel(master=status_frame, text="Select Start/ End Time First")
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return

    start = datetime.datetime(int(year), int(month), int(day), int(start_time[:2]), int(start_time[2:]))
    end = datetime.datetime(int(year), int(month), int(day), int(end_time[:2]), int(end_time[2:]))

    available_scans = downloader.find_scans(start, end, radar_site)

    if available_scans:
        # Convert each AwsNexradFile object to a string representation with index
        scan_strings = [f"{i}: {scan.filename}" for i, scan in enumerate(available_scans, start=1)]
        scan_strings.insert(0, "0: Select All") # Add "Select All" at the beginning
        
        # Join the list of strings into a single string
        output_text = "\n".join(scan_strings)

        # Create a label to indicate the format of the output
        format_label = customtkinter.CTkLabel(master=output_frame, text="Index: File Name", wraplength=600)
        format_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Display the output_text
        output_label = customtkinter.CTkLabel(master=output_frame, text=output_text, wraplength=600)
        output_label.grid(row=1, column=1, padx=10, pady=10)
        
        # Create a text box for the user to input the indexes
        index_input = customtkinter.CTkEntry(master=output_frame_2)
        index_input.grid(row=1, column=1, padx=10, pady=10)
        
        # Create a button to trigger the download process
        download_button = customtkinter.CTkButton(master=output_frame_2, text="Download Selected Scans", command=lambda: start_download_thread(index_input.get(), available_scans))
        download_button.grid(row=2, column=1, padx=10, pady=10)
    else:
        output_label = customtkinter.CTkLabel(master=output_frame, text="No available scans found for the selected criteria.", wraplength=600)
        output_label.grid(row=0, column=1, padx=10, pady=10)

def start_download():
    status_label_2.grid_remove() 
    progress_bar.set(0)
    status_label = customtkinter.CTkLabel(master=status_frame, text="Downloading Files...")
    status_label.grid(row=0, column=0, padx=10, pady=10)
    progress_bar.grid(row=2, column=0, padx=10, pady=10)

def update_progress_bar(progress):
    progress_bar.set(progress)

def start_download_thread(indexes, available_scans):
    download_thread = threading.Thread(target=download_scans, args=(indexes, available_scans))
    download_thread.start()

def download_scans(indexes, available_scans):
    log.info('Starting Download')
    start_download()

    # Reset the download_event
    download_event.clear()

    # Check if "Select All" is selected
    if indexes == '0':
        selected_scans = available_scans
    else:
        # Assuming indexes is a string of comma-separated integers
        selected_indexes = [int(index) for index in indexes.split(',')]
        selected_scans = [scan for i, scan in enumerate(available_scans, start=1) if i in selected_indexes]
    
    log.info(selected_scans)
    if len(selected_scans) != 0:
        # Trigger the download process for the selected scans in a separate thread
        log.info('Downloading')
        total_scans = len(selected_scans)
        downloader.download_scans(selected_scans, download_event, download_complete, total_scans, update_progress_bar)
    else:
        status_label = customtkinter.CTkLabel(master=status_frame, text="ERROR: selected_scans is empty")
        status_label.grid(row=0, column=0, padx=10, pady=10)
        log.error('Selected Scans is None')

def download_complete(event, total_scans):
    if event.is_set():
        progress_bar.stop()
        progress_bar.grid_remove()
        status_label = customtkinter.CTkLabel(master=status_frame, text="Download Complete!")
        status_label_2 = customtkinter.CTkLabel(master=status_frame, text=f"Completed {total_scans} downloads")
        status_label.grid(row=0, column=0, padx=10, pady=10)
        status_label_2.grid(row=1, column=0, padx=10, pady=10)

# Path Frame
# Output Path Selection
output_path_label = customtkinter.CTkLabel(master=path_frame, text="Output Path:")
output_path_label.grid(row=0, column=0, padx=10, pady=10)

output_path_entry = customtkinter.CTkEntry(master=path_frame)
output_path_entry.grid(row=0, column=1, padx=10, pady=10)

# Browse Button for Output Path
def browse_output_path():
    from tkinter import filedialog
    path = filedialog.askdirectory()
    if path:
        output_path_entry.delete(0, 'end')
        output_path_entry.insert(0, path)
        downloader.set_download_path(path) # Update the download path

browse_button = customtkinter.CTkButton(master=path_frame, text="Browse", command=browse_output_path)
browse_button.grid(row=0, column=2, padx=10, pady=10)
    
# Input Frame
year_label = customtkinter.CTkLabel(master=input_frame, text="Select Year:")
year_label.grid(row=0, column=0, padx=10, pady=10)
year_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Year'] + questions.get_available_years())
CTkScrollableDropdown(year_dropdown, values=questions.get_available_years())
year_dropdown.grid(row=0, column=1, padx=10, pady=10)

year_button = customtkinter.CTkButton(master=input_frame, text="Select Year", command=lambda: update_months()) 
year_button.grid(row=0, column=2, padx=10, pady=10)

month_label = customtkinter.CTkLabel(master=input_frame, text="Select Month:")
month_label.grid(row=1, column=0, padx=10, pady=10)
month_dropdown = customtkinter.CTkComboBox(master=input_frame, values=["Select Year First"]) 
month_dropdown.grid(row=1, column=1, padx=10, pady=10)
month_button = customtkinter.CTkButton(master=input_frame, text="Select Month", command=lambda: update_days()) 
month_button.grid(row=1, column=2, padx=10, pady=10)

day_label = customtkinter.CTkLabel(master=input_frame, text="Select Day:")
day_label.grid(row=2, column=0, padx=10, pady=10)
day_dropdown = customtkinter.CTkComboBox(master=input_frame, values=["Select Month First"]) 
day_dropdown.grid(row=2, column=1, padx=10, pady=10)
day_buttion = customtkinter.CTkButton(master=input_frame, text="Select Day", command=lambda: update_radars()) 
day_buttion.grid(row=2, column=2, padx=10, pady=10)

radar_label = customtkinter.CTkLabel(master=input_frame, text="Select Radar:")
radar_label.grid(row=3, column=0, padx=10, pady=10)
radar_dropdown = customtkinter.CTkComboBox(master=input_frame, values=["Select Day First"]) 
radar_dropdown.grid(row=3, column=1, padx=10, pady=10)
radar_button = customtkinter.CTkButton(master=input_frame, text="Select Radar", command=lambda: time_range_selection()) 
radar_button.grid(row=3, column=2, padx=10, pady=10)

start_time_label = customtkinter.CTkLabel(master=input_frame, text="Start Time:")
start_time_label.grid(row=4, column=0, padx=10, pady=10)
start_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Radar First']) 
start_time_dropdown.grid(row=4, column=1, padx=10, pady=10)

end_time_label = customtkinter.CTkLabel(master=input_frame, text="End Time:")
end_time_label.grid(row=5, column=0, padx=10, pady=10)
end_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Radar First']) 
end_time_dropdown.grid(row=5, column=1, padx=10, pady=10)

find_scans_button = customtkinter.CTkButton(master=input_frame, text="Find Scans", command=lambda: find_scans()) 
find_scans_button.grid(row=6, column=0, columnspan=3, padx=50, pady=10)


# Output Frame
output_label = customtkinter.CTkLabel(master=output_frame, text="", wraplength=600)

progress_bar = customtkinter.CTkProgressBar(master=status_frame, determinate_speed=0.5)

status_label = customtkinter.CTkLabel(master=output_frame)

status_label_2 = customtkinter.CTkLabel(master=output_frame)


root.mainloop()
