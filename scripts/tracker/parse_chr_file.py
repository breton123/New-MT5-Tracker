
def parse_chr_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    config = {
        'chart': {
            'expert': {
                'inputs': {}
            },
            'window': {
                'indicator': {},
                'object': {}
            }
        }
    }

    current_section = None  # Track the current section we are parsing
    current_inputs = None   # Track if we are in the 'inputs' section

    for line in lines:
        line = line.strip()
        if line.startswith('<chart>'):
            current_section = 'chart'
        elif line.startswith('<expert>'):
            current_section = 'expert'
        elif line.startswith('<inputs>'):
            current_section = 'inputs'
            current_inputs = config['chart']['expert']['inputs']
        elif line.startswith('<window>'):
            current_section = 'window'
        elif line.startswith('<indicator>'):
            current_section = 'indicator'
        elif line.startswith('<object>'):
            current_section = 'object'
        elif line.startswith('</'):
            current_section = None
        elif '=' in line and current_section:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if current_section == 'chart':
                if key == 'id':
                    config['chart']['id'] = int(value)
                elif key == 'symbol':
                    config['chart']['symbol'] = value
                elif key == 'description':
                    config['chart']['description'] = value
                elif key == 'period_type':
                    config['chart']['period_type'] = int(value)
                elif key == 'period_size':
                    config['chart']['period_size'] = int(value)
                elif key == 'digits':
                    config['chart']['digits'] = int(value)
                elif key == 'tick_size':
                    config['chart']['tick_size'] = float(value)
                elif key == 'position_time':
                    config['chart']['position_time'] = int(value)
                elif key == 'scale_fix':
                    config['chart']['scale_fix'] = int(value)
            elif current_section == 'expert':
                if key == 'name':
                    config['chart']['expert']['name'] = value
                elif key == 'path':
                    config['chart']['expert']['path'] = value
                elif key == 'expertmode':
                    config['chart']['expert']['expertmode'] = int(value)
            elif current_section == 'indicator':
                config['chart']['window']['indicator'][key] = value
            elif current_section == 'object':
                config['chart']['window']['object'][key] = value
            elif current_section == 'inputs' and current_inputs is not None:
                current_inputs[key] = value

    return config