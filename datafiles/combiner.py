import os
import pandas as pd
import glob

# Root directory
root_dir = "/root/old/ns-3-mmwave-oran/datafiles"
output_dir = os.path.join(root_dir, "concatenated")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Files to process
file_patterns = ["cu-up-cell-*.txt", "cu-cp-cell-*.txt", "du-cell-*.txt"]

# Get all files matching patterns in each run directory
runs = ["run_1", "run_2", "run_3"]
all_files = {}

for pattern in file_patterns:
    for run in runs:
        file_list = glob.glob(os.path.join(root_dir, run, pattern))
        for file_path in file_list:
            file_name = os.path.basename(file_path)  # Extract filename
            if file_name not in all_files:
                all_files[file_name] = []
            all_files[file_name].append(file_path)

# Process each file type
for file_name, file_paths in all_files.items():
    dfs = []

    for i, file_path in enumerate(file_paths):
        df = pd.read_csv(file_path)

        if df.empty:
            print(f"Warning: {file_path} is empty. Skipping.")
            continue

        print(f"Processing {file_path}, Shape: {df.shape}")

        # Adjust timestamps for continuity
        if i > 0:
            last_timestamp = dfs[-1]["timestamp"].iloc[-1]
            first_timestamp = df["timestamp"].iloc[0]
            offset = last_timestamp - first_timestamp + 10  # Ensure continuity
            df["timestamp"] += offset

        dfs.append(df)

    # Concatenate and save the file
    if dfs:
        final_df = pd.concat(dfs, ignore_index=True)
        output_file = os.path.join(output_dir, file_name)
        final_df.to_csv(output_file, index=False)
        print(f"Saved concatenated file: {output_file}")

print("All files processed successfully!")

