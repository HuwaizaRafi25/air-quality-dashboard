import os
import pandas as pd

folder_path = "data/"
output_file = "dashboard/main_data.csv"

csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

df_list = []
for file in csv_files:
    df = pd.read_csv(os.path.join(folder_path, file))
    df["station"] = file.replace(".csv", "")
    df_list.append(df)

df_final = pd.concat(df_list, ignore_index=True)

df_final.to_csv(output_file, index=False)
print(f"Data gabungan disimpan di {output_file}")
