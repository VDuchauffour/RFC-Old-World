import pandas as pd
import os
import typer

def ods_to_csv(ods_file: str, output_dir: str = '.'):
    docs = pd.read_excel(ods_file, engine="odf", header=None, sheet_name=None)
    
    for sheet_name, df in docs.items():
        csv_filename = os.path.join(output_dir, f"{sheet_name}.csv")
        df.to_csv(csv_filename, index=False, header=False)
        print(f"Saved sheet '{sheet_name}' to {csv_filename}")


if __name__ == "__main__":
    typer.run(ods_to_csv)
