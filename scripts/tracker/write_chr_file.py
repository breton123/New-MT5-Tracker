def write_chr_file(file_path, config):
    with open(file_path, 'w+') as file:
        file.write("<chart>\n")
        write_chart_section(file, config['chart'])
        file.write("</chart>\n")
        

def write_chart_section(file, chart):
    file.write(f"id={chart['id']}\n")
    file.write(f"symbol={chart['symbol']}\n")
    file.write(f"description={chart['description']}\n")
    file.write(f"period_type=0\n")
    file.write(f"period_size=1\n")
    file.write(f"digits=5\n")
    file.write(f"tick_size=0.000000\n")
    #file.write(f"position_time={chart['position_time']}\n")
    #file.write(f"scale_fix={chart['scale_fix']}\n")
    file.write("\n")
    write_expert_section(file, chart['expert'])
    write_window_section(file, chart['window'])

def write_expert_section(file, expert):
    file.write("<expert>\n")
    file.write(f"name={expert['name']}\n")
    file.write(f"path={expert['path']}\n")
    file.write(f"expertmode={expert['expertmode']}\n")
    write_inputs_section(file, expert['inputs'])
    file.write("</expert>\n\n")


def write_inputs_section(file, inputs):
    file.write("<inputs>\n=\n")
    for key, value in inputs.items():
        file.write(f"{key}={value}\n")
    file.write("</inputs>\n")


def write_window_section(file, window):
    file.write("<window>\n")
    write_indicator_section(file, window['indicator'])
    write_object_section(file, window['object'])
    file.write("</window>\n\n")


def write_indicator_section(file, indicator):
    file.write("<indicator>\n")
    for key, value in indicator.items():
        file.write(f"{key}={value}\n")
    file.write("</indicator>\n")

def write_object_section(file, obj):
    file.write("<object>\n")
    for key, value in obj.items():
        file.write(f"{key}={value}\n")
    file.write("</object>\n")