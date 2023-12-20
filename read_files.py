import os 

# initializing a dictionary.
data = {}

# Reading txt files from folder(txt_files).
folder_path = './txt_files'
file_names = os.listdir(folder_path)

# Check if path exists.
if os.path.exists(folder_path):
    print(f"Folder exists {folder_path}")
else:
    print(f"Folder {folder_path} does not exist.")


# reading each file and storing the names and their content.
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
        data[file_name] = content

        file.close() # closing the file.

# Printing the file_name and content of each text file.
for file_name, content in data.items():
    print(f"Content of file {file_name}:\n{content}\n")

# Reading the first 3 lines that print the number of (jobs, machines and makespan).
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        num_jobs = int(file.readline().strip())
        num_machines = int(file.readline().strip())
        try: # check if there is a makespan.
            makespan = int(file.readline().strip())
        except ValueError:
            makespan = None # if not, None is assigned to it.

        # printing each value. 
        print("\n")
        print(f"File {file_name}")
        print(f"Number of jobs: {num_jobs}")
        print(f"Number of machines: {num_machines}")
        print(f"Makespan: {makespan}")
    
        file.close() # closing the file.

