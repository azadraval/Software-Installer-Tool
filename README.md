Software Installer Tool
This Python-based Software Installer Tool simplifies the batch installation of multiple software packages (.exe and .msi) using a graphical interface built with tkinter. It includes real-time progress tracking, administrator privilege checks, and silent installation options for a seamless user experience.

Features
Batch Installations: Select and install multiple .exe or .msi files sequentially.
Graphical Interface: User-friendly GUI built with tkinter.
Admin Privilege Check: Automatically requests elevated privileges when needed.
Progress Feedback: Real-time progress bar and status updates during installations.
Silent Installations: Installs software with minimal user intervention using /S or /quiet flags.
Error Handling: Notifies users of errors during installation and provides debugging details.
How It Works
Specify Folder: Set the path to the folder containing .exe and .msi installers in the software_folder variable.
Launch the Tool: Run the script to load installer files into the application.
Select and Install: Choose software from the list and click "Install Selected Software."
Track Progress: Monitor installation progress through the progress bar and status label.
Setup Instructions
Prerequisites:
Python 3.x installed.
.exe or .msi files stored in a folder.
Run the Script:
Clone or download the repository.
Set the software_folder variable in the script.
Run the tool:
bash
Copy code
python software_installer.py
Administrator Rights:
Ensure the script runs with admin privileges for successful installations. The tool prompts for elevation if necessary.
File Structure
bash
Copy code
.
├── software_installer.py     # Main script file
└── D:\Softwares              # Folder containing .exe/.msi files (change this path in the script)
Code Highlights
Silent Installation:
python
Copy code
command = [installer_path, '/S']  # For .exe files
command = ['msiexec', '/i', installer_path, '/quiet', '/norestart']  # For .msi files
subprocess.run(command, check=True)
Admin Privilege Check:
python
Copy code
ctypes.windll.shell32.IsUserAnAdmin()
Real-Time Progress Bar:
python
Copy code
self.progress_bar["value"] = progress_percentage
self.root.update_idletasks()
Future Improvements
Add support for additional file formats and installation flags.
Implement logging to track installation events.
Enhance the interface with sorting and search features.
Contributing
Contributions are welcome! Fork the repository, make changes, and submit a pull request. Feedback and suggestions are greatly appreciated.

License
This project is open-source under the MIT License.
