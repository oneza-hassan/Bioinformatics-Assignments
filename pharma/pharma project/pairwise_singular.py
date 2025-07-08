import pandas as pd
import numpy as np
import os


#define the function to Process a specific domain interaction within the DataFrame


#PAIRWISE FILTERATION 

def process_pairwise_domain_interaction(df, domain_interaction):
    # Drop unnecessary columns
    df = df.drop(['DonorH', 'AvgDist', 'AvgAng'], axis=1)

    # Modify residue names, handling NaN values
    df['Acceptor'] = df['Acceptor'].apply(lambda x: x.split('@')[0] if isinstance(x, str) else np.nan)
    df['Donor'] = df['Donor'].apply(lambda x: x.split('@')[0] if isinstance(x, str) else np.nan)

    # Group by acceptor and donor residues, update Frames, and calculate Frac
    grouped = df.groupby(['Acceptor', 'Donor'])
    result = pd.DataFrame(columns=df.columns)

    for _, group in grouped:
        frames_sum = group['Frames'].sum()
        frac = frames_sum / (5000 * len(group))
        group.iloc[0, df.columns.get_loc('Frames')] = frames_sum
        group.iloc[0, df.columns.get_loc('Frac')] = frac
        result = pd.concat([result, group.iloc[[0]]], ignore_index=True)

    # Add a row for the domain interaction
    domain_row = pd.DataFrame([[domain_interaction, np.nan, np.nan, np.nan, np.nan]], columns=df.columns)
    result = pd.concat([domain_row, result], ignore_index=True)

    return result

#define that function to Process the entire input file, handling multiple domain interactions.
def process_file_pairwise(file_path, output_path):
    # Read the input file
    df = pd.read_excel(file_path)

    # Initialize variables for domain interaction boundaries
    start_index = None
    result_dfs = []

    # Process each row in the DataFrame
    for index, row in df.iterrows():
        if pd.notna(row['Domain Interaction']):
            if start_index is not None:
                # Process the previous domain interaction
                result_df = process_pairwise_domain_interaction(df.iloc[start_index:index, :], domain_interaction=df.at[start_index, 'Domain Interaction'])
                result_dfs.append(result_df)

            # Set the start index for the next domain interaction
            start_index = index

    # Process the last domain interaction in the file
    result_df = process_pairwise_domain_interaction(df.iloc[start_index:, :], domain_interaction=df.at[start_index, 'Domain Interaction'])
    result_dfs.append(result_df)

    # Concatenate all result dataframes
    final_result = pd.concat(result_dfs, ignore_index=True)

    # Write the result to an output file
    final_result.to_excel(output_path, index=False)

# call the function for the pairwaise filtration
'''
input_file = input("Enter the path/name of the filtered MD simulation file (.xlsx format): ")
output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}_pairwise.xlsx"

process_file_pairwise(input_file, output_file)

'''


#SINGULAR FILTERATION 

def process_singular_domain_interaction(df, domain_interaction):
    # Drop unnecessary columns
    df = df.drop(['DonorH', 'AvgDist', 'AvgAng'], axis=1)

    # Modify residue names, handling NaN values
    df['Acceptor'] = df['Acceptor'].apply(lambda x: x.split('@')[0] if isinstance(x, str) else np.nan)
    df['Donor'] = df['Donor'].apply(lambda x: x.split('@')[0] if isinstance(x, str) else np.nan)

    # Extract unique residues from both Acceptor and Donor columns
    unique_residues = pd.unique(pd.concat([df['Acceptor'], df['Donor']], ignore_index=True).dropna())

    # Initialize a DataFrame to store the results
    result = pd.DataFrame(columns=['Domain Interaction', 'Residue', 'Frames', 'Frac'])

   # Initialize a variable to track whether 'Domain Interaction' has been written
    domain_interaction_written = False

    # Process each unique residue
    for residue in unique_residues:
        residue_rows = df[(df['Acceptor'] == residue) | (df['Donor'] == residue)]
        if not residue_rows.empty:
            frames_sum = residue_rows['Frames'].sum()
            frac = frames_sum / (5000 * len(residue_rows))
            
            # Check if 'Domain Interaction' has already been written
            if not domain_interaction_written:
                result = pd.concat([result, pd.DataFrame([['', residue, frames_sum, frac]], columns=result.columns)], ignore_index=True)
                domain_interaction_written = True
            else:
                result = pd.concat([result, pd.DataFrame([['', residue, frames_sum, frac]], columns=result.columns)], ignore_index=True)

    # Add a row for the domain interaction
    domain_row = pd.DataFrame([[domain_interaction, np.nan, np.nan, np.nan]], columns=result.columns)
    result = pd.concat([domain_row, result], ignore_index=True)

    return result


def process_file_singular(file_path, output_path):
    # Read the input file
    df = pd.read_excel(file_path)

    # Initialize variables for domain interaction boundaries
    start_index = None
    result_dfs = []

    # Process each row in the DataFrame
    for index, row in df.iterrows():
        if pd.notna(row['Domain Interaction']):
            if start_index is not None:
                # Process the previous domain interaction
                result_df = process_singular_domain_interaction(df.iloc[start_index:index, :], domain_interaction=df.at[start_index, 'Domain Interaction'])
                result_dfs.append(result_df)

            # Set the start index for the next domain interaction
            start_index = index

    # Process the last domain interaction in the file
    if start_index is not None:
        result_df = process_singular_domain_interaction(df.iloc[start_index:, :], domain_interaction=df.at[start_index, 'Domain Interaction'])
        result_dfs.append(result_df)

    # Concatenate all result dataframes
    final_result = pd.concat(result_dfs, ignore_index=True)

    # Write the result to an output file
    final_result.to_excel(output_path, index=False)

# Call the function for the pairwise filtration
'''
input_file = input("Enter the path/name of the filtered MD simulation file (.xlsx format): ")
output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}_singular.xlsx"

process_file_singular(input_file, output_file)
'''