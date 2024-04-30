# NEXRAD File Grabber 
'''This program will ask a series of questions to identify the year, month, and day of NEXRAD data to download from the AWS S3 bucket.'''

import nexradaws, datetime, logging as log, os

log.basicConfig(
    filename='D:/Programming Projects/Weather/NEXRAD File Grabber/nexrad_downloader.log', 
    level=log.INFO, 
    format='%(asctime)s %(levelname)s: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S')


conn = conn = nexradaws.NexradAwsInterface()
path = 'D:/Programming Projects/Weather/NEXRAD File Grabber/NEXRAD Files'

def questionare():
    global radar, start, end

    log.info('Starting Questionare')

    print(conn.get_avail_years())
    year = input("Enter a year from the above list: ")
    if str(year) not in conn.get_avail_years():
        print(f"Error: {year} is not a valid year. Please try again.")
        log.error(f"Invalid year: {year}")
        raise ValueError("Invalid year")
    else:
        print(f"Your selected year: {year}")


    print(conn.get_avail_months(year))
    month = input("Enter a month from the above list: ")

    if str(month) not in conn.get_avail_months(year):
        print(f"Error: {month} is not a valid month in {year}. Please try again.")
        log.error(f"Invalid month: {month}")
        raise ValueError("Invalid month")
    else:
        print(f"Your selected month: {month}")

    print(conn.get_avail_days(year, month))
    day = input("Enter a day from the above list: ")
    if str(day) not in conn.get_avail_days(year, month):
        print(f"Error: {day} is not a valid day in {year}-{month}. Please try again.")
        log.error(f"Invalid day: {day}")
        raise ValueError("Invalid day")
    else:
        print(f"Your selected day: {day}")

    print(conn.get_avail_radars(year, month, day))
    radar = input("Enter a radar ID from the above list: ")
    if str(radar) not in conn.get_avail_radars(year, month, day):
        print(f"Error: {radar} is not a valid radar ID for {year}-{month}-{day}. Please try again.")
        log.error(f"Invalid radar ID: {radar}")
        raise ValueError("Invalid radar ID")
    else:
        print(f'Your selected radar: {radar}')

    start_time = input("Enter a start time (UTC) in the format HHMM: ")
    end_time = input("Enter an end time (UTC) in the format HHMM: ")
    start = datetime.datetime(int(year), int(month), int(day), int(start_time[:2]), int(start_time[2:]))
    end = datetime.datetime(int(year), int(month), int(day), int(end_time[:2]), int(end_time[2:]))

    return start, end, radar

def download_scans(start, end, radar):
    log.info(f'Downloading NEXRAD scans for {radar} from {start} to {end}')

    scan_list = conn.get_avail_scans_in_range(start, end, radar)
    for index, scan in enumerate(scan_list):
        print(f"{index}: {scan}")

    selected_scan_index = input("Enter the index of the scan you want to select: ")

    if ',' in selected_scan_index:
        selected_scan_index = selected_scan_index.split(',')
    elif ' ' in selected_scan_index:
        selected_scan_index = selected_scan_index.split()
    elif ', ' in selected_scan_index:
        selected_scan_index = selected_scan_index.split(', ')
    else:
        selected_scan_index = selected_scan_index

    for index in selected_scan_index:
        selected_scan = scan_list[int(index)]
        print(f"You selected scan: {selected_scan}")

        print('Downloading Scan')

        conn.download(selected_scan, path)
        print('Scan Downloaded')

        log.info('Download Complete')

def main():
    log.info('Starting Program')
    start, end, radar = questionare()
    download_scans(start, end, radar)

if __name__ == "__main__":
    main()