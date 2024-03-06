import csv
import subprocess
import os
from datetime import datetime

def get_cpu_usage(delay):
    # Capture the output of mpstat
    mpstat_output = subprocess.run(f"mpstat 1 {delay}", shell=True, capture_output=True, text=True).stdout
    # Extract the CPU idle time from the last line of mpstat output
    cpu_idle_line = mpstat_output.strip().split('\n')[-1]
    cpu_idle = float(cpu_idle_line.split()[-1])
    cpu_usage = 100.0 - cpu_idle
    return cpu_usage

def get_memory_usage():
    # Capture the output of free
    free_output = subprocess.run("free -m", shell=True, capture_output=True, text=True).stdout
    # Extract the memory usage from the second line of free output
    mem_line = free_output.strip().split('\n')[1]
    mem_parts = mem_line.split()
    total_memory = float(mem_parts[1])
    used_memory = float(mem_parts[2])  # Used memory
    memory_usage_percent = (used_memory / total_memory) * 100
    return used_memory, memory_usage_percent

def write_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', '% Global CPU', 'Used Memory Capacity', '% Memory Used'])
        writer.writerows(data)

def cpu_mem_monitoring(output_file, delay, amount):
    current_directory = os.getcwd()
    subdirectory = "cpu_mem/"
    output_file_path = os.path.join(current_directory, subdirectory, output_file)

    # Create the subdirectory if it doesn't exist
    os.makedirs(os.path.join(current_directory, subdirectory), exist_ok=True)
    
    data = []
    for _ in range(amount):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu_usage = get_cpu_usage(delay)
        used_memory, memory_usage_percent = get_memory_usage()
        data.append((timestamp, cpu_usage, used_memory, memory_usage_percent))
        # Sleep for the specified delay
        subprocess.run(['sleep', str(delay)])

    write_to_csv(output_file_path, data)

# Example usage: Monitor every second for 2 seconds (for testing)
cpu_mem_monitoring('cpu_mem.csv', 1, 2)
