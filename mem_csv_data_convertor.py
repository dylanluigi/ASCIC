import re
import csv

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

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['TIME', 'TOTAL', 'FREE', 'USED', 'BUFF_CACHE'])

        for line in infile:
            info = extract_info(line)
            if info:
                csv_writer.writerow(info)
            else:
                print(f"Skipping line: {line.strip()}")

txt_to_csv('mem.txt', 'output_mem.csv')
