import pandas as pd
import numpy as np

def merge_and_compare_files(file1_path, file2_path, output_file_path):
    # Read data from Excel into DataFrames
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    # Merge DataFrames on common columns (assuming 'Domain Interaction', 'Acceptor', 'Donor' are common)
    merged_df = pd.merge(df1, df2, on=['Domain Interaction', 'Acceptor', 'Donor'], how='outer', suffixes=('_with_zinc', '_wildtype'))

    # Create a new column 'Comparison' with the greater of the two 'Frac' values
    merged_df['Comparison'] = merged_df[['Frac_with_zinc', 'Frac_wildtype']].max(axis=1)

    # Fill NaN values in 'Frac' columns with 0
    merged_df[['Frac_with_zinc', 'Frac_wildtype']] = merged_df[['Frac_with_zinc', 'Frac_wildtype']].fillna(0)

    # Replace NaN values in 'Comparison' column with 0 if either 'Frac' value is 0
    #merged_df['Comparison'].loc[(merged_df['Frac_with_zinc'] == 0) | (merged_df['Frac_wildtype'] == 0)] = 0

    # Select the relevant columns for the output
    output_df = merged_df[['Domain Interaction', 'Acceptor', 'Donor', 'Frac_with_zinc', 'Frac_wildtype', 'Comparison']]

    # Replace NaN values in non-'Domain Interaction' columns with 0
    output_df.loc[output_df['Domain Interaction'].notna(), ['Acceptor', 'Donor', 'Frac_with_zinc', 'Frac_wildtype', 'Comparison']] = np.nan

    # Save the output to a new Excel file
    output_df.to_excel(output_file_path, index=False)

# Example usage
file1_path = 'parp-dna-zn-nad_All_filtered_0.2_pairwise.xlsx'
file2_path = 'PARP-DNA_All_filtered_0.2_pairwise.xlsx'
output_file = "pairwise_comparison1.xlsx"

merge_and_compare_files(file1_path, file2_path, output_file)
