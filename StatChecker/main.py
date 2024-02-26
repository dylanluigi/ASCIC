import os
from cpu.cpu import txt_to_csv as cpu_txt_to_csv, extract_info as extract_info_cpu
from mem.mem import mem_txt_to_csv, extract_info as extract_info_mem

def run_cpu_script(delay, amount):
    input_file_cpu = 'cpu.txt'
    output_file_cpu = 'cpu.csv'
    cpu_txt_to_csv(input_file_cpu, output_file_cpu, delay, amount)

def run_mem_script(delay, amount):
    input_file_mem = 'mem.txt'
    output_file_mem = 'mem.csv'
    mem_txt_to_csv(input_file_mem, output_file_mem, delay, amount)

def main():
    print("Select the script to run:")
    print("1. CPU Script")
    print("2. Memory Script")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        delay_cpu = int(input("Enter delay for CPU script: "))
        amount_cpu = int(input("Enter amount for CPU script: "))
        run_cpu_script(delay_cpu, amount_cpu)
    elif choice == '2':
        delay_mem = int(input("Enter delay for Memory script: "))
        amount_mem = int(input("Enter amount for Memory script: "))
        run_mem_script(delay_mem, amount_mem)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
