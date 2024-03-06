import re
import csv
import os
import subprocess

def extract_info_vmstat(line):
    # Adjust the regex to match the new line format with the timestamp prepended
    regex = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+\d+\s+\d+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+).*")
    match = re.search(regex, line)
    if match:
        timestamp, swpd, free, buff, cache = match.groups()
        return timestamp, swpd, free, buff, cache
    else:
        return None

def vmstat_to_csv(input_file, output_file, delay, amount):

    current_directory = os.getcwd()
    subdirectory = "mem/"
    output_file_path = os.path.join(current_directory, subdirectory, output_file)
    input_file_path = os.path.join(current_directory, subdirectory, input_file)

    # Create the subdirectory if it doesn't exist
    os.makedirs(os.path.join(current_directory, subdirectory), exist_ok=True)

    # Adjusted bash command to prepend a timestamp to each vmstat output line
    # Note: This command uses date and awk to insert the current timestamp before each vmstat output line
    bash_command_string = f"bash -c 'vmstat {delay} {amount} | while read line; do echo \"$(date +\"%Y-%m-%d %H:%M:%S\") $line\"; done' > {input_file_path}"
    subprocess.run(bash_command_string, shell=True, check=True)

    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        # Update the header to include TIMESTAMP
        csv_writer.writerow(['TIMESTAMP', 'SWPD', 'FREE', 'BUFF', 'CACHE'])

        # Skip the initial lines that don't contain the vmstat data we're interested in
        for _ in range(2):  # You may need to adjust this based on your output
            next(infile)

        for line in infile:
            info = extract_info_vmstat(line)
            if info:
                csv_writer.writerow(info)
            else:
                print(f"Skipping line: {line.strip()}")

vmstat_to_csv('mem.txt', 'mem.csv', 1, 2)
