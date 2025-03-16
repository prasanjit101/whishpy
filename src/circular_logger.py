import logging
import os
import sys
import threading
import asyncio
from datetime import datetime
from queue import Queue
from pathlib import Path

class CircularLogger:
    def __init__(self, max_size=1024*90, log_file=None):  # 90kb default
        if log_file is None:
            # Use appropriate log path for both development and bundled app
            if getattr(sys, 'frozen', False):
                # Running in py2app bundle
                log_file = Path.home() / '.whishpy' / 'whishpy.log'
            else:
                # Running in development
                log_file = 'whishpy.log'
        self.max_size = max_size
        self.log_file = log_file
        self.buffer = []
        self.current_size = 0
        self.lock = threading.Lock()
        self.write_queue = Queue()
        self.writer_thread = threading.Thread(target=self._file_writer, daemon=True)
        self.writer_thread.start()
        
    def _log(self, level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        entry_size = len(log_entry.encode('utf-8'))
        
        with self.lock:
            # Check if adding this entry would exceed max size
            if self.current_size + entry_size > self.max_size:
                # Remove oldest entries until we have space
                while self.buffer and (self.current_size + entry_size > self.max_size):
                    removed = self.buffer.pop(0)
                    self.current_size -= len(removed.encode('utf-8'))
            
            self.buffer.append(log_entry)
            self.current_size += entry_size
            self.write_queue.put(log_entry)
    
    def debug(self, message):
        self._log('DEBUG', message)
    
    def info(self, message):
        self._log('INFO', message)
    
    def warning(self, message):
        self._log('WARNING', message)
    
    def error(self, message):
        self._log('ERROR', message)
    
    def get_logs(self):
        with self.lock:
            return ''.join(self.buffer)
    
    def clear_logs(self):
        with self.lock:
            self.buffer = []
            self.current_size = 0
    
    def _file_writer(self):
        """Background thread that writes logs to file"""
        while True:
            log_entry = self.write_queue.get()
            try:
                with open(self.log_file, 'a') as f:
                    f.write(log_entry)
                    # Check file size and rotate if needed
                    if os.path.getsize(self.log_file) > self.max_size:
                        self._rotate_log()
            except Exception as e:
                print(f"Error writing to log file: {e}")
            finally:
                self.write_queue.task_done()
    
    def _rotate_log(self):
        """Rotate the log file when it reaches max size"""
        try:
            with self.lock:
                if os.path.exists(self.log_file):
                    # Create backup of current log
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_file = f"{self.log_file}.{timestamp}"
                    os.rename(self.log_file, backup_file)
                    
                    # Write remaining buffer to new log file
                    with open(self.log_file, 'w') as f:
                        f.write(''.join(self.buffer))
        except Exception as e:
            print(f"Error rotating log file: {e}")

# Create a global logger instance
logger = CircularLogger()

def setup_logging():
    # Configure standard logging to use our circular logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[CircularLogHandler()]
    )

class CircularLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logger._log(record.levelname, log_entry)

    def close(self):
        # Wait for all queued logs to be written before closing
        logger.write_queue.join()
        super().close()
