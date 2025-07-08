import pandas as pd
import re
import os 


def filter_significant_interactions(input_file_path, threshold):
    """
    Filter data based on the condition (Frac column >= threshold)
    and save the filtered data to a new Excel file.

    Parameters:
    - input_file_path (str): Path to the input Excel file.
    - threshold (float): threshold used is 0.2.
    """

    # Read the filtered data from the input file
    filtered_data_all = pd.read_excel(input_file_path, index_col=0)

    # Filter rows based on the condition (Frac column >= threshold) and non-empty 'Domain Interaction'
    filtered_data_condition = filtered_data_all[
        (filtered_data_all['Frac'] >= threshold) | (filtered_data_all['Frac'].isna())
    ]

    # Create the output file path for the filtered data
    output_file_name = os.path.splitext(os.path.basename(input_file_path))[0]
    filtered_output_path = f"{output_file_name}_0.2.xlsx"

    # Save the filtered data to a new Excel file
    filtered_data_condition.to_excel(filtered_output_path, index=True)
    print(f"Filtered data with condition has been saved to {filtered_output_path}")

# Example usage:
print('\n\n\n')
input_file_path = input("Enter the path/name of the input file (.xlsx format): ")
threshold = float(input("Enter the Threshold value in the range 0 to 1: "))
filter_significant_interactions(input_file_path, threshold)

