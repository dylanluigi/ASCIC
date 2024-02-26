import re
import csv
import subprocess
import os

delay = 0
amount = 0

# Linux command to get format:
# top -b -d 1 -n 6 | grep -E 'top -|%Cpu\(s\)|MiB Mem' | awk '/top -/ { time=$0 } /%Cpu\(s\)/ { cpu=$0 } /MiB Mem/ { print time, cpu, $0 }' > test.txt


def extract_info(line):
    regex = re.compile(r"top - (\d+:\d+:\d+) .*?%Cpu\(s\):\s+(\d+\.\d+)\s+us,\s+(\d+\.\d+)\s+sy,\s+(\d+\.\d+)\s+ni,\s+(\d+\.\d+)\s+id,\s+(\d+\.\d+)\s+wa,\s+(\d+\.\d+)\s+hi,\s+(\d+\.\d+)\s+si,\s+(\d+\.\d+)\s+st\s+MiB\sMem\s:\s+(\d+\.\d+)\stotal,\s+(\d+\.\d+) free,\s+(\d+\.\d+) used,\s+(\d+\.\d+) buff/cache")
    match = re.search(regex, line)
    if match:
        timestamp, user, system, ni, idle, wa, hi, si, st, total, free, used, buff_cache = match.groups()
        return timestamp, user, system, ni, idle, wa, hi, si, st, total, free, used, buff_cache
    else:
        return None

def cpu_mem_txt_to_csv(input_file, output_file, delay, amount):
    current_directory = os.getcwd()
    subdirectory = "cpu_mem/"
    output_file_path = os.path.join(current_directory, subdirectory, output_file)
    input_file_path = os.path.join(current_directory, subdirectory, input_file)

    # Create the subdirectory if it doesn't exist
    os.makedirs(os.path.join(current_directory, subdirectory), exist_ok=True)

    bash_command_string = "top -b -d" + str(delay) + " -n " + str(amount) + " | grep -E 'top -|%Cpu\(s\)|MiB Mem' | awk '/top -/ { time=$0 } /%Cpu\(s\)/ { cpu=$0 } /MiB Mem/ { print time, cpu, $0 }' > cpu_mem/cpu_mem.txt"
    subprocess.run(bash_command_string, shell=True)

    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['TIME', 'USER', 'SYSTEM', 'NI', 'IDLE', 'WA', 'HI', 'SI', 'ST', 'TOTAL', 'FREE', 'USED', 'BUFF_CACHE'])

        for line in infile:
            print(line)
            info = extract_info(line)
            if info:
                csv_writer.writerow(info)
                print(info)
            else:
                print(f"Skipping line: {line.strip()}")

cpu_mem_txt_to_csv('cpu_mem.txt', 'cpu_mem.csv', 1, 2)