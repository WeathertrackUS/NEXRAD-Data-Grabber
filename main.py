import nexradaws, datetime

conn = conn = nexradaws.NexradAwsInterface()
path = 'D:/Programming Projects/Weather/NEXRAD File Grabber/NEXRAD Files'

print(conn.get_avail_years())
year = input("Enter a year from the above list: ")
if str(year) not in conn.get_avail_years():
    print(f"Error: {year} is not a valid year. Please try again.")
    exit()
else:
    print(f"Your selected year: {year}")


print(conn.get_avail_months(year))
month = input("Enter a month from the above list: ")

if str(month) not in conn.get_avail_months(year):
    print(f"Error: {month} is not a valid month in {year}. Please try again.")
    exit()
else:
    print(f"Your selected month: {month}")

print(conn.get_avail_days(year, month))
day = input("Enter a day from the above list: ")
if str(day) not in conn.get_avail_days(year, month):
    print(f"Error: {day} is not a valid day in {year}-{month}. Please try again.")
    exit()
else:
    print(f"Your selected day: {day}")

print(conn.get_avail_radars(year, month, day))
radar = input("Enter a radar ID from the above list: ")
if str(radar) not in conn.get_avail_radars(year, month, day):
    print(f"Error: {radar} is not a valid radar ID for {year}-{month}-{day}. Please try again.")
    exit()
else:
    print(f'Your selected radar: {radar}')

start_time = input("Enter a start time (UTC) in the format HHMM: ")
end_time = input("Enter an end time (UTC) in the format HHMM: ")
start = datetime.datetime(int(year), int(month), int(day), int(start_time[:2]), int(start_time[2:]))
end = datetime.datetime(int(year), int(month), int(day), int(end_time[:2]), int(end_time[2:]))

scan_list = conn.get_avail_scans_in_range(start, end, radar)
for index, scan in enumerate(scan_list):
    print(f"{index}: {scan}")

selected_scan_index = input("Enter the index of the scan you want to select: ")
if not selected_scan_index.isdigit() or int(selected_scan_index) >= len(scan_list):
    print("Invalid index. Please try again.")
    exit()

selected_scan = scan_list[int(selected_scan_index)]
print(f"You selected scan: {selected_scan}")

conn.download(selected_scan, path)
print('Scan Downloaded')