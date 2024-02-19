import os
import re
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

    return df

def process_vowels(df):

    # Initialize a dictionary to store vowel combinations and their frequencies
    vowel_combinations = {}

    vowels = ["a","ä","â","à","á","å",
            "e","ë","ê","è","é",
            "i","ï","î","ì","í",
            "o","ö","ô","ø","ò","ó",
            "u","ü","û","ù","ú","ů",
            "y","ÿ","ŷ","ỳ","ý",
            "æ","œ","œ̂","œ̀","œ́",
            "‖j‖","‖j̈‖","‖ĵ‖","‖j́‖",
            "‖v‖","‖v̈‖","‖v̂‖","‖v̀‖","‖v́‖","‖v̊‖",
            "‖w‖","‖ẅ‖","‖ŵ‖","‖ẁ‖","‖ẃ‖","‖ẘ‖",
            "(i)","(ï)","(î)","(ì)","(í)",
            "(y)","(ÿ)","(ŷ)","(ỳ)","(ý)",
            "(j)","(j̈)","(ĵ)","(j́)",
            "(u)","(ü)","(û)","(ù)","(ú)","(ů)",
            "(v)","(v̈)","(v̂)","(v̀)","(v́)","(v̊)",
            "(w)","(ẅ)","(ŵ)","(ẁ)","(ẃ)","(ẘ)"]

    # Define a regex pattern to match consecutive vowels
    vowel_pattern = r"([" + "".join(map(re.escape, vowels)) + r"]{2,})"
    vowel_regex = re.compile(vowel_pattern)

    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        word = row["Token"]
        frequency = row["Frequency"]
        
        # Exclude words that begin with '*' or '!'
        if word.startswith("*") or word.startswith("!"):
            continue
        
        # Initialize a flag to track whether a sequence of consecutive vowels has been found
        consecutive_vowels_found = False
        
        # Find all matches of consecutive vowels in the word
        for match in vowel_regex.finditer(word):
            vowel_sequence = match.group(0)
            if vowel_sequence:
                # If a consecutive vowel sequence is found, set the flag and add it to the dictionary
                consecutive_vowels_found = True
                if vowel_sequence in vowel_combinations:
                    vowel_combinations[vowel_sequence] += frequency
                else:
                    vowel_combinations[vowel_sequence] = frequency
        
        # Filter out non-vowel characters and count individual vowels
        for i, char in enumerate(filter(lambda c: c in vowels, word)):
            # If the current character is not part of a consecutive vowel sequence
            if not consecutive_vowels_found:
                if char in vowel_combinations:
                    vowel_combinations[char] += frequency
                else:
                    vowel_combinations[char] = frequency

            # Check if the next character is 'h' or 'j'
            if i < len(word) - 1 and word[i+1] in ['h', 'j']:
                # Add 'h' or 'j' to the current vowel or vowel sequence
                if char in vowel_combinations:
                    vowel_combinations[char + word[i+1]] = frequency
                elif consecutive_vowels_found:
                    if vowel_sequence + word[i+1] in vowel_combinations:
                        vowel_combinations[vowel_sequence + word[i+1]] += frequency
                    else:
                        vowel_combinations[vowel_sequence + word[i+1]] = frequency

    #removing the unwanted characters from the dictionary
    # Iterate over the keys in the vowel_combinations dictionary
    for key in list(vowel_combinations.keys()):
        # Remove unwanted characters from the key
        cleaned_key = key.replace("(", "").replace(")", "").replace("‖", "")
        # Check if the cleaned key is different from the original key
        if cleaned_key != key:
            # Update the dictionary with the cleaned key and its corresponding value
            vowel_combinations[cleaned_key] = vowel_combinations.pop(key)

    return vowel_combinations

# Function to plot bar plots
def plot_bar(data, title, outfile):
    plt.figure(figsize=(10, 6))
    plt.bar(data['Vowel'], data['Count'], color='skyblue')
    plt.xlabel('Vowel')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    outpath = os.path.join("output", "graphs", outfile)
    plt.savefig(outpath)
    plt.show()

def plot_results(vowel_combinations, args):

    # Convert the dictionary to a DataFrame for plotting
    df_plot = pd.DataFrame(vowel_combinations.items(), columns=['Vowel', 'Count'])

    df_plot['Vowel'].str.replace('(', '')
    df_plot['Vowel'].str.replace(')', '')
    df_plot['Vowel'].str.replace('‖', '')

    if args.alphabetical == True:
        # Sort the DataFrame by vowel in ascending order
        df_plot = df_plot.sort_values(by='Vowel', 
                                        ascending=True)
    else:
        # Sort the DataFrame by count in descending order
        df_plot = df_plot.sort_values(by='Count', 
                                        ascending=False)

    plot_bar(df_plot, "Vowel counts", "vowel_counts_bar_plot.png")

    # Separate vowel sequences into monographs, digraphs, and trigraphs
    monographs = []
    digraphs = []
    trigraphs = []
    tetragraphs = []
    for vowel_seq in vowel_combinations.keys():
        if len(vowel_seq) == 1:
            monographs.append(vowel_seq)
        elif len(vowel_seq) == 2:
            digraphs.append(vowel_seq)
        elif len(vowel_seq) == 3:
            trigraphs.append(vowel_seq)
        elif len(vowel_seq) == 4:
            tetragraphs.append(vowel_seq)

    # Plot monographs
    monographs_data = {key: vowel_combinations[key] for key in monographs}
    if args.alphabetical == True:
        df_monographs = pd.DataFrame(monographs_data.items(), 
                                    columns=['Vowel', 'Count']).sort_values(by='Vowel', 
                                                                            ascending=True)
    else:
        df_monographs = pd.DataFrame(monographs_data.items(), 
                                    columns=['Vowel', 'Count']).sort_values(by='Count', 
                                                                            ascending=False)
    plot_bar(df_monographs, 'Count of Monographs', 'monographs_bar_plot.png')

    # Plot digraphs
    digraphs_data = {key: vowel_combinations[key] for key in digraphs}
    if args.alphabetical == True:
        df_digraphs = pd.DataFrame(digraphs_data.items(), 
                                columns=['Vowel', 'Count']).sort_values(by='Vowel', 
                                                                        ascending=True)
    else:
        df_digraphs = pd.DataFrame(digraphs_data.items(), 
                        columns=['Vowel', 'Count']).sort_values(by='Count', 
                                                                ascending=False)
    plot_bar(df_digraphs, 'Count of Digraphs', 'digraphs_bar_plot.png')

    # Plot trigraphs
    trigraphs_data = {key: vowel_combinations[key] for key in trigraphs}
    if args.alphabetical == True:
        df_trigraphs = pd.DataFrame(trigraphs_data.items(), 
                                    columns=['Vowel', 'Count']).sort_values(by='Vowel', 
                                                                            ascending=True)
    else:
        df_trigraphs = pd.DataFrame(trigraphs_data.items(), 
                            columns=['Vowel', 'Count']).sort_values(by='Count', 
                                                                    ascending=False)
    plot_bar(df_trigraphs, 'Count of Trigraphs', 'trigraphs_bar_plot.png')

    #plot tetragraphs
    tetragraphs_data = {key: vowel_combinations[key] for key in tetragraphs}
    if args.alphabetical == True:
        df_tetragraphs = pd.DataFrame(tetragraphs_data.items(), 
                                    columns = ["Vowel","Count"]).sort_values(by="Vowel", 
                                                                            ascending=True)
    else:
        df_tetragraphs = pd.DataFrame(tetragraphs_data.items(), 
                                    columns = ["Vowel","Count"]).sort_values(by="Count", 
                                                                            ascending=False)
    plot_bar(df_tetragraphs, "Count of Tetragraphs", "tetragraphs_bar_plot.png")

    return None

def save_tables(vowel_combinations, args):
    # Initialize lists to store data for the table
    monographs = []
    monographs_freq = []
    digraphs = []
    digraphs_freq = []
    trigraphs = []
    trigraphs_freq = []
    tetragraphs = []
    tetragraphs_freq = []

    # Iterate through each entry in the vowel counts dictionary
    for vowel, freq in vowel_combinations.items():
        # Categorize the vowel sequences based on their lengths
        if len(vowel) == 1:
            monographs.append(vowel)
            monographs_freq.append(freq)
        elif len(vowel) == 2:
            digraphs.append(vowel)
            digraphs_freq.append(freq)
        elif len(vowel) == 3:
            trigraphs.append(vowel)
            trigraphs_freq.append(freq)
        elif len(vowel) == 4:
            tetragraphs.append(vowel)
            tetragraphs_freq.append(freq)

    # Determine the maximum length among the lists
    max_length = max(len(monographs), len(monographs_freq), len(digraphs), len(digraphs_freq), len(trigraphs), len(trigraphs_freq), len(tetragraphs), len(tetragraphs_freq))

    # Pad the lists with empty strings or NaN values to ensure they have the same length
    monographs += [''] * (max_length - len(monographs))
    monographs_freq += [np.nan] * (max_length - len(monographs_freq))
    digraphs += [''] * (max_length - len(digraphs))
    digraphs_freq += [np.nan] * (max_length - len(digraphs_freq))
    trigraphs += [''] * (max_length - len(trigraphs))
    trigraphs_freq += [np.nan] * (max_length - len(trigraphs_freq))
    tetragraphs += [''] * (max_length - len(tetragraphs))
    tetragraphs_freq += [np.nan] * (max_length - len(tetragraphs_freq))

    # Create a DataFrame for the table
    table_data = {
        'Monographs': monographs,
        'Monographs_freq': monographs_freq,
        'Digraphs': digraphs,
        'Digraphs_freq': digraphs_freq,
        'Trigraphs': trigraphs,
        'Trigraphs_freq': trigraphs_freq,
        'Tetragraphs': tetragraphs,
        'Tetragraphs_freq': tetragraphs_freq
    }

    # create and save tabular data
    df_table = pd.DataFrame(table_data)
    df_outpath = os.path.join("output", "frequency_tables", args.filename)
    df_table.to_excel(df_outpath, index=False)

    return None

def main():
    args = input_parse()
    # load data
    df = load_data(args.filename)
    # process all the vowel combos
    vowel_combinations = process_vowels(df)
    # save visualizations
    plot_results(vowel_combinations, args)
    # save output tables
    save_tables(vowel_combinations, args)

    print("\n[INFO]: Results are saved in the output folder\n")

if __name__=="__main__":
    main()