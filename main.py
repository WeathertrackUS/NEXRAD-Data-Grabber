# NEXRAD File Grabber Backend
'''This program will ask a series of questions to identify the year, month, and day of NEXRAD data to download from the AWS S3 bucket.'''

import nexradaws, datetime, logging as log, os, time, concurrent.futures, threading

conn = conn = nexradaws.NexradAwsInterface()
path = os.path.dirname(os.path.abspath(__file__))

log_directory = 'C:\\log'

if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
log.basicConfig(
    level = log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_directory, 'Nexrad_Downloader.log'),
    filemode='w'
)

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
    def __init__(self, set_path_callback):
        self.conn = conn
        self.path = path # Initialize path as None
        self.set_path_callback = set_path_callback # Store the callback

    def set_download_path(self, path):
        self.path = path # Set the download path
        if self.set_path_callback:
            self.set_path_callback(path) # Call the callback with the new path

    def find_scans(self, start, end, radar):
        log.info(f'Searching for NEXRAD scans for {radar} from {start} to {end}')
        scan_list = self.conn.get_avail_scans_in_range(start, end, radar)
        log.info(f'Scan List: {scan_list}')
        return scan_list

    def download_scans(self, scans, download_event, download_complete_callback, total_downloads, progress_callback):
        self.completed_downloads = 0
        self.total_downloads = total_downloads
        self.download_event = download_event
        self.download_complete_callback = download_complete_callback
        self.progress_callback = progress_callback
        
        if self.path == os.path.dirname(os.path.abspath(__file__)):
            if not os.path.exists(self.path):
                os.makedirs(self.path)

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self._download_scan, scan) for scan in scans]
            for future in concurrent.futures.as_completed(futures):
                future.result()

    def _download_scan(self, scan):
        log.info(f'Downloading NEXRAD scan: {scan.filename}')
        self.conn.download(scan, self.path)
        log.info('Download Complete')
        log.info(f'File can be found at: {self.path}')
        self.completed_downloads += 1
        self.download_progress = self.completed_downloads / self.total_downloads

        if self.completed_downloads == self.total_downloads:
            log.info(f"completed scans {self.completed_downloads}/{self.total_downloads}")
            log.info(f"Download progress: {self.download_progress * 100:.2f}%")
            print(f"completed scans {self.completed_downloads}/{self.total_downloads}")
            print(f"Download progress: {self.download_progress * 100:.2f}%")
            self.download_event.set()
            self.download_complete_callback(self.download_event, self.total_downloads)
        else:
            log.info(f"completed scans {self.completed_downloads}/{self.total_downloads}")
            print(f"completed scans {self.completed_downloads}/{self.total_downloads}")
            print(f"Download progress: {self.download_progress * 100:.2f}%")
            # Introduce a delay of 2 seconds before the next download
            time.sleep(2)

            # Call the progress_callback from the main thread
            threading.Thread(target=self.progress_callback, args=(self.download_progress,)).start()

        return scan.filename