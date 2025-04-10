import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def input_parse():
    parser = argparse.ArgumentParser()
    #add arguments
    parser.add_argument("-f", 
                        "--filename",
                        help = "pick which dataset you want",
                        type = str)
    parser.add_argument("-o", 
                        '--output', 
                        type=str, 
                        help='Output file name for the sound position tables', 
                        default='output.xlsx')
    # save arguments to be parsed from the CLI
    args = parser.parse_args()

    return args

def main():
    # intialise arguments 
    args = input_parse()
    inpath = os.path.join("data", "4_annotated_segmented", args.filename)
    # Step 1: Read the Excel file into a DataFrame
    df = pd.read_excel(inpath)
    col_remove = ["Label", "Translation", "Notes"]
    df.drop(columns=col_remove, inplace=True)
    
    # get the sound position list
    exclude_chars = ['#', '<de>', '<en>', '[ig]', 'h', 'l', 'v','|ß|','ü']

    # Create an empty dictionary to store the results
    word_dict = {}

    # Iterate through every two rows in the dataframe
    for i in range(0, len(df), 2):
        # Extract the word and frequency from the first row
        word = ''.join([x for x in list(df.iloc[i,1:].values) if pd.notnull(x)])
        frequency = df.iloc[i, 0]

        # Initialize an empty list to store sound positions for the current word
        sound_positions = []

        # Iterate through the split characters row (the row underneath)
        for char in df.iloc[i + 1, 1:]:
            if pd.notnull(char) and char not in exclude_chars:  # Check if the character is not null and not in the exclusion list
                sound_positions.append(char)

        # Add the word, frequency, and sound positions to the dictionary
        word_dict[word] = {'frequency': frequency, 'sound_positions': sound_positions}

    result_list = []
    for word, data in word_dict.items():
        frequency = data['frequency']
        sound_positions = data['sound_positions']
        
        for sound_position in sound_positions:
            result_list.append({
                'sound_position': sound_position,
                'word': word,
                'frequency': frequency
            })

    # Step 3: Convert the list of dictionaries into a DataFrame
    result_df = pd.DataFrame(result_list, 
                             columns=['sound_position', 'word', 'frequency'])

    # Sort the DataFrame based on the 'sound_position' column
    result_df.sort_values(by='sound_position', inplace=True)

    # Save the DataFrame to an Excel file
    outpath = os.path.join("output", "clustered", args.filename)
    result_df.to_excel(outpath, index=False)

    print(f"\n[INFO]: The sound positions result has been saved to {outpath}\n")

if __name__=="__main__":
    main()