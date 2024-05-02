# NEXRAD File Grabber Backend
'''This program will ask a series of questions to identify the year, month, and day of NEXRAD data to download from the AWS S3 bucket.'''

import nexradaws, datetime, logging as log, os, time

log.basicConfig(
    filename='D:/Programming Projects/Weather/NEXRAD File Grabber/nexrad_downloader.log', 
    level=log.INFO, 
    format='%(asctime)s %(levelname)s: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S')


conn = conn = nexradaws.NexradAwsInterface()
path = 'D:/Programming Projects/Weather/NEXRAD File Grabber/NEXRAD Files'

class Question:
    def __init__(self):
        self.conn = conn

    def get_available_years(self):
        return self.conn.get_avail_years()
    
    def get_available_months(self, year):
        return self.conn.get_avail_months(year)
    
    def get_available_days(self, year, month):
        return self.conn.get_avail_days(year, month)
    
    def get_available_radars(self, year, month, day):
        return self.conn.get_avail_radars(year, month, day)
    
    def get_time_range(self, year, month, day):
        start = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
        end = datetime.datetime(int(year), int(month), int(day), 23, 59, 59)
        return start, end

class NexradDownloader:
    def __init__(self):
        self.conn = conn
        self.path = path

    def find_scans(self, start, end, radar):
        log.info(f'Searching for NEXRAD scans for {radar} from {start} to {end}')
        scan_list = self.conn.get_avail_scans_in_range(start, end, radar)
        log.info(f'Scan List: {scan_list}')
        return scan_list

    def download_scans(self, scan, start_download_callback, download_complete_callback):
        log.info(f'Downloading NEXRAD scan: {scan.filename}')
        start_download_callback() # Call the start_download function
        conn.download(scan, self.path)
        log.info('Download Complete')
        download_complete_callback() # Call the download_complete function

