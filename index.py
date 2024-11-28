import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import ctypes
import sys
import threading
import time

class SoftwareInstaller:
    def __init__(self, root, software_folder):
        self.root = root
        self.root.title("Software Installer")
        self.software_folder = software_folder  # Path to the folder with installers
        self.installer_files = []  # List to store file paths of installers
        
        # Load all installer files in the folder
        self.load_software_files()

        # GUI elements
        self.software_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10)
        self.software_listbox.pack(pady=10)

        self.select_button = tk.Button(root, text="Install Selected Software", command=self.install_software, state=tk.DISABLED)
        self.select_button.pack(pady=10)

        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.update_listbox()  # Update the listbox with software files

    def load_software_files(self):
        """Load all .exe or .msi files from the specified software folder."""
        if os.path.exists(self.software_folder):
            for filename in os.listdir(self.software_folder):
                file_path = os.path.join(self.software_folder, filename)
                if os.path.isfile(file_path) and (filename.endswith('.exe') or filename.endswith('.msi')):
                    self.installer_files.append(file_path)
            print(f"Loaded installers: {self.installer_files}")  # Debug
        else:
            messagebox.showerror("Error", f"The folder {self.software_folder} does not exist.")

    def update_listbox(self):
        """Update the listbox with filenames from the software folder."""
        self.software_listbox.delete(0, tk.END)  # Clear existing listbox items
        for installer in self.installer_files:
            self.software_listbox.insert(tk.END, os.path.basename(installer))  # Insert file names
        
        # Enable the install button if there are files to select
        self.select_button.config(state=tk.NORMAL if self.software_listbox.size() > 0 else tk.DISABLED)

    def install_software(self):
        """Install the selected software in a separate thread."""
        selected_indices = self.software_listbox.curselection()  # Get selected indices
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one software to install.")
            return
        
        selected_installers = [self.installer_files[i] for i in selected_indices]  # Get file paths of selected installers
        
        # Check for administrator privileges
        if not self.is_admin():
            self.run_as_admin()
            return
        
        # Start installation in a separate thread
        install_thread = threading.Thread(target=self.run_installations, args=(selected_installers,))
        install_thread.start()

    def run_installations(self, selected_installers):
        """Run the installations in sequence."""
        total_files = len(selected_installers)
        for idx, installer in enumerate(selected_installers):
            self.progress_label.config(text=f"Installing {os.path.basename(installer)}... ({idx + 1}/{total_files})")
            self.progress_bar["value"] = (idx / total_files) * 100  # Update progress
            self.root.update_idletasks()

            self.run_installer(installer)  # Run each selected installer

        self.progress_bar["value"] = 100  # Set progress bar to 100%
        self.progress_label.config(text="All installations completed!")
        messagebox.showinfo("Installation Complete", "All selected software has been installed.")

    def run_installer(self, installer_path):
        """Run the installer and update progress."""
        try:
            print(f"Starting installation: {installer_path}")  # Debug
            if installer_path.endswith('.exe'):
                command = [installer_path, '/S']
            elif installer_path.endswith('.msi'):
                command = ['msiexec', '/i', installer_path, '/quiet', '/norestart']

            print(f"Executing command: {command}")  # Debug
            process = subprocess.run(command, check=True)
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

            # Simulate progress during installation
            for i in range(1, 101):
                time.sleep(0.05)  # Simulating installation time
                self.progress_bar["value"] += 1
                self.root.update_idletasks()

        except subprocess.CalledProcessError as e:
            print(f"Error during installation: {e}")  # Debug
            messagebox.showerror("Installation Failed", f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")  # Debug
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def is_admin(self):
        """Check if the script is running with administrator privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except AttributeError:
            return False

    def run_as_admin(self):
        """Request admin privileges and restart the script."""
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f"\"{sys.argv[0]}\"", None, 1
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to relaunch with administrator rights: {e}")
            sys.exit(1)

if __name__ == "__main__":
    software_folder = r"D:\Softwares"  # Change this to your folder path
    root = tk.Tk()
    app = SoftwareInstaller(root, software_folder)
    root.mainloop()
