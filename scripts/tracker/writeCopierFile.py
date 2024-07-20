def writeSection(data_dict ,file):
    for section, options in data_dict.items():
            file.write(f"<{section}>\n")
            for key, value in options.items():
                if type(value) == dict:
                    temp = {
                        key: value
                    }
                    writeSection(temp, file)
                else:
                    file.write(f"{key}={value}\n")
            file.write(f"</{section}>\n")

def writeCopierFile(file_path, data_dict):
    with open(file_path, 'w') as file:
        for section, options in data_dict.items():
            if type(data_dict[section]) == dict:
                temp = {}
                temp[section] = data_dict[section]
                writeSection(temp, file)