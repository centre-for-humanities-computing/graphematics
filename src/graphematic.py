import pandas as pd
import os
import argparse

def process_files(file_paths, out_path):
    dfs = []
    file_names = []

    # Load dataframes from Excel files
    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_names.append(file_name)
        dfs.append(pd.read_excel(file_path))

    # Extract frequency column headers
    freq_columns = [list(df.columns[df.columns.str.startswith('frequency')]) for df in dfs]

    # Create a new dataframe with unique graphemes from all files
    graphemes = list(set(sum(freq_columns, [])))
    result_df = pd.DataFrame({'graphemes': graphemes})

    # Extract frequencies for soundposition columns from the last row for each file
    for i, df in enumerate(dfs):
        result_df[file_names[i]] = result_df['graphemes'].map(lambda x: df[x].iloc[-1] if x in df.columns else 0)

    # Add the "distance" column
    result_df['distance'] = result_df.iloc[:, 1:].diff(axis=1).abs().sum(axis=1)

    # Add two summary rows to the "distance" column
    result_df.loc['Total', 'distance'] = result_df['distance'].sum()
    result_df.loc['Average', 'distance'] = result_df.loc['Total', 'distance'] / len(file_paths)

    # Save to Excel
    result_df.to_excel(out_path, index=False)

    # Display the resulting dataframe
    print(result_df)

def main():
    parser = argparse.ArgumentParser(description='Process Excel files and calculate distance.')
    parser.add_argument('files', nargs='+', help='Input Excel files')
    parser.add_argument('--outpath', help='Output Excel file path', default='output/distance/distance_result.xlsx')

    args = parser.parse_args()
    process_files(args.files, args.outpath)

if __name__ == "__main__":
    main()
