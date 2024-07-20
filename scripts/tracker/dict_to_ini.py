
def dict_to_ini(data):
    lines = []
    
    for section, contents in data.items():
        lines.append(f"<{section}>")
        for key, value in contents.items():
            if isinstance(value, dict):
                if key == 'inputs':
                    lines.append("<inputs>")
                    for subkey, subcontents in value.items():
                        lines.append(f"{subkey}==== {subkey.replace('s_', '').replace('_', ' ')} ===")
                        for subsubkey, subsubvalue in subcontents.items():
                            lines.append(f"{subsubkey}={subsubvalue}")
                    lines.append("</inputs>")
                else:
                    for subkey, subvalue in value.items():
                        lines.append(f"{subkey}={subvalue}")
            else:
                lines.append(f"{key}={value}")
        lines.append(f"</{section}>")

    return "\n".join(lines)