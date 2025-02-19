import os
import pandas as pd
import shutil

# Define paths
datafiles_dir = "/root/old/ns-3-mmwave-oran/datafiles"
concatenated_dir = os.path.join(datafiles_dir, "concatenated")
destination_dir = "/root/old/ns-3-mmwave-oran/ns-3-mmwave-oran"

# Ensure concatenated directory exists
os.makedirs(concatenated_dir, exist_ok=True)

# Define file patterns to process
file_patterns = ["cu-up-cell-", "cu-cp-cell-", "du-cell-"]

# Find and process matching files
for pattern in file_patterns:
    matching_files = [f for f in os.listdir(os.path.join(datafiles_dir, "run_1")) if f.startswith(pattern)]
    
    if not matching_files:
        print(f"Warning: No files matching {pattern} found!")
        continue

    all_data = []

    for run in ["run_1", "run_2", "run_3"]:
        run_path = os.path.join(datafiles_dir, run)
        for file_name in matching_files:
            file_path = os.path.join(run_path, file_name)
            
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                df = pd.read_csv(file_path)
                all_data.append(df)
            else:
                print(f"Warning: {file_path} is empty or missing. Skipping.")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        output_file = os.path.join(concatenated_dir, matching_files[0])
        combined_df.to_csv(output_file, index=False)
        print(f"Created: {output_file}")

# Copy concatenated files to ns-3-mmwave-oran folder
if os.path.exists(destination_dir):
    for file_name in os.listdir(concatenated_dir):
        source_file = os.path.join(concatenated_dir, file_name)
        destination_file = os.path.join(destination_dir, file_name)

        try:
            shutil.copy(source_file, destination_file)
            print(f"Copied: {source_file} -> {destination_file}")
        except Exception as e:
            print(f"ERROR: Failed to copy {file_name}: {e}")
    print("All files copied successfully!")
else:
    print(f"ERROR: Destination folder {destination_dir} does not exist!")

print("Processing complete!")

