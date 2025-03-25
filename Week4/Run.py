import os
import argparse

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

def run_producer(index):
    """Run a specific producer script based on index."""
    os.system(f"python {producer_files[index]} --bootstrap-server {args.bootstrap_server}")

def menu():
    while True:
        print("\n===== Producer Script Menu =====")
        for i, file in enumerate(producer_files):
            print(f"{i+1}. Run {file}")
        print(f"{len(producer_files)+1}. Run All Producers")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(producer_files):
                run_producer(choice - 1)
            elif choice == len(producer_files) + 1:
                for i in range(len(producer_files)):
                    os.system(f"python {producer_files[i]} --bootstrap-server {args.bootstrap_server} &")  # Run all in parallel
            elif choice == 0:
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")
        else:
            print("Invalid input, please enter a number.")

if __name__ == "__main__":
    menu()
