import os
import portalocker

user_profile = os.environ['USERPROFILE']
databaseFolder = os.path.join(user_profile, 'AppData', 'Local', 'Mt5TrackerDatabase')


def getErrorLog():
    log_file_path = os.path.join(databaseFolder, "errorlog.txt")
    try:
        with open(log_file_path, "r") as file:
            try:
                portalocker.lock(file, portalocker.LOCK_EX)
                error_log = file.read()
            finally:
                portalocker.unlock(file)
        return error_log
    except FileNotFoundError:
        print(f"Error log file '{log_file_path}' not found.")
        return ""
    except IOError as e:
        print(f"Failed to read error log file: {e}")
        return ""
    except portalocker.LockException as e:
        print(f"Failed to acquire lock on error log file: {e}")
        return ""