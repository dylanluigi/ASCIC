import re
import csv
import os
import subprocess

# Linux command to get format:
# top -b -d 2 -n 4 | grep -E 'top -|MiB Mem' | awk '/top -/ { time=$0 } /MiB Mem/ { print time, $0 }'  > Desktop/mem.txt  


def extract_info(line):
    regex = re.compile(r"top - (\d+:\d+:\d+) .*?MiB\sMem\s:\s+(\d+\.\d+)\stotal,\s+(\d+\.\d+) free,\s+(\d+\.\d+) used,\s+(\d+\.\d+) buff/cache")
    match = re.search(regex, line)
    if match:
        timestamp, total, free, used, buff_cache = match.groups()
        return timestamp, total, free, used, buff_cache
    else:
        return None

def mem_txt_to_csv(input_file, output_file, delay, amount):

    current_directory = os.getcwd()
    subdirectory = "StatChecker/mem/"
    output_file_path = os.path.join(current_directory, subdirectory, output_file)
    input_file_path = os.path.join(current_directory, subdirectory, input_file)

    # Create the subdirectory if it doesn't exist
    os.makedirs(os.path.join(current_directory, subdirectory), exist_ok=True)


    bash_command_string = "top -b -d "+str(delay)+" -n "+str(amount)+" | grep -E 'top -|MiB Mem' | awk '/top -/ { time=$0 } /MiB Mem/ { print time, $0 }' > StatChecker/mem/mem.txt"
    subprocess.run(bash_command_string, shell=True)

    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['TIME', 'TOTAL', 'FREE', 'USED', 'BUFF_CACHE'])

        for line in infile:
            info = extract_info(line)
            if info:
                csv_writer.writerow(info)
            else:
                print(f"Skipping line: {line.strip()}")

mem_txt_to_csv('mem.txt', 'mem.csv', 1, 2)