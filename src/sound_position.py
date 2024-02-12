import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the Excel file into a DataFrame
df = pd.read_excel("data/GSA_TS_20.12.2023.xlsx")
col_remove = ["Label", "Translation", "Notes"]
df.drop(columns=col_remove, inplace=True)

# get the sound position list
sound_positions_df = pd.read_excel("data/Sound_positions.xlsx")
exclude_chars = ['#', '<de>', '<en>', '[ig]', 'h', 'l', 'v','|ß|','ü']
sound_positions_list = [s for s in sound_positions_df["sound_positions"].tolist() if s not in exclude_chars]

# Create an empty dictionary to store the results
word_dict = {}

# Iterate through every two rows in the dataframe
for i in range(0, len(df), 2):
    # Extract the word and frequency from the first row
    word = df.iloc[i, 0]
    frequency = df.iloc[i, 1]

    # Initialize an empty list to store sound positions for the current word
    sound_positions = []

    # Iterate through the split characters row (the row underneath)
    for char in df.iloc[i + 1, 2:]:
        if pd.notnull(char) and char not in exclude_chars:  # Check if the character is not null and not in the exclusion list
            sound_positions.append(char)

    # Add the word, frequency, and sound positions to the dictionary
    word_dict[word] = {'frequency': frequency, 'sound_positions': sound_positions}

# Print the resulting dictionary
print(word_dict)

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
result_df = pd.DataFrame(result_list, columns=['sound_position', 'word', 'frequency'])

# Sort the DataFrame based on the 'sound_position' column
result_df.sort_values(by='sound_position', inplace=True)

# Save the DataFrame to an Excel file
sound_positions_excel_path = 'output/clustered_graph_list/clustered_GSA_TS_20.12.2023.xlsx'
result_df.to_excel(sound_positions_excel_path, index=False)

print(f"The sound positions result has been saved to: {sound_positions_excel_path}")

# Print the resulting DataFrame
print(result_df)

