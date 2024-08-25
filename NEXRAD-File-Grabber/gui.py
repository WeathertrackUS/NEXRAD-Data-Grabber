"""
The NEXRAD File Grabber Frontend is a graphical user interface (GUI) application built using the CustomTkinter library.
It allows users to select a year and month to download NEXRAD weather data files.

The `update_months` function updates the available months in the month dropdown based on the selected year.
It retrieves the available months from the `main.Question` class and updates the dropdown values accordingly.

The GUI consists of two frames: an input frame and an output frame.
The input frame contains a year dropdown, a year selection button, and a month dropdown.
The output frame is currently empty but could be used to display the downloaded files or other output.

The application is initialized with the CustomTkinter appearance mode set to "System" and the default color theme set to "blue".
The main window is set to a size of 800x600 pixels and titled "NEXRAD Downloader".
"""
# NEXRAD File Grabber Frontend
import customtkinter
import logging as log
import datetime
import threading
import main
import os
import CTkScrollableDropdown

log_directory = 'C:\\log'

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_directory, 'Nexrad_Downloader.log'),
    filemode='w'
)


def update_download_path(path):
    """
    Updates the download path with the provided path.

    Parameters:
        path (str): The new download path.

    Returns:
        None
    """
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
    """
    Updates the month dropdown menu based on the selected year.

    Retrieves the currently selected year from the year dropdown menu,
    clears the current month dropdown values, and populates it with available months for the selected year.
    The month dropdown menu is then updated and rearranged in the input frame.

    Parameters:
        None

    Returns:
        None
    """
    global month_dropdown  # skipcq: PYL-W0603
    year = year_dropdown.get()
    month_dropdown['values'] = []  # skipcq: PYL-E0601
    available_months = questions.get_available_months(year)
    month_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Month'] + available_months)
    CTkScrollableDropdown.CTkScrollableDropdown(month_dropdown, values=available_months)
    month_label.grid(row=1, column=0, padx=10, pady=10)
    month_dropdown.grid(row=1, column=1, padx=10, pady=10)
    month_button.grid(row=1, column=2, padx=10, pady=10)


def update_days():
    """
    Updates the day dropdown menu based on the selected year and month.

    Retrieves the currently selected year and month from the respective dropdown menus,
    clears the current day dropdown values, and populates it with available days for the
    selected year and month. The day dropdown menu is then updated and rearranged in the
    input frame.

    Parameters:
        None

    Returns:
        None
    """
    global day_dropdown  # skipcq: PYL-W0603
    year = year_dropdown.get()
    month = month_dropdown.get()
    day_dropdown['values'] = []  # skipcq: PYL-E0601
    available_days = questions.get_available_days(year, month)
    day_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Day'] + available_days)
    CTkScrollableDropdown.CTkScrollableDropdown(day_dropdown, values=available_days)
    day_label.grid(row=2, column=0, padx=10, pady=10)
    day_dropdown.grid(row=2, column=1, padx=10, pady=10)
    day_buttion.grid(row=2, column=2, padx=10, pady=10)


def update_radars():
    """
    Updates the list of available radar sites based on the selected year, month, and day.

    Retrieves the currently selected year, month, and day from the corresponding dropdown menus.
    Clears the current list of radar sites and populates it with the available radar sites for the selected date.
    Updates the radar site dropdown menu with the new list of available radar sites.

    Parameters:
        None

    Returns:
        None
    """
    global radar_dropdown  # skipcq: PYL-W0603
    year = year_dropdown.get()
    month = month_dropdown.get()
    day = day_dropdown.get()
    radar_dropdown['values'] = []  # skipcq: PYL-E0601
    available_radars = questions.get_available_radars(year, month, day)
    radar_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Radar Site'] + available_radars)
    CTkScrollableDropdown.CTkScrollableDropdown(radar_dropdown, values=available_radars)
    radar_label.grid(row=3, column=0, padx=10, pady=10)
    radar_dropdown.grid(row=3, column=1, padx=10, pady=10)
    radar_button.grid(row=3, column=2, padx=10, pady=10)


def generate_time_list():
    """
    Generate a list of times in the format 'HHMM' every 15 minutes from 0000 to 2345.

    Returns:
        list: A list of strings representing the times in the format 'HHMM'.
    """
    time_list = []
    for hour in range(24):
        for minute in range(0, 60, 15):  # Start at 0, end at 60, step by 15
            time_list.append(f"{hour:02d}{minute:02d}")  # Format as 'HHMM'
    time_list.append('2359')
    return time_list


def time_range_selection():
    """
    Selects a time range by creating dropdown menus for start and end times.

    Retrieves a list of available times from the generate_time_list function.
    Creates dropdown menus for selecting the start and end times, and populates them with the available times.
    Arranges the dropdown menus and their corresponding labels in the input frame.

    Parameters:
        None

    Returns:
        None
    """
    global start_time_dropdown, end_time_dropdown  # skipcq: PYL-W0603
    time_list = generate_time_list()
    start_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Start Time'])
    CTkScrollableDropdown.CTkScrollableDropdown(start_time_dropdown, values=time_list)
    end_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select End Time'])
    CTkScrollableDropdown.CTkScrollableDropdown(end_time_dropdown, values=time_list)
    start_time_label.grid(row=4, column=0, padx=10, pady=10)
    start_time_dropdown.grid(row=4, column=1, padx=10, pady=10)
    end_time_label.grid(row=5, column=0, padx=10, pady=10)
    end_time_dropdown.grid(row=5, column=1, padx=10, pady=10)


def find_scans():
    """
    Finds scans based on the selected year, month, day, start time, end time, and radar site.

    Retrieves the selected values from the dropdown menus and checks if all required fields are filled.
    If any field is empty, displays an error message and returns.

    If all fields are filled, creates a datetime object for the start and end times and uses the downloader to find available scans.
    If scans are found, generates a list of scan filenames and displays them in the output label.
    If no scans are found, displays a message indicating that no scans were found.

    Parameters:
        None

    Returns:
        None
    """
    output_label.grid_remove()
    output_label.grid_forget()

    year = year_dropdown.get()
    month = month_dropdown.get()
    day = day_dropdown.get()
    start_time = start_time_dropdown.get()
    end_time = end_time_dropdown.get()
    radar_site = radar_dropdown.get()

    if not year:  # skipcq: PYL-R1705
        log.error(selection_text[0])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[0])  # skipcq: PYL-W0621
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not month:  # skipcq: PYL-R1705
        log.error(selection_text[1])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[1])  # skipcq: PYL-W0621
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not day:  # skipcq: PYL-R1705
        log.error(selection_text[2])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[2])  # skipcq: PYL-W0621
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not radar_site:  # skipcq: PYL-R1705
        log.error(selection_text[3])
        status_label = customtkinter.CTkLabel(master=status_frame, text=selection_text[3])  # skipcq: PYL-W0621
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return
    elif not start_time or not end_time:  # skipcq: PYL-R1705
        log.error("Select Start/ End Time First")
        status_label = customtkinter.CTkLabel(master=status_frame, text="Select Start/ End Time First")  # skipcq: PYL-W0621
        status_label.grid(row=0, column=0, padx=10, pady=10)
        return

    start = datetime.datetime(int(year), int(month), int(day), int(start_time[:2]), int(start_time[2:]))
    end = datetime.datetime(int(year), int(month), int(day), int(end_time[:2]), int(end_time[2:]))

    available_scans = downloader.find_scans(start, end, radar_site)

    scan_strings = []

    if available_scans:
        # Clear the scan_strings list before generating the new list
        scan_strings.clear()

        output_label.configure(text="")

        # Add "0: Select All" to the beginning of the list
        scan_strings.append("0: Select All")

        # Add the new scan filenames to the list
        for i, scan in enumerate(available_scans, start=1):
            scan_strings.append(f"{i}: {scan.filename}")

        # Join the list of strings into a single string
        output_text = "\n".join(scan_strings)

        # Create a label to indicate the format of the output
        format_label = customtkinter.CTkLabel(master=output_frame, text="Index: File Name", wraplength=600)
        format_label.grid(row=0, column=1, padx=10, pady=10)

        # Display the output_text
        output_label.configure(text=output_text)
        output_label.grid(row=1, column=1, padx=10, pady=10)

        # Create a text box for the user to input the indexes
        index_input = customtkinter.CTkEntry(master=output_frame_2)
        index_input.grid(row=1, column=1, padx=10, pady=10)

        # Create a button to trigger the download process
        download_button = customtkinter.CTkButton(master=output_frame_2, text="Download Selected Scans",
                                                  command=lambda: start_download_thread(index_input.get(), available_scans))
        download_button.grid(row=2, column=1, padx=10, pady=10)
    else:
        output_label.configure(text="No available scans found for the selected criteria.")
        output_label.grid(row=0, column=1, padx=10, pady=10)


def start_download():
    """
    Starts the download process by resetting the progress bar and updating the status label.

    This function does not take any parameters and does not return any values.
    """
    status_label_2.grid_remove()
    progress_bar.set(0)
    status_label = customtkinter.CTkLabel(master=status_frame, text="Downloading Files...")  # skipcq: PYL-W0621
    status_label.grid(row=0, column=0, padx=10, pady=10)
    progress_bar.grid(row=2, column=0, padx=10, pady=10)


def update_progress_bar(progress):
    """
    Updates the progress bar with the given progress value.

    Args:
        progress (int): The progress value to be set on the progress bar.

    Returns:
        None
    """
    progress_bar.set(progress)


def start_download_thread(indexes, available_scans):
    """
    Starts a new thread to download the selected scans.

    Parameters:
        indexes (str): A string of comma-separated integers representing the indexes of the scans to download.
        available_scans (list): A list of available scans.

    Returns:
        None
    """
    download_thread = threading.Thread(target=download_scans, args=(indexes, available_scans))
    download_thread.start()


def download_scans(indexes, available_scans):
    """
    Downloads the selected scans from the available scans.

    Args:
        indexes (str): A string of comma-separated integers representing the indexes of the scans to be downloaded.
        available_scans (List[Scan]): A list of available scans.

    Returns:
        None

    Raises:
        None

    """
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
        status_label = customtkinter.CTkLabel(master=status_frame, text="ERROR: selected_scans is empty")  # skipcq: PYL-W0621
        status_label.grid(row=0, column=0, padx=10, pady=10)
        log.error('Selected Scans is None')


def download_complete(event, total_scans):
    """
    Handles the completion of a download event.

    Args:
        event: The download event object.
        total_scans: The total number of scans downloaded.

    Returns:
        None

    Raises:
        None
    """
    if event.is_set():
        output_label.configure(text="")
        progress_bar.stop()
        progress_bar.grid_remove()
        status_label = customtkinter.CTkLabel(master=status_frame, text="Download Complete!")  # skipcq: PYL-W0621
        status_label_2 = customtkinter.CTkLabel(master=status_frame, text=f"Completed {total_scans} downloads")  # skipcq: PYL-W0621
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
    """
    Opens a file dialog for the user to select an output path.

    This function uses tkinter's filedialog to prompt the user to select a directory.
    If a path is selected, it updates the output path entry field and sets the download path for the downloader.

    Parameters:
        None

    Returns:
        None
    """
    from tkinter import filedialog
    path = filedialog.askdirectory()
    if path:
        output_path_entry.delete(0, 'end')
        output_path_entry.insert(0, path)
        downloader.set_download_path(path)  # Update the download path


browse_button = customtkinter.CTkButton(master=path_frame, text="Browse", command=browse_output_path)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Input Frame
year_label = customtkinter.CTkLabel(master=input_frame, text="Select Year:")
year_label.grid(row=0, column=0, padx=10, pady=10)
year_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Year'] + questions.get_available_years())
CTkScrollableDropdown.CTkScrollableDropdown(year_dropdown, values=questions.get_available_years())
year_dropdown.grid(row=0, column=1, padx=10, pady=10)

year_button = customtkinter.CTkButton(master=input_frame, text="Select Year", command=lambda: update_months())  # skipcq: PYL-W0108
year_button.grid(row=0, column=2, padx=10, pady=10)

month_label = customtkinter.CTkLabel(master=input_frame, text="Select Month:")
month_label.grid(row=1, column=0, padx=10, pady=10)
month_dropdown = customtkinter.CTkComboBox(master=input_frame, values=["Select Year First"])
month_dropdown.grid(row=1, column=1, padx=10, pady=10)
month_button = customtkinter.CTkButton(master=input_frame, text="Select Month", command=lambda: update_days())  # skipcq: PYL-W0108
month_button.grid(row=1, column=2, padx=10, pady=10)

day_label = customtkinter.CTkLabel(master=input_frame, text="Select Day:")
day_label.grid(row=2, column=0, padx=10, pady=10)
day_dropdown = customtkinter.CTkComboBox(master=input_frame, values=["Select Month First"])
day_dropdown.grid(row=2, column=1, padx=10, pady=10)
day_buttion = customtkinter.CTkButton(master=input_frame, text="Select Day", command=lambda: update_radars())  # skipcq: PYL-W0108
day_buttion.grid(row=2, column=2, padx=10, pady=10)

radar_label = customtkinter.CTkLabel(master=input_frame, text="Select Radar:")
radar_label.grid(row=3, column=0, padx=10, pady=10)
radar_dropdown = customtkinter.CTkComboBox(master=input_frame, values=["Select Day First"])
radar_dropdown.grid(row=3, column=1, padx=10, pady=10)
radar_button = customtkinter.CTkButton(master=input_frame, text="Select Radar", command=lambda: time_range_selection())  # skipcq: PYL-W0108
radar_button.grid(row=3, column=2, padx=10, pady=10)

start_time_label = customtkinter.CTkLabel(master=input_frame, text="Start Time:")
start_time_label.grid(row=4, column=0, padx=10, pady=10)
start_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Radar First'])
start_time_dropdown.grid(row=4, column=1, padx=10, pady=10)

end_time_label = customtkinter.CTkLabel(master=input_frame, text="End Time:")
end_time_label.grid(row=5, column=0, padx=10, pady=10)
end_time_dropdown = customtkinter.CTkComboBox(master=input_frame, values=['Select Radar First'])
end_time_dropdown.grid(row=5, column=1, padx=10, pady=10)

find_scans_button = customtkinter.CTkButton(master=input_frame, text="Find Scans", command=lambda: find_scans())  # skipcq: PYL-W0108
find_scans_button.grid(row=6, column=0, columnspan=3, padx=50, pady=10)


# Output Frame
output_label = customtkinter.CTkLabel(master=output_frame, text="", wraplength=600)
output_label.grid(row=1, column=0, padx=10, pady=10)

progress_bar = customtkinter.CTkProgressBar(master=status_frame, determinate_speed=0.5)

status_label = customtkinter.CTkLabel(master=output_frame)

status_label_2 = customtkinter.CTkLabel(master=output_frame)

root.mainloop()
