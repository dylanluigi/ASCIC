import re
import csv
import subprocess
import os

delay = 0
amount = 0

def extract_info(line):
    regex = re.compile(r"top - (\d+:\d+:\d+).*?%Cpu\(s\):\s+(\d+\.\d+)\s+us,\s+(\d+\.\d+)\s+sy,\s+(\d+\.\d+)\s+ni,\s+(\d+\.\d+)\s+id,\s+(\d+\.\d+)\s+wa,\s+(\d+\.\d+)\s+hi,\s+(\d+\.\d+)\s+si,\s+(\d+\.\d+)\s+st")
    match = re.search(regex, line)
    if match:
        timestamp, user, system, ni, idle, wa, hi, si, st = match.groups()
        return timestamp, user, system, ni, idle, wa, hi, si, st
    else:
        return None

def txt_to_csv(input_file, output_file, delay, amount):
    current_directory = os.getcwd()
    subdirectory = "StatChecker/cpu/"
    output_file_path = os.path.join(current_directory, subdirectory, output_file)
    input_file_path = os.path.join(current_directory, subdirectory, input_file)

    # Create the subdirectory if it doesn't exist
    os.makedirs(os.path.join(current_directory, subdirectory), exist_ok=True)


    bash_command_string = "top -b -d" + str(delay) + " -n " + str(amount) + " | grep -E 'top -|%Cpu\(s\)' | awk '/top -/ { time=$0 } /%Cpu\(s\)/ { print time, $0 }' > StatChecker/cpu/cpu.txt"
    subprocess.run(bash_command_string, shell=True)

    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['TIME', 'USER', 'SYSTEM', 'NI', 'IDLE', 'WA', 'HI', 'SI', 'ST'])

        for line in infile:
            info = extract_info(line)
            if info:
                csv_writer.writerow(info)
                print(info)
            else:
                print(f"Skipping line: {line.strip()}")

txt_to_csv('cpu.txt', 'cpu.csv', 1, 2)