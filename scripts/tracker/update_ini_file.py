
from scripts.tracker.read_ini_file import read_ini_file


def update_ini_file(file_path, profile_name):
    terminal_config = read_ini_file(file_path)
    
    if terminal_config is None:
        print("Failed to read the INI file.")
        return
    
    if "Charts" in terminal_config:
        terminal_config["Charts"]["ProfileLast"] = profile_name
    else:
        terminal_config.add_section("Charts")
        terminal_config["Charts"]["ProfileLast"] = profile_name
    
    if not terminal_config.has_section("Experts"):
        terminal_config.add_section("Experts")
    
    terminal_config["Experts"]["enabled"] = "1"
    terminal_config["Experts"]["allowdllimport"] = "1"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as configfile:
            terminal_config.write(configfile)
    except Exception as e:
        print(f"An error occurred while writing to the INI file: {e}")
