# Graphematic Analysis

This repository contains a collection of string processing and visualization scripts with the purpose to follow the steps of the *_Handbuch der ..._*.

The Python code in this repository can be used to replicate the analysis outlined in the handbook, with individual scripts responsible for performing separate steps of the analysis. 

This approach is not entirely automated and requires manual input and inspection of files at certain steps. Where necessary, those steps are outlined below.

## Requirements

In order to run this code locally on your own computer, it is recommended that you have Python ≥ 3.9 installed. The necessary requirements to run the code in this repository can be found in the ```requirements.txt``` file. These can be installed in the following way:

```bash 
# update pip
python -m pip install --upgrade pip
# install the requirements
python -m pip install -r requirements.txt
```

<details>
<summary> Advanced users</summary>
We recommend installing packages from the requirements.txt file in a virtual environment to avoid potential conflicts with existing Python installations. A minimal script for this is provided in setup.sh, which should be satisfactory for macOS and Linux. For Windows users, we recommend enabling the [Windows Subsytem for Linux](https://learn.microsoft.com/en-us/windows/wsl/about).
</details>

## Performing the analysis

### 0. Preparing the document

The initial transcribed document should be saved in Word doc format according to the instructions outlined in the *Handbuch*. There should preferably be no additional formating, such as footnotes and margin notes.

This initial wordlist should be saved in the folder called [```data/0_raw_data```](data/0_raw_data/).

### 1. Creating wordlists

With the transcribed document in place, we go through this document to extract a **wordlist**. This wordlist counts how many times each indvidual word form appears in the document.

To do this, we run the following code, changing the FILENAME parameter to match the name of your own file:

```bash
python src/wordlist_extract.py --filename FILENAME
```

The results from this script are saved in the folder [```data/1_wordlists```](data/1_wordlists/).

### 2. Segmented wordlists

The next step is to take this extracted wordlist and to create a **segmented word list**. This requires expert domain knowledge and is done manually, according to the instructions laid out in the *Handbuch*.

Once completed, the new file should be saved in the folder called [```data/2_segmented_wordlists```](data/2_segmented_wordlists/).

### 3. Parsing segments

Our next step takes the segmented wordlist and parses them in such a way that each graph appears in a separate column in an Excel worksheet. This allows for them to be manually linked up with specific sounds for the next steps of the analysis.

To produce the parsed, segmented wordlist, we run the following:

```bash
python src/word_parser.py --filename FILENAME
```

The results from this script are saved in the folder [```data/3_parsed_segmented```](data/3_parsed_segmented/).

### 4. Annotating the segments

The outputs from the previous step are manually inspected and annotated according to the instructions outlined in the *Handbuch*. In the resulting file, we have all of the individual graphs in the document aligned with their specific sound position. 

This annotated, segmented wordlist should be saved in the folder [```data/4_annotated_segmented```](data/4_annotated_segmented/).

### 5. Clustering sound_positions

We then take the annotated, segmented wordlist and calculate the occurrence of different sound positions in the new document. The output from this is a table showing all occurrences of each individual sound position, the words in which those occur, and the number of occurrences (of each word).

This is created using the following script:

```bash
python src/sound_position.py --filename FILENAME
```

The output from this step is saved in the folder called [```output/clustered_graph_list```](output/clusted).

### 6. Manually rearranging data

As outlined in the *Handbuch*, the next step is to manually sort and re-arrange these outputs according to morpheme type and allographs. 

The output from this step should be saved in the folder [```data/5_boxes_raw```](data/5_boxes_raw/).

### 7a. Calculating leading graphs

The next step is to calculate the *leading graph* - in other words, the allograph which covers more than 50% of occurences in the original document.

To calculate this value, we run the following, changing the filenames as you please:

```bash
python src/leading_graph.py --filename FILENAME --output FILENAME
```

The result from this script will be saved in the folder called [```data/6_boxes```](data/6_boxes/).

### 7b. Calculating distances

We can finally calculate the *graphemic distance* between any two graphemes as extracted from a document using the previous steps. To do this, we specify specficially which graphemes we wish to compare.

To do this, we run the following code:

```bash
python3.11 src/graphematic.py --files FILE1 FILE2 ... --outfile FILENAME
```

For example, to compare hypothetical results for *{â}_closed_syllable* vs *{â}_open_syllable*:

```bash
python3.11 src/graphematic.py --files {â}_closed_syllable.xlsx {â}_open_syllable.xlsx --outfile results.xlsx
```

In any case, the results are saved in the folder called [```output/distance```](output/distance/).

### 8. Visualizing vowel distribution

Finally, we can create simple barplots to show the distribution of vowels and vowel clusters in our original document. For this, we only need the segmented wordlist created as part of step two above. 

We can present the results either by ordering the vowel (clusters) alphabetically, or in order of descending size. 

To create results with vowels arranged alphabetically:

```bash
python src/bar_plot.py --filename FILENAME --alphabetical
```

To plot based on descending frequency, simply remove the final flag:

```bash
python src/bar_plot.py --filename FILENAME
```

In each case, the visualizations are saved into the folder called [```output/graphs```](output/graphs/). A table of the same results is saved alongside this in the folder called [```output/frequencies```](output/frequencies).