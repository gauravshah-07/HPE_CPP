import os
import argparse
import subprocess

# List of producer script filenames
producer_files = [
    "Producer_Rotational.py",
    "Producer_Current.py",
    "Producer_Voltage.py",
    "Producer_Temperature.py",
    "Producer_Power.py"
]

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Kafka Producer Script Menu')
parser.add_argument('--bootstrap-server', default='admin:9092', help='Kafka bootstrap server address (default: admin:9092)')
args = parser.parse_args()

# Store running processes
processes = {}

def run_producer(index):
    """Run a specific producer script in the background."""
    file = producer_files[index]
    if file in processes:
        print(f"{file} is already running.")
    else:
        process = subprocess.Popen(["python", file, "--bootstrap-server", args.bootstrap_server], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes[file] = process
        print(f"Started {file} (PID: {process.pid})")

def stop_producer(index):
    """Stop a specific producer script."""
    file = producer_files[index]
    if file in processes:
        processes[file].terminate()
        print(f"Stopped {file}")
        del processes[file]
    else:
        print(f"{file} is not running.")

def stop_all_producers():
    """Stop all running producer scripts."""
    for file, process in processes.items():
        process.terminate()
        print(f"Stopped {file}")
    processes.clear()

def menu():
    while True:
        print("\n===== Producer Script Menu =====")
        for i, file in enumerate(producer_files):
            print(f"{i+1}. Run {file}")
        print(f"{len(producer_files)+1}. Run All Producers")
        print(f"{len(producer_files)+2}. Stop All Producers")
        print(f"{len(producer_files)+3}. Show Running Producers")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(producer_files):
                run_producer(choice - 1)
            elif choice == len(producer_files) + 1:
                for i in range(len(producer_files)):
                    run_producer(i)
            elif choice == len(producer_files) + 2:
                stop_all_producers()
            elif choice == len(producer_files) + 3:
                if processes:
                    print("\nRunning Producers:")
                    for file, process in processes.items():
                        print(f"- {file} (PID: {process.pid})")
                else:
                    print("No producers are running.")
            elif choice == 0:
                print("Exiting...")
                stop_all_producers()
                break
            else:
                print("Invalid choice, please try again.")
        else:
            print("Invalid input, please enter a number.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nStopping all producers...")
        stop_all_producers()
