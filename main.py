import os
import subprocess
from datetime import datetime
import importlib

def check_and_install_dependencies():
    """Check and install necessary dependencies if not available."""
    required_packages = ["colorama", "tkinter", "tqdm", "sd_prompt_reader"]
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call(["pip", "install", package])

check_and_install_dependencies()

from colorama import Fore, Style
from sd_prompt_reader.image_data_reader import ImageDataReader
from tkinter import filedialog
from tkinter import Tk
from tqdm import tqdm

def extract_prompts_from_folder():
    """Extract prompts from images in the specified folder and save to an output file."""
    root = Tk()
    root.withdraw()  # Hide the main window.
    folder_path = filedialog.askdirectory()  # Open the file explorer and get the selected directory path.
    if not folder_path:
        print("No folder selected. Exiting...")
        return
    output_file = "prompts_" + datetime.now().strftime("%Y%m%d") + ".txt"
    with open(output_file, 'w') as f:
        # Get the list of files
        files = os.listdir(folder_path)
        # Initialize the progress bar
        pbar = tqdm(total=len(files))
        for filename in files:
            if filename.endswith(".jpg"):
                file_path = os.path.join(folder_path, filename)
                
                reader = ImageDataReader(file_path)
                prompt = reader.positive
                
                # Error handling for empty jpeg
                if not prompt:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(Fore.RED + f"{filename} is a no parameters " + Fore.LIGHTGREEN_EX + "(skipped)" + Style.RESET_ALL)
                else:
                    f.write(prompt + ' ##' + '\n')  # Added ' ##' to the prompt and an extra '\n' to insert a line between prompts
            # Update the progress bar
            pbar.update(1)
        # Close the progress bar
        pbar.close()


if __name__ == "__main__":
    print(Fore.YELLOW + "Welcome to the PNG Ripper. Please select a folder to extract prompts from." + Style.RESET_ALL)
    extract_prompts_from_folder()
