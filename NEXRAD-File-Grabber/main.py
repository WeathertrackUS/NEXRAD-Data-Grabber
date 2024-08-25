# NEXRAD File Grabber Backend
# This program will ask a series of questions to identify the year, month, and day of NEXRAD data to download from the AWS S3 bucket.

import nexradaws
import datetime
import logging as log
import os
import time
import concurrent.futures
import threading

conn = nexradaws.NexradAwsInterface()
path = os.path.dirname(os.path.abspath(__file__))

log_directory = 'C:\\log'

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_directory, 'Nexrad_Downloader.log'),
    filemode='w'
)


class Question:
    def __init__(self):
        """
        Initializes a Question instance.

        Args:
            None

        Returns:
            None
        """
        self.conn = conn


    def get_available_years(self):
        """
        Returns a list of available years.

        Args:
            None

        Returns:
            list: A list of available years.
        """
        return self.conn.get_avail_years()


    def get_available_months(self, year):
        """
        Returns a list of available months for a given year.

        Args:
            year (int): The year for which to retrieve available months.

        Returns:
            list: A list of available months.
        """
        return self.conn.get_avail_months(year)


    def get_available_days(self, year, month):
        """
        Returns a list of available days for a given year and month.

        Args:
            year (int): The year for which to retrieve available days.
            month (int): The month for which to retrieve available days.

        Returns:
            list: A list of available days.
        """
        return self.conn.get_avail_days(year, month)


    def get_available_radars(self, year, month, day):
        """
        Returns a list of available radar sites for a given date.

        Args:
            year (int): The year of the date.
            month (int): The month of the date.
            day (int): The day of the date.

        Returns:
            list: A list of available radar sites.
        """
        return self.conn.get_avail_radars(year, month, day)


    @staticmethod
    def get_time_range(year, month, day):
        """
        Returns a tuple of two datetime objects representing the start and end of a given day.

        Args:
            year (int): The year of the date.
            month (int): The month of the date.
            day (int): The day of the date.

        Returns:
            tuple: A tuple containing two datetime objects. The first is the start of the day (00:00:00) and the second is the end of the day (23:59:59).
        """
        start = datetime.datetime(int(year), int(month), int(day), 0, 0, 0)
        end = datetime.datetime(int(year), int(month), int(day), 23, 59, 59)
        return start, end


class NexradDownloader:
    def __init__(self, set_path_callback):
        """
        Initializes a NexradDownloader instance.

        Args:
            set_path_callback (function): A callback function to be called when the download path is set.

        Returns:
            None
        """
        self.progress_callback = None
        self.download_complete_callback = None
        self.download_event = None
        self.total_downloads = None
        self.completed_downloads = None
        self.conn = conn
        self.path = path  # Initialize path as None
        self.set_path_callback = set_path_callback  # Store the callback


    def set_download_path(self, output_path):
        """
        Sets the download path for the NexradDownloader instance.

        Args:
            output_path (str): The path where the downloaded files will be saved.

        Returns:
            None
        """
        self.path = output_path  # Set the download path
        if self.set_path_callback:
            self.set_path_callback(path)  # Call the callback with the new path


    def find_scans(self, start, end, radar):
        """
        Finds NEXRAD scans within a specified time range for a given radar site.

        Args:
            start (datetime): The start time of the scan range.
            end (datetime): The end time of the scan range.
            radar (str): The radar site to search for scans.

        Returns:
            list: A list of available scans for the specified radar site and time range.
        """
        log.info(f'Searching for NEXRAD scans for {radar} from {start} to {end}')  # skipcq: PYL-W1203
        scan_list = self.conn.get_avail_scans_in_range(start, end, radar)
        log.info(f'Scan List: {scan_list}')
        return scan_list


    def download_scans(self, scans, download_event, download_complete_callback, total_downloads, progress_callback):
        """
        Downloads a list of NEXRAD scans concurrently using a thread pool.

        Args:
            scans (list): A list of scans to be downloaded.
            download_event: An event object to signal the start of the download process.
            download_complete_callback (function): A callback function to be called when the download is complete.
            total_downloads (int): The total number of scans to be downloaded.
            progress_callback (function): A callback function to report the download progress.

        Returns:
            None
        """
        self.completed_downloads = 0
        self.total_downloads = total_downloads
        self.download_event = download_event
        self.download_complete_callback = download_complete_callback
        self.progress_callback = progress_callback

        if self.path == os.path.dirname(os.path.abspath(__file__)) and not os.path.exists(self.path):
            os.makedirs(self.path)

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self._download_scan, scan) for scan in scans]
            for future in concurrent.futures.as_completed(futures):
                future.result()


    def download_scan(self, scan):
        """
        Downloads a single NEXRAD scan.

        Args:
            scan: The scan object to be downloaded.

        Returns:
            str: The filename of the downloaded scan.

        Notes:
            This function logs the download progress and updates the download event.
            If the download is complete, it calls the download_complete_callback.
            Otherwise, it calls the progress_callback and introduces a delay before the next download.
        """
        log.info(f'Downloading NEXRAD scan: {scan.filename}')  # skipcq: PYL-W1203
        self.conn.download(scan, self.path)
        log.info('Download Complete')
        log.info(f'File can be found at: {self.path}')  # skipcq: PYL-W1203
        self.completed_downloads += 1
        self.download_progress = self.completed_downloads / self.total_downloads  # skipcq: PYL-W0201

        if self.completed_downloads == self.total_downloads:
            log.info(f'Download Complete. Completed Scans: {self.completed_downloads}')  # skipcq: PYL-W1203
            log.info(f'Download progress: {self.download_progress * 100:.2f}%')  # skipcq: PYL-W1203
            print(f'completed scans {self.completed_downloads}/{self.total_downloads}')
            print(f'Download progress: {self.download_progress * 100:.2f}%')
            self.download_event.set()
            self.download_complete_callback(self.download_event, self.total_downloads)
        else:
            log.info(f"completed scans {self.completed_downloads}/{self.total_downloads}")  # skipcq: PYL-W1203
            print(f"completed scans {self.completed_downloads}/{self.total_downloads}")
            print(f"Download progress: {self.download_progress * 100:.2f}%")
            # Introduce a delay of 2 seconds before the next download
            time.sleep(2)

            # Call the progress_callback from the main thread
            threading.Thread(target=self.progress_callback, args=(self.download_progress,)).start()

        return scan.filename
