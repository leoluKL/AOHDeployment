import os
import re

def number_headings(md_content):
    header_counter = [0] * 6  # Supports up to 6 levels of headers
    lines = md_content.split('\n')
    new_lines = []
    
    for line in lines:
        # Match headings and ignore existing numbers
        match = re.match(r'^(#+)\s*(\d+(\.\d+)*)*\s*(.*)$', line)
        if match:
            level = len(match.group(1)) - 1  # Calculate the depth level of the heading
            header_counter[level] += 1
            # Reset all lower level counters to zero
            for i in range(level + 1, 6):
                header_counter[i] = 0
            
            # Create the numbered header prefix, ensuring only one period follows the last number
            header_number = '.'.join(str(header_counter[i]) for i in range(level + 1) if header_counter[i] > 0)
            new_line = f'{match.group(1)} {header_number} {match.group(4)}'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    return '\n'.join(new_lines)

def process_directory(directory):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                numbered_content = number_headings(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(numbered_content)
                print(f'Updated {file_path}')

# Get the directory where the script file is located
script_directory = os.path.dirname(os.path.realpath(__file__))

# Run the process_directory function with the script's directory
process_directory(script_directory)