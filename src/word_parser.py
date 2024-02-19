import os
import pandas as pd
import numpy as np
import argparse


def input_parse():
    parser = argparse.ArgumentParser()
    #add arguments
    parser.add_argument("-f", "--filename", help = "pick which dataset you want", type = str)
    # save arguments to be parsed from the CLI
    args = parser.parse_args()

    return args

# Define the function
def parse(s: str) -> list[str]:
    tokens = []
    current = 0
    token_start = -1

    # Define list case-sensitive list of Vowels, without lowercasing
    vowels = ["a", "ä", "æ", "e", "i", "o", "ö", "ø", "u", "ü", "y", 
              "A", "Ä", "Æ", "E", "I", "O", "Ö", "Ø", "U", "Ü", "Y"]
    vowel_frequency = {}

    # getting everything wrapped by : :  their own cell
    while current < len(s):
        if s[current] == ":":
            if (token_start != -1) and (s[token_start] == ":"):
                tokens.append(s[token_start : current + 1])
                token_start = -1
            elif token_start == -1:
                token_start = current

        # getting everything wrapped by | | their own cell
        elif s[current] == "|":
            if (token_start != -1) and (s[token_start] == "|"):
                tokens.append(s[token_start : current + 1])
                token_start = -1
            elif token_start == -1:
                token_start = current

        # getting everything wrapped by ! ! their own cell
        elif s[current] == "!":
            if (token_start != -1) and (s[token_start] == "!"):
                tokens.append(s[token_start : current + 1])
                token_start = -1
            elif token_start == -1:
                token_start = current
        
        #Getting everything wrapped by < > their own cell
        elif s[current] == "<":
            token_start = current
        elif s[current] == ">":
            tokens.append(s[token_start : current + 1])
            token_start = -1
        
        elif s[current] == "[":
            # Check for content between "*"
            next_index = current + 1
            while next_index < len(s) and s[next_index] != "]":
                next_index += 1

            # Include content between "*" in the same cell
            tokens.append(s[current:next_index + 1])
            current = next_index  # Update current index
        
        # Getting everything wrapped by () their own cell
        elif s[current] == "(":
            token_start = current
        elif s[current] == ")":
            tokens.append(s[token_start : current + 1])
            token_start = -1
        
        #Get consecutive # their own cell
        elif s[current] == "#":
            # Check for consecutive "#" symbols
            next_index = current + 1
            while next_index < len(s) and s[next_index] == "#":
                next_index += 1

            tokens.append(s[current:next_index])
            current = next_index - 1  # Update current index

        elif s[current] == "*":
            # Check for content between "*"
            next_index = current + 1
            while next_index < len(s) and s[next_index] != "*":
                next_index += 1

            # Include content between "*" in the same cell
            tokens.append(s[current:next_index + 1])
            current = next_index  # Update current index

        elif token_start == -1:
            # Check if the current and next characters are special strings
            special_strings = ["‖i‖", "‖y‖", "‖u‖", "‖j‖", "‖v‖", "‖w‖", 
                               "‖I‖", "‖Y‖", "‖U‖", "‖J‖", "‖V‖", "‖W‖"]
            for string in special_strings:
                if s.startswith(string, current):
                    tokens.append(string)
                    current += len(string) - 1  # Skip the characters of the special string
                    token_start = -1
                    break
            else:
                # Check if the current and next characters are both vowels
                if (
                    current < len(s) - 1
                    and s[current] in vowels
                    and (s[current + 1] in vowels or s[current + 1] in {"h", "j"})
                ):
                    tokens.append(s[current])

                    # Check for additional characters like "h" or "j"
                    next_index = current + 1
                    while (
                        next_index < len(s)
                        and (s[next_index] in {"h", "j"} or s[next_index] in vowels)
                    ):
                        tokens[-1] += s[next_index]
                        next_index += 1

                    current = next_index - 1  # Update current index
                    # Update the vowel_frequency dictionary
                    #if tokens[-1] in vowel_frequency:
                    #    vowel_frequency[tokens[-1]] += 1
                    #else:
                    #    vowel_frequency[tokens[-1]] = 1

                else:
                    tokens.append(s[current])

        current += 1

    return tokens

# Adding row of NaN underneath every row 
def Add_Empty_Values(df):
    empty_values = np.full_like(df.values, np.nan)
    data = np.hstack([df.values, empty_values]).reshape(-1, df.shape[1])
    df_ordered = pd.DataFrame(data, columns=df.columns)
    return df_ordered

def main():
    # intialise arguments 
    args = input_parse()

    # define paths
    datapath = os.path.join("data", "2_segmented_wordlists", args.filename)
    df = pd.read_excel(datapath)
    df = df.dropna()

    # apply parse function
    df["ParsedTokens"] = df['Token'].apply(parse)

    # make a wide dataframe
    wide_df = pd.DataFrame(df["ParsedTokens"].to_list(), columns=[f"Token_{i}" for i in range(df["ParsedTokens"].apply(len).max())])

    # make result df
    result_df = pd.concat([df, wide_df], axis=1)

    # add empty rows
    ordered_results = Add_Empty_Values(result_df)

    # remove the ParsedTokens column
    col_remove = "ParsedTokens"

    fin_df = ordered_results.drop(col_remove, axis=1)

    outpath = os.path.join("data", "3_parsed_segmented", f"segmented_{args.filename}")
    #save to excel format
    fin_df.to_excel(outpath, index=False)
    print(f"\n[INFO]: The word parser results has been saved to {outpath}\n")
    

if __name__ == "__main__":
    main()