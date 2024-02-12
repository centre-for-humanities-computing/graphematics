# import pandas
import pandas as pd

# defining paths
#PA_path = "data/GSA_PA_14.12.2023.xlsx"
#TS_path = "data/GSA_TS_14.12.2023.xlsx"
SWL_PA_path = "data/segmented_wordlists/SWL_PA_wordlist.xlsx"
#loading in the files
#df_PA = pd.read_excel(PA_path)
#df_TS = pd.read_excel(TS_path)
df_SWL_PA = pd.read_excel(SWL_PA_path)

#extracting the columns to new dfs
#new_PA = df_PA[["Token", "Frequency"]].copy()
#new_TS = df_TS[["Token", "Frequency"]].copy()
new_SWL_PA = df_SWL_PA[["Token", "Frequency"]].copy()
# removing na's
#fin_PA = new_PA.dropna()
#fin_TS = new_TS.dropna()
fin_SWL_PA = new_SWL_PA.dropna()

#save them to excel
#PA_excel = "data/Wordlists/PA_wordlist.xlsx"
#TS_excel = "data/Wordlists/TS_wordlist.xlsx"
SWL_PA_excel = "data/Wordlists/SWL_PA_wordlist_new.xlsx"

#fin_PA.to_excel(PA_excel, index=False)
#fin_TS.to_excel(TS_excel, index=False)
fin_SWL_PA.to_excel(SWL_PA_excel, index=False)
#print(fin_PA)
#print(fin_TS)