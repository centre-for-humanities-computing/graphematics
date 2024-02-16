# import pandas
import os
import re
import string
import argparse
from collections import Counter, OrderedDict
from docx import Document
import pandas as pd

def input_parse():
    # Define argparse to get input, output paths
    parser = argparse.ArgumentParser(description="Creates wordlists from full texts.")
    parser.add_argument("-f", 
                        "--filename", 
                        required=True, 
                        help="Input filename")
    args = parser.parse_args()
    
    return args

def cleanup(s):
    """
    remove punctuation before counting
    """
    s = s.replace(".", "")
    s = s.replace(",", "")
    s = s.replace(":", "")
    s = s.replace(";", "")
    s = s.replace("?", "")
    s = s.replace("!", "")
    s = s.replace("/", "")
    s = s.replace(">", "")
    s = s.replace("<", "")
    s = s.replace("- ", "")
    s = s.rstrip()
    
    return s

def paren(s):
    if "(" in s:
        if ")" in s:
            pass
        else:
            s = s.replace("(", "")
    if ")" in s:
        if "(" in s:
            pass
        else:
            s = s.replace(")", "")
    
    return s

def ugly_regex(raw_text):
    # regex matching according to instructions
    raw_text = re.sub(r'  ', ' ', raw_text)
    raw_text = re.sub(r'\^.*?^}\s?', '', raw_text)      # braces
    raw_text = re.sub(r'\<.+?\>', '', raw_text)         # square brackets
    raw_text = re.sub(r'\{.*?\}\s?', '', raw_text)      # braces
    raw_text = re.sub(r'(\w)\[\-\d+\]', r'\1-', raw_text)  # hypens + page
    raw_text = re.sub(r'(\w)\[\d+\]', r'\1-', raw_text)  # hypens + page
    raw_text = re.sub(r'\- ', '', raw_text)            # hyphens + page 2
    raw_text = re.sub(r'\[.*?\]', '', raw_text)         # page numbers
    raw_text = re.sub(r'\.\s?|\:\s?|\;\s?|\:\s?|\!\s?', ' ', raw_text) # punctuation
    raw_text = re.sub(r'\_\_', '#####', raw_text)       # transforms
    raw_text = re.sub(r'\_', '####', raw_text)          # transforms
    raw_text = re.sub(r'\|', '###', raw_text)           # transforms
    raw_text = re.sub(r'\=\s?', '##', raw_text)            # transforms

    return raw_text

def doc_process(doc):
    # fix words over line breaks
    raw_text = ""
    for i in doc.paragraphs:
        if i.text == "":
            pass
        else:
            line = i.text
            if line[-1]=="-":
                raw_text += line[:-1]
            else:
                raw_text += line + " "
    regexed_text = ugly_regex(raw_text)
    # create list of all tokens
    tokens = regexed_text.split()
    cleaned = []
    for token in tokens:
        if len(token)==1 and token.isalnum() == False:
            pass
        else:
            token = cleanup(token)
            token = paren(token)
            cleaned.append(token)
    # count tokens
    wordcounts = Counter(cleaned)
    # created sorted dic & final cleanup 
    sortedDict = dict( sorted(wordcounts.items(), key=lambda x: x[0].lower()) )

    tups = []
    for k,v in sortedDict.items():
        if any(i.isdigit() for i in k):
            pass
        else:
            tup = (k,v)
            tups.append(tup)

    return tups

def main():
    args = input_parse()

    inpath = os.path.join("data", "0_raw_data", args.filename)
    #loading in the files
    doc = Document(inpath)
    tups = doc_process(doc)
    df = pd.DataFrame(tups, columns=["Token", "Frequency"])
    df = df[df["Token"] != ""]
    df["Label"] = ""
    df["Translation"] = ""
    #save them to excel
    final_df = df.sort_values(by=["Token"], key=lambda x: x.str.lower(), ascending=True)
    outfile = args.filename.split(".")[0]+".xlsx"
    outpath = os.path.join("data", "1_wordlists", f"wordlist_{outfile}")
    df.to_excel(outpath, index=False)
    print(f"\n[INFO]: The tokenized wordlist results has been saved to: {outpath}\n")


if __name__=="__main__":
    main()