import argparse
import pandas as pd

def input_parse():
    # Define argparse to get input, output paths
    parser = argparse.ArgumentParser(description="Process data and calculate percentages.")
    parser.add_argument("-i", 
                        "--input_file", 
                        required=True, 
                        help="Path to the input Excel file")
    parser.add_argument("-o", 
                        "--output_file", 
                        required=True, 
                        help="Path to save the output Excel file")
    args = parser.parse_args()
    
    return args

def read_data(file_path):
    # Read data from Excel file
    df = pd.read_excel(file_path)
    
    return df

def transform_data(df, frequency_columns):
    # Convert empty cells to zeros
    df = df.apply(lambda x: x.apply(lambda y: 0 if pd.isna(y) else y))

    # Convert frequency columns to numeric
    for column in frequency_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').astype(float)

    # Iterate over rows and update cells with percentages
    for index, row in df.iterrows():
        values = [row[column] for column in frequency_columns]
        total_sum = sum(filter(pd.notna, values)) or 1

        for column, value in zip(frequency_columns, values):
            df.at[index, column] = value / total_sum

    return df

def calculate_percentage(df, frequency_columns):
    # Sum the frequencies in each column
    column_sums = {column: df[column].sum() for column in frequency_columns}

    # Calculate percentages
    df.loc['Total'] = pd.Series(column_sums)
    total_sum = sum(column_sums.values())
    
    for column in frequency_columns:
        df.loc['Percentage', column] = (column_sums[column] / total_sum) * 100

    return df

def save_data(df, out_path):
    # Save the DataFrame to Excel file
    df.to_excel(out_path, index=False)

if __name__ == "__main__":
    args = input_parse()
    # Read data
    inpath = os.path.join("data", "5_boxes_raw", args.input_file)
    data_frame = read_data(inpath)

    # Identify frequency columns dynamically
    frequency_columns = [column for column in data_frame.columns if "frequency" in column]

    # Transform data
    transformed_data = transform_data(data_frame, frequency_columns)

    # Calculate percentages
    data_with_percentages = calculate_percentage(transformed_data, frequency_columns)

    # Save data
    outpath = os.path.join("data", "6_boxes", args.output_file)
    save_data(data_with_percentages, outpath)
