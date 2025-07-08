#PHARMACOINFORMATICS: PROTEIN DOMAIN INTERACTIONS 
#AND COMPARISON BETWEEN WILD TYPE AND ZINC ASSOCIATED ONE
'''
Group members: Oneza, Zainab, Arooba, Fatima
BS Bioinformatics 7th semester
NCB QAU 
'''

'''
    pip install pandas
    pip install openpyxl
    pip list to check the package and version 
    Package            Version
    ------------------ ---------
    Python             3.10.1
    pandas             2.0.2
    openpyxl           3.1.2
    re                 2.2.1
    numpy              1.24.3

'''

import pandas as pd
import numpy as np
import re
import os 


#STEP 0: FILE PREPRATION

# Define a function to convert .avg files to xlsx files
def avg_to_xlsx(avg_file, xlsx_file):
    # Read the .avg file as a dataframe
    df = pd.read_csv(avg_file, sep="\s+", header=0)

    # Remove the # from the header
    df.columns = df.columns.str.replace("#", "")

    # Write the dataframe to an xlsx file
    df.to_excel(xlsx_file, index=False)


#call the function to convert the files

'''
avg_to_xlsx("parp-dna-zn-nad_All.UU.avg.dat", "parp-dna-zn-nad_All.xlsx")
avg_to_xlsx("PARP-DNA_All.UU.avg.dat", "PARP-DNA_All.xlsx")
'''

#define the function to remove the trailing white spaces from excel and add an underscore between the residue and its position
def remove_spaces_add_underscore(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file, header=None)

    # Iterate over columns and rows to remove spaces
    for col in df.columns:
        for i in range(len(df[col])):
            if isinstance(df.at[i, col], str):
                df.at[i, col] = ' '.join(part.strip() if part.isnumeric() else part for part in df.at[i, col].split())
    # Extract the header from the first row
    header = df.iloc[0]

    # Modify the DataFrame by replacing the space with an underscore in the entries from the second row onwards
    for index, row in df.iterrows():
        if index != 0:  # Skip the header row
            df.iloc[index] = [f"{residue.replace(' ', '_')}" if pd.notna(residue) else pd.NaT for residue in row]

    # Save the modified DataFrame back to the Excel file
    df.to_excel(output_file, header=None, index=False)


#call the function to remove the spaces and add underscore
'''
remove_spaces_add_underscore('RESIDUES FILE 1.xlsx', 'RESIDUES FILE.xlsx')
'''

#STEP 1: FILTRATION BASED ON THE DOMAIN RANGES AND INTERCAAT RESIDUES

# File paths for the provided Excel files
residues_file_path = input("Enter the path/ name of the Residue File (.xlsx format): ")
domain_ranges_file_path = input("Enter the path/ name of the Domain range File (.xlsx format): ")
md_simulation_file_path = input("Enter the path/ name of the MD simulation cleaned File (.xlsx format): ")


# Read the Excel files into pandas DataFrames
residues_df = pd.read_excel(residues_file_path)
domain_ranges_df = pd.read_excel(domain_ranges_file_path)
md_simulation_df = pd.read_excel(md_simulation_file_path)

# Print some information for debugging
'''
print("Residues DataFrame:")
print(residues_df.head())
print("\nDomain Ranges DataFrame:")
print(domain_ranges_df.head())
print("\nMD Simulation DataFrame:")
print(md_simulation_df.head())
'''

# Construct the domain_ranges dictionary before calling the function
domain_ranges = {row['Domain']: (row['start pos'], row['end pos']) for _, row in domain_ranges_df.iterrows()}

'''print(domain_ranges)'''



#define the function for filteration 
def filter_md_simulation_data_corrected(residues_df, domain_ranges, md_simulation_df):
    filtered_rows_list = []

    for column in residues_df.columns:
        '''print(column)'''
        print("\n")

        # Add a header row with the domain interaction
        filtered_rows_list.append(pd.DataFrame([column], columns=['Domain Interaction']))
       
        for residue in residues_df[column].dropna():
            '''print(residue)'''   

            # Splitting residue into name and position, assuming an underscore is used
            residue_parts = residue.split('_')
            '''print(residue_parts)'''
            
            if len(residue_parts) == 2 and residue_parts[1].isdigit():
                residue_name = residue_parts[0]
                residue_pos = int(residue_parts[1])
                
                # Determine the residue's own domain based on residue position
                residue_domain = None
                for domain, (start_pos, end_pos) in domain_ranges.items():
                    if start_pos <= residue_pos <= end_pos:
                        residue_domain = domain
                        break

                # Determine the interacting domain based on column name
                interacting_domain = column.split('-')[1]  # Assuming the column name is in the format ZN1-ZN3
                interacting_domain = interacting_domain.split('_')[0]

                '''print(f"Residue: {residue_name}_{residue_pos}, Residue Domain: {residue_domain}, Interacting Domain: {interacting_domain}")'''

                if interacting_domain:

                    filtered_rows = md_simulation_df[
                        # Check if either 'Acceptor' or 'Donor' starts with the given residue name and position
                        ((md_simulation_df['Acceptor'].str.startswith(f'{residue_name}_{residue_pos}@')) |
                         (md_simulation_df['Donor'].str.startswith(f'{residue_name}_{residue_pos}@'))) &
                        # Check if the position of the residue (extracted from 'Acceptor' or 'Donor') is within the interacting domain range
                        ((md_simulation_df['Acceptor'].str.extract('(\d+)')[0].astype(int).between(*domain_ranges[interacting_domain])) |
                         (md_simulation_df['Donor'].str.extract('(\d+)')[0].astype(int).between(*domain_ranges[interacting_domain])))
                    ]
                    
                    # Print information for debugging
                    '''print(f"Residue: {residue_name}_{residue_pos}, {residue} Domain: {residue_domain}, Interacting Domain: {interacting_domain}")'''
                
                    # Append filtered rows to the list
                    filtered_rows_list.append(filtered_rows)

                    '''
                    print(filtered_rows)
                    print('\n')

                    print(type(filtered_rows_list))
                    print(type(filtered_rows))'''

            else:
                print(f"Invalid residue format: '{residue}' in column '{column}'")
        
        # Add two blank rows between domain interactions
        filtered_rows_list.extend([pd.DataFrame(), pd.DataFrame()])

    # Check if there are valid residues before concatenating
    if filtered_rows_list:

        # Concatenate filtered rows for all residues
        filtered_data_all = pd.concat(filtered_rows_list, ignore_index=True)
        '''
        print("\n")
        print(filtered_data_all)'''

        # Save the filtered data to an Excel file
        output_file_path = f"{os.path.splitext(os.path.basename(md_simulation_file_path))[0]}_filtered.xlsx"
        filtered_data_all.to_excel(output_file_path, index=False)
        print(f"Filtered data has been saved to {output_file_path}")
    else:
        print("No valid residues found for filtering.")


# Call the function to store filtered residues
'''
filter_md_simulation_data_corrected(residues_df, domain_ranges, md_simulation_df)
'''


#STEP 2: FILTRATION BASED ON A THRESHOLD CONDITION FOR SIGNIFICANT INTERACTIONS

#define the function to filter the file further for significant interactions i-e Frac>=0.2
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

# Call the function to filter based on fractions:
print('\n\n\n')
'''
input_file_path = input("Enter the path/name of the input file (.xlsx format): ")
threshold = float(input("Enter the Threshold value in the range 0 to 1: "))
filter_significant_interactions(input_file_path, threshold)
'''


#STEP 3: PAIRWISE FILTRATION

#define the function to Process a specific domain interaction within the DataFrame
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


#STEP 4: SINGULAR FILTERATION 

# Define the function to process a specific domain interaction within the DataFrame
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


#define the function to Process a specific domain interaction within the DataFrame


#STEP 5: PAIRWISE FILTERATION 

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


#STEP 6: SINGULAR FILTERATION 

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

#STEP 7: PAIRWISE COMPARISON

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

# usage
'''
file1_path = 'parp-dna-zn-nad_All_filtered_0.2_pairwise.xlsx'
file2_path = 'PARP-DNA_All_filtered_0.2_pairwise.xlsx'
output_file = "pairwise_comparison1.xlsx"

merge_and_compare_files(file1_path, file2_path, output_file)
'''


#STEP 8: SINGULAR COMPOSITION

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
'''
compare_and_save('PARP-DNA_All_filtered_0.2_singular.xlsx', 'parp-dna-zn-nad_All_filtered_0.2_singular.xlsx', 'singular_comparison.xlsx')
'''
