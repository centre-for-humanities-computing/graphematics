# Graphematic Analysis

This repository contains a collection of string processing and visualization scripts with the purpose to follow the steps of the *_Handbuch der ..._*.

The Python code in this repository can be used to replicate the analysis outlined in the handbook, with individual scripts responsible for performing separate steps of the analysis. 

This approach is not entirely automated and requires manual input and inspection of files at certain steps. Where necessary, those steps are outlined below.

## Requirements

In order to run this code locally on your own computer, it is recommended that you have Python ≥ 3.9 installed. 

<details>
<summary> Advanced users</summary>
We recommend installing packages from the requirements.txt file in a virtual environment to avoid potential conflicts with existing Python installations. A minimal script for this is provided in setup.sh, which should be satisfactory for macOS and Linux. For Windows users, we recommend enabling the [Windows Subsytem for Linux](https://learn.microsoft.com/en-us/windows/wsl/about).
</details>


The first step is running the ´´´word_parser.py´´´ script, which takes data from the ´´´data/Wordlists´´´ folder and segments them so they can be annotated. Run this script by adding the 
"-f" argument to the commandline, which should be the name of the wordlist you want to segment. As long as the data is in the correct folder, there is no need to specify which folder it is in.

The second step is taking an annotated segmented wordlist - that is, the product of ´´´word_parser.py´´´ which has then been manually annotated, and running that through the ´´´sound_position.py´´´ script.
Here you need to go into the script and specify which file is the input. Then you can just run it, and it saves the output to ´´´output/clustered_graph_list´´´, but you need to specify the name of the output file, also in the script

To get the MT boxes with percentages, you run the ´´´leading_graph.py´´´ script with the commandline argument -i  for "input" and -o for "output". The input should be from the ´´´boxes_raw´´´
folder, and the output should be put into the ´´´boxes´´´ folder. It is important that these boxes are in the correct format, like the example in the repo. 

To get the graphematic distances you run the graphematic.py script followed by the files you want to do it on, as well as the –-outpath command, which defines where and under which name the resulting file will be saved. 
The files should be given their relative path. 

Also enclosed in the repository is a script that takes a segmented wordlist and turns it back into a normal wordlist, but that might not be necessary. 
