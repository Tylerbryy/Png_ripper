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

def consolidate_prompts(raw_text):
    prompts = []
    current_prompt = []
    
    for line in raw_text.split('\n'):
        stripped_line = line.strip()
        
        # Check for the '##' delimiter to identify the end of a prompt.
        if stripped_line.endswith('##'):
            current_prompt.append(stripped_line)
            prompts.append(' '.join(current_prompt))
            current_prompt = []
        else:
            current_prompt.append(stripped_line)

    # For cases where there's no '##' at the end
    if current_prompt:
        prompts.append(' '.join(current_prompt))
    
    return '\n'.join(prompts)


import json

def extract_prompts_from_folder(output_format='txt'):
    """Extract prompts from images in the specified folder and save to an output file."""
    root = Tk()
    root.withdraw()  # Hide the main window.
    folder_path = filedialog.askdirectory()  # Open the file explorer and get the selected directory path.
    if not folder_path:
        print("No folder selected. Exiting...")
        return
    
    # Adjust the output filename based on the chosen format
    output_file = "prompts_" + datetime.now().strftime("%Y%m%d") + "." + output_format
    
    extracted_prompts = []
    
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
                extracted_prompts.append(prompt)
        # Update the progress bar
        pbar.update(1)
    # Close the progress bar
    pbar.close()
    
    # Save the extracted prompts based on the chosen format
    if output_format == 'txt':
        with open(output_file, 'w') as f:
            f.write(consolidate_prompts('\n'.join([prompt + ' ##' for prompt in extracted_prompts])))
    elif output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(extracted_prompts, f, indent=4)

if __name__ == "__main__":
    print(Fore.YELLOW + "Welcome to the PNG Ripper. Please select a folder to extract prompts from." + Style.RESET_ALL)
    format_choice = input("Choose an output format (txt/json) [default: txt]: ").strip().lower() or 'txt'
    extract_prompts_from_folder(format_choice)
