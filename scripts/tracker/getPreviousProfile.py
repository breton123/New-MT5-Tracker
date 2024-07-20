from scripts.tracker.read_ini_file import read_ini_file


def getPreviousProfile(file_path):
    terminal_config = read_ini_file(file_path)
    if terminal_config is None:
        return "MT5-Tracker-Profile"
    if "Charts" in terminal_config:
        return terminal_config["Charts"]["ProfileLast"]
    else:
        return "MT5-Tracker-Profile"