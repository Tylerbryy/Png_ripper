import os
from datetime import datetime
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
                    print(Fore.RED + f"{filename} is a no parameters " + Fore.LIGHTGREEN_EX + "(skipped)" + Style.RESET_ALL)
                else:
                    f.write(prompt + '\n')
            # Update the progress bar
            pbar.update(1)
        # Close the progress bar
        pbar.close()

if __name__ == "__main__":
    extract_prompts_from_folder()
