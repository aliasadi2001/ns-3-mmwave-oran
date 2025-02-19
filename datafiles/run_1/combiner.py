import os
import pandas as pd

# File paths
folder_path = "/root/old/ns-3-mmwave-oran/datafiles"
runs = ["run_1/cu-cp-cell-3.txt", "run_2/cu-cp-cell-3.txt", "run_3/cu-cp-cell-3.txt"]

dfs = []
for run in runs:
    file_path = os.path.join(folder_path, run)
    df = pd.read_csv(file_path)

    print(f"File: {run}, Shape: {df.shape}")  # Debugging step
    
    if df.empty:
        print(f"Error: {run} is empty! Exiting.")
        exit(1)

    dfs.append(df)

# Ensure timestamps are continuous
timestamp_offset = 0
for i in range(1, len(dfs)):  # Start from second file
    last_timestamp = dfs[i - 1]["timestamp"].iloc[-1]
    first_timestamp = dfs[i]["timestamp"].iloc[0]

    offset = last_timestamp - first_timestamp + 10  # Ensure continuity
    dfs[i]["timestamp"] += offset  # Adjust timestamps

# Concatenate all data
final_df = pd.concat(dfs, ignore_index=True)

# Save to new file
output_file = "/root/old/ns-3-mmwave-oran/datafiles/concatenated/cu-cp-cell-3.txt"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
final_df.to_csv(output_file, index=False)

print("Concatenation completed successfully!")

