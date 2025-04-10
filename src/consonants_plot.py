import os
import re
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def input_parse():
    # Define argparse to get input, output paths
    parser = argparse.ArgumentParser(description="Creates visualizations and output tables")
    parser.add_argument("-f", 
                        "--filename", 
                        required=True, 
                        help="Input filename")
    parser.add_argument("-a",
                        "--alphabetical",
                        action="store_true")
    args = parser.parse_args()
    
    return args

def load_data(filename):
    # Read the Excel file
    filepath = os.path.join("data", "2_segmented_wordlists", filename)
    df = pd.read_excel(filepath)

    # Assuming your column name is 'Token', and 'Frequency' for the frequency column
    column_name = 'Token'
    frequency_column = 'Frequency'

    # Lowercase the words in the column and convert to string type
    df[column_name] = df[column_name].astype(str).str.lower()
    #df.dropna(inplace=True)

    return df

def process_consonants(df):

    # Initialize a dictionary to store consonant combinations and their frequencies
    consonant_combinations = {}

    consonants = ["b", "c", "d", "f", 
                  "g", "h", "j", "k",
                  "l", "m" , "n", "p" , 
                  "q", "r", "s", "ß" , "ſ" , 
                  "t", "v", "w", "x" , "z" , 
                  "þ", "ð", 
                  "‖i‖", "‖y‖", "‖u‖", "‖ï‖" , 
                  "‖î‖", "‖ì‖", "‖í‖", "‖ÿ‖", 
                  "‖ŷ‖", "‖ỳ‖", "‖ý‖", "‖ü‖" , 
                  "‖û‖", "‖ù‖", "‖ú‖", "‖ů‖"]

    # Define a regex pattern to match consecutive consonants
    # Escape special characters
    escaped_consonants = [re.escape(v) for v in consonants]

    # Join the list into a single regex pattern with alternation
    pattern = "|".join(escaped_consonants)

    # Compile the regex pattern
    compiled_pattern = re.compile(pattern)

    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        word = row["Token"].lower()
        frequency = row["Frequency"]
        
        # Exclude words that begin with '*' or '!'
        cleaned = re.sub('\*.*?\*', '', word)
        cleaned = re.sub('\!.*?\!', '', cleaned)
        
        if cleaned=="nan":
            pass    
        else:
            clusters = re.findall(r'\:(.*?)\:', cleaned)
            if clusters:
                for consonant_sequence in clusters:
                    if consonant_sequence in consonant_combinations:
                        consonant_combinations[consonant_sequence] += frequency
                    else:
                        consonant_combinations[consonant_sequence] = frequency
            else:
                consonants = re.findall(pattern, cleaned)
                for consonant in consonants:
                    if consonant in consonant_combinations:
                        consonant_combinations[consonant] += frequency
                    else:
                        consonant_combinations[consonant] = frequency

    return consonant_combinations

def normalize_key(key):
    # Remove punctuation using regex
    return re.sub(r'[^\w\s]', '', key)

def merge_dict_values(d):
    merged_dict = defaultdict(int)
    
    for key, value in d.items():
        normalized_key = normalize_key(key)
        merged_dict[normalized_key] += value
    
    return dict(merged_dict)

# Function to plot bar plots
def plot_bar(data, title, outfile):
    plt.figure(figsize=(10, 6))
    plt.bar(data['consonant'], data['Count'], color='skyblue')
    plt.xlabel('consonant')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    outpath = os.path.join("output", "graphs", outfile)
    plt.savefig(outpath)
    plt.show()

def plot_results(consonant_combinations, args):
    consonant_combinations = merge_dict_values(consonant_combinations)

    # Convert the dictionary to a DataFrame for plotting
    df_plot = pd.DataFrame(consonant_combinations.items(), columns=['consonant', 'Count'])

    if args.alphabetical == True:
        # Sort the DataFrame by consonant in ascending order
        df_plot = df_plot.sort_values(by='consonant', 
                                        ascending=True)
    else:
        # Sort the DataFrame by count in descending order
        df_plot = df_plot.sort_values(by='Count', 
                                        ascending=False)

    plot_bar(df_plot, "consonant counts", "consonant_counts_bar_plot.png")

    # Separate consonant sequences into monographs, digraphs, and trigraphs
    monographs = []
    digraphs = []
    trigraphs = []
    tetragraphs = []
    pentagraphs = []
    hexagraphs = []
    for consonant_seq in consonant_combinations.keys():
        cleaned = consonant_seq.replace('(', '').replace(')', '').replace('‖', '')
        if len(cleaned) == 1:
            monographs.append(consonant_seq)
        elif len(cleaned) == 2:
            digraphs.append(consonant_seq)
        elif len(cleaned) == 3:
            trigraphs.append(consonant_seq)
        elif len(cleaned) == 4:
            tetragraphs.append(consonant_seq)
        elif len(cleaned) == 5:
            pentagraphs.append(consonant_seq)
        elif len(cleaned) == 6:
            hexagraphs.append(consonant_seq)

    # Plot monographs
    monographs_data = {key: consonant_combinations[key] for key in monographs}
    if args.alphabetical == True:
        df_monographs = pd.DataFrame(monographs_data.items(), 
                                    columns=['consonant', 'Count']).sort_values(by='consonant', 
                                                                            ascending=True)
    else:
        df_monographs = pd.DataFrame(monographs_data.items(), 
                                    columns=['consonant', 'Count']).sort_values(by='Count', 
                                                                            ascending=False)
    plot_bar(df_monographs, 'Count of Monographs', 'monographs_bar_plot.png')

    # Plot digraphs
    digraphs_data = {key: consonant_combinations[key] for key in digraphs}
    if args.alphabetical == True:
        df_digraphs = pd.DataFrame(digraphs_data.items(), 
                                columns=['consonant', 'Count']).sort_values(by='consonant', 
                                                                        ascending=True)
    else:
        df_digraphs = pd.DataFrame(digraphs_data.items(), 
                        columns=['consonant', 'Count']).sort_values(by='Count', 
                                                                ascending=False)
    plot_bar(df_digraphs, 'Count of Digraphs', 'digraphs_bar_plot.png')

    # Plot trigraphs
    trigraphs_data = {key: consonant_combinations[key] for key in trigraphs}
    if args.alphabetical == True:
        df_trigraphs = pd.DataFrame(trigraphs_data.items(), 
                                    columns=['consonant', 'Count']).sort_values(by='consonant', 
                                                                            ascending=True)
    else:
        df_trigraphs = pd.DataFrame(trigraphs_data.items(), 
                            columns=['consonant', 'Count']).sort_values(by='Count', 
                                                                    ascending=False)
    plot_bar(df_trigraphs, 'Count of Trigraphs', 'trigraphs_bar_plot.png')

    #plot tetragraphs
    tetragraphs_data = {key: consonant_combinations[key] for key in tetragraphs}
    if args.alphabetical == True:
        df_tetragraphs = pd.DataFrame(tetragraphs_data.items(), 
                                    columns = ["consonant","Count"]).sort_values(by="consonant", 
                                                                            ascending=True)
    else:
        df_tetragraphs = pd.DataFrame(tetragraphs_data.items(), 
                                    columns = ["consonant","Count"]).sort_values(by="Count", 
                                                                            ascending=False)
    plot_bar(df_tetragraphs, "Count of Tetragraphs", "tetragraphs_bar_plot.png")

    #plot pentagraphs
    pentagraphs_data = {key: consonant_combinations[key] for key in pentagraphs}
    if args.alphabetical == True:
        df_pentagraphs = pd.DataFrame(pentagraphs_data.items(), 
                                    columns = ["consonant","Count"]).sort_values(by="consonant", 
                                                                            ascending=True)
    else:
        df_pentagraphs = pd.DataFrame(pentagraphs_data.items(), 
                                    columns = ["consonant","Count"]).sort_values(by="Count", 
                                                                            ascending=False)
    plot_bar(df_pentagraphs, "Count of Pentagraphs", "pentagraphs_bar_plot.png")

     #plot hexagraphs
    hexagraphs_data = {key: consonant_combinations[key] for key in hexagraphs}
    if args.alphabetical == True:
        df_hexagraphs = pd.DataFrame(hexagraphs_data.items(), 
                                    columns = ["consonant","Count"]).sort_values(by="consonant", 
                                                                            ascending=True)
    else:
        df_hexagraphs = pd.DataFrame(hexagraphs_data.items(), 
                                    columns = ["consonant","Count"]).sort_values(by="Count", 
                                                                            ascending=False)
    plot_bar(df_hexagraphs, "Count of Hexagraphs", "hexagraphs_bar_plot.png")

    return None

def save_tables(consonant_combinations, args):
    consonant_combinations = merge_dict_values(consonant_combinations)

    # Initialize lists to store data for the table
    monographs = []
    monographs_freq = []
    digraphs = []
    digraphs_freq = []
    trigraphs = []
    trigraphs_freq = []
    tetragraphs = []
    tetragraphs_freq = []
    pentagraphs = []
    pentagraphs_freq = []
    hexagraphs = []
    hexagraphs_freq = []

    # Iterate through each entry in the consonant counts dictionary
    for consonant, freq in consonant_combinations.items():
        cleaned = consonant.replace('(', '').replace(')', '').replace('‖', '')
        # Categorize the consonant sequences based on their lengths
        if len(cleaned) == 1:
            monographs.append(consonant)
            monographs_freq.append(freq)
        elif len(cleaned) == 2:
            digraphs.append(consonant)
            digraphs_freq.append(freq)
        elif len(cleaned) == 3:
            trigraphs.append(consonant)
            trigraphs_freq.append(freq)
        elif len(cleaned) == 4:
            tetragraphs.append(consonant)
            tetragraphs_freq.append(freq)
        elif len(cleaned) == 5:
            pentagraphs.append(consonant)
            pentagraphs_freq.append(freq)
        elif len(cleaned) == 6:
            hexagraphs.append(consonant)
            hexagraphs_freq.append(freq)

    # Determine the maximum length among the lists
    max_length = max(len(monographs), 
                     len(monographs_freq), 
                     len(digraphs), 
                     len(digraphs_freq), 
                     len(trigraphs), 
                     len(trigraphs_freq), 
                     len(tetragraphs), 
                     len(tetragraphs_freq),
                     len(pentagraphs),
                     len(pentagraphs_freq),
                     len(hexagraphs),
                     len(hexagraphs_freq))

    # Pad the lists with empty strings or NaN values to ensure they have the same length
    monographs += [''] * (max_length - len(monographs))
    monographs_freq += [np.nan] * (max_length - len(monographs_freq))
    digraphs += [''] * (max_length - len(digraphs))
    digraphs_freq += [np.nan] * (max_length - len(digraphs_freq))
    trigraphs += [''] * (max_length - len(trigraphs))
    trigraphs_freq += [np.nan] * (max_length - len(trigraphs_freq))
    tetragraphs += [''] * (max_length - len(tetragraphs))
    tetragraphs_freq += [np.nan] * (max_length - len(tetragraphs_freq))
    pentagraphs += [''] * (max_length - len(pentagraphs))
    pentagraphs_freq += [np.nan] * (max_length - len(pentagraphs_freq))
    hexagraphs += [''] * (max_length - len(hexagraphs))
    hexagraphs_freq += [np.nan] * (max_length - len(hexagraphs_freq))

    # Create a DataFrame for the table
    table_data = {
        'Monographs': monographs,
        'Monographs_freq': monographs_freq,
        'Digraphs': digraphs,
        'Digraphs_freq': digraphs_freq,
        'Trigraphs': trigraphs,
        'Trigraphs_freq': trigraphs_freq,
        'Tetragraphs': tetragraphs,
        'Tetragraphs_freq': tetragraphs_freq,
        'Pentagraphs': pentagraphs,
        'Pentagraphs_freq': pentagraphs_freq,
        'Hexagraphs': hexagraphs,
        'Hexagraphs_freq': hexagraphs_freq
    }

    # create and save tabular data
    df_table = pd.DataFrame(table_data)
    df_outpath = os.path.join("output", "frequencies", args.filename)
    df_table.to_excel(df_outpath, index=False)

    return None

def main():
    args = input_parse()
    # load data
    df = load_data(args.filename)
    # process all the consonant combos
    consonant_combinations = process_consonants(df)
    # save visualizations
    plot_results(consonant_combinations, args)
    # save output tables
    save_tables(consonant_combinations, args)

    print("\n[INFO]: Results are saved in the output folder\n")

if __name__=="__main__":
    main()