import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the other folder
module_path = os.path.join(current_dir, '..', 'simulator')

# Add the module path to sys.path
sys.path.append(module_path)

# Now you can import the module
import simulator