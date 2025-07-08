import pandas as pd

def compare_and_save(input_file1, input_file2, output_file):
    # Read input files
    df1 = pd.read_excel(input_file1)
    df2 = pd.read_excel(input_file2)

    # Merge dataframes on 'Domain Interaction' and 'Residue'
    merged_df = pd.merge(df1, df2, on=['Domain Interaction', 'Residue'], how='outer', suffixes=('_wildtype', '_withZinc'))

    # Fill NaN values with 0
    merged_df = merged_df.fillna(0)

    # Add a new column for the comparison
    merged_df['comparison'] = merged_df.apply(lambda row: row['Frac_wildtype'] if row['Frac_wildtype'] > row['Frac_withZinc'] else row['Frac_withZinc'], axis=1)

    # Set 0s in the 'Frac_wildtype', 'Frac_withZinc', 'Residue', and 'comparison' columns to NaN for rows where the 'Domain Interaction' column is filled
    mask = merged_df['Domain Interaction'] != 0
    merged_df.loc[mask, ['Residue','Frac_wildtype', 'Frac_withZinc', 'comparison']] = None

    # Set 0s in the 'Domain Interaction' row and column to NaN
    mask = (merged_df['Domain Interaction'] == 0) & (merged_df['Residue'] != 0)
    merged_df.loc[mask, 'Domain Interaction'] = None
    merged_df.loc[:, 'Domain Interaction'] = merged_df['Domain Interaction'].replace(0, None)

    # Drop duplicates based on 'Domain Interaction' and 'Residue'
    merged_df = merged_df.drop_duplicates(subset=['Domain Interaction', 'Residue'], keep='first')

    # Select relevant columns for the output
    output_df = merged_df[['Domain Interaction', 'Residue', 'Frac_wildtype', 'Frac_withZinc', 'comparison']]

    # Save the result to a new Excel file
    output_df.to_excel(output_file, index=False)

# Example usage
compare_and_save('PARP-DNA_All_filtered_0.2_singular.xlsx', 'parp-dna-zn-nad_All_filtered_0.2_singular.xlsx', 'singular_comparison.xlsx')

