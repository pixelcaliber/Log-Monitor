import logging
import os
import time
from collections import deque
from typing import List, Deque, Any

class LogMonitor:
    """
    A class for monitoring log files and notifying observers of new log entries.

    This class implements the observer pattern to allow multiple listeners
    to be notified when new log lines are added to the monitored file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the LogMonitor instance.

        Args:
            file_path (str): The path to the log file to monitor.
        """
        self.file_path = file_path
        self.observers: List[Any] = []

    def get_last_lines(self, lines: int = 10) -> Deque[str]:
        """
        Retrieve the last n lines from the log file.

        Args:
            lines (int): The number of lines to retrieve. Defaults to 10.

        Returns:
            Deque[str]: A deque containing the last n lines of the log file.
        """
        with open(self.file_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            data_queue: Deque[str] = deque()
            temp = ""

            while size > 0 and len(data_queue) < lines:
                size -= 1
                f.seek(size)
                new_byte = f.read(1)
                temp = new_byte.decode("utf-8") + temp
                if new_byte == b"\n":
                    data_queue.appendleft(temp)
                    temp = ""

            if temp:
                data_queue.appendleft(temp)

            return data_queue

    def register_observer(self, observer: Any) -> None:
        """
        Register a new observer to be notified of log updates.

        Args:
            observer (Any): The observer object to register.
        """
        self.observers.append(observer)

    def unregister_observer(self, observer: Any) -> None:
        """
        Unregister an observer from receiving log updates.

        Args:
            observer (Any): The observer object to unregister.
        """
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, line: str) -> None:
        """
        Notify all registered observers of a new log line.

        Args:
            line (str): The new log line to notify observers about.
        """
        logging.info(f"New log line: {line.strip()}")
        for observer in self.observers:
            observer.update(line)

    def tail_log(self) -> None:
        """
        Continuously monitor the log file for new entries and notify observers.

        This method runs indefinitely, sleeping for short intervals when no new
        lines are available.
        """
        with open(self.file_path, "r") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    self.notify_observers(line)
                else:
                    time.sleep(0.1)