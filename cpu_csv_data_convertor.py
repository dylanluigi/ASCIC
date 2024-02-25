import re
import csv

def extract_info(line):
    regex = re.compile(r"top - (\d+:\d+:\d+).*?%Cpu\(s\):\s+(\d+\.\d+)\s+us,\s+(\d+\.\d+)\s+sy,\s+(\d+\.\d+)\s+ni,\s+(\d+\.\d+)\s+id,\s+(\d+\.\d+)\s+wa,\s+(\d+\.\d+)\s+hi,\s+(\d+\.\d+)\s+si,\s+(\d+\.\d+)\s+st")
    match = re.search(regex, line)
    if match:
        timestamp, user, system, ni, idle, wa, hi, si, st = match.groups()
        return timestamp, user, system, ni, idle, wa, hi, si, st
    else:
        return None

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['TIME', 'USER', 'SYSTEM', 'NI', 'IDLE', 'WA', 'HI', 'SI', 'ST'])

        for line in infile:
            info = extract_info(line)
            if info:
                csv_writer.writerow(info)
            else:
                print(f"Skipping line: {line.strip()}")

txt_to_csv('input.txt', 'output.csv')
