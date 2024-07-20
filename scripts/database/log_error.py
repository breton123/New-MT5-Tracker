from datetime import datetime
import os
import portalocker

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def log_error(error_message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{current_time}] {error_message}\n"
    try:
        log_file_path = os.path.join(databaseFolder, "errorlog.txt")
        with open(log_file_path, "a") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                file.write(log_entry)
            finally:
                portalocker.unlock(file)
    except portalocker.LockException as e:
        print(f"Task: (Log Error)  Failed to acquire lock: {e}")
    except IOError as e:
        print(f"Task: (Log Error)  Failed to write to log file: {e}")
