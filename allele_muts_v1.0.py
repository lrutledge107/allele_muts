#!/usr/bin/env python
# coding: utf-8

# # allele_muts.py
# ### Incorporating Mutation Codes into STR Genotypes Output from SatAnalyzer

# #### Step 1: Transforming Output from SatAnalyzer to Input for allele_muts.py

# In[1]:


# Import required packages and define paths

import pandas as pd
import os
import numpy as np
import glob

dir_path = os.getcwd()
in_path = os.path.join(dir_path, 'data', 'input')
out_path = os.path.join(dir_path,'data','merged', 'MergedInput.csv')


# In[2]:


# Combine all the *_genotypes_mra_final.txt" SatAnalyzer output files into a single merged file
# Output is put in the "merged" folder 
# Create a file list and indicate files in the path
file_list = glob.glob(in_path + "/*_genotypes_mra_final.txt")

# Create an empty list
gtmra_list = []
 
# Loop through files and append the files into a list
for file in file_list:
    gtmra_list.append(pd.read_csv(file, sep='\t'))

# Concatenate all DataFrames in the list into a single DataFrame, return a new DataFrame.
gtmra_merged = pd.concat(gtmra_list, ignore_index=True)
 
# Sort the output file according to Sample and then Locus
gtmra_merged.sort_values(["Sample", "Locus"], axis=0, 
                 ascending=True, inplace=True)

# Remove dropped loci (STR003, STR005, STR023, STR024, STR025). Note that this step may not be necessary in the future when they are removed from the assay and no longer appear in the output.
gtmra_merged = gtmra_merged[gtmra_merged["Locus"].str.contains("Cfam_STR003|Cfam_STR005|Cfam_STR023|Cfam_STR024|Cfam_STR025") == False]

# Export the dataframe into an excel file with specified name (data/merged/MergedInput.csv).
gtmra_merged.to_csv(out_path, index=False)


# In[3]:


# Identify path to current working directory
dir_path = os.getcwd()

# Identify path to merged input file
data_path = os.path.join(dir_path, 'data', 'merged', 'MergedInput.csv')

# Convert merged file into a dataframe
df_merged = pd.read_csv(data_path)

# Check dataframe - optional
# df_merged.head()


# #### Step 2: Pre-Processing
# 
# We want to process the input spreadsheet to achieve the following goals
#  1. Create a new column called allele_call which is a duplicate of the Allele column except when there is a
#     case for a sample at a locus that has no Putative Allele = 'Y' and no Allele = -99, in which case
#     we will replace all the rows associated with that Sample and Locus with a single row with the
#     allele_call = -99
#  2. If allele = -99 (regardless of Putative Allele flag), then it should be brought through as a final allele in the allele_mut column.
#  3. All other instances where Putative Allele is N should be excluded from the final genotype file. 
#  4. At this stage, where only the Putative Allele = Y (or Allele = -99), where there is only one row entry for a sample at a specific locus, then that entry needs to be duplicated in the next row. So that the output ensures each Locus for each Sample has two (and only two) entries. 

# In[4]:


# Create a dataframe of genotypes with two alleles at each locus
# Each output is put in the "processed" folder

def is_unique(s):
    a = s.to_numpy() # s.values (pandas<0.24)
    return (a[0] == a).all()

df_pre00 = df_merged
df_pre00['allele_call'] = df_pre00.loc[:, 'Allele']

# create a new column with Sample concatenated to Locus for use finding duplicates
df_pre00['Sample_Locus'] = df_pre00['Sample'].map(str) + '_' + df_pre00['Locus'].map(str)

grps = df_pre00.groupby('Sample_Locus')

grp_keep = []
for grp_key, grp_df in grps:

    if is_unique(grp_df['PutativeAllele']) and grp_df['PutativeAllele'].iat[0] == 'N':
        # print(grp_key)
        temp_df = grp_df.iloc[[0]].copy()
        temp_df['allele_call'] = -99
        grp_keep.append(temp_df)
    else:
        grp_keep.append(grp_df)

df_pre0 = pd.concat(grp_keep, axis=0, ignore_index=True)

data_path = os.path.join(dir_path, 'data', 'processed', 'MergedInput_pre0.csv')
df_pre0 = df_pre0.reset_index(drop=True) 
df_pre0.to_csv(data_path, index=False)

# Check dataframe - optional
# df_pre0.head()


# In[13]:


# Identify Putative Allele = Y and allele call = -99 to create actual genotypes

df_pre1 = df_pre0[(df_pre0['PutativeAllele'] == 'Y') | (df_pre0['allele_call'] == -99)]

data_path = os.path.join(dir_path, 'data', 'processed', 'MergedInput_pre1.csv')
df_pre1 = df_pre1.reset_index(drop=True) 
df_pre1.to_csv(data_path, index=False)

# Check dataframe - optional
# df_pre1.head()


# In[14]:


# Separate out the rows that only have a single row and make a new dataframe
# Output goes to "processed" folder

# This will give all the rows that are singletons
df_pre2 = df_pre1[~df_pre1['Sample_Locus'].duplicated(keep=False)]

data_path = os.path.join(dir_path, 'data', 'processed', 'MergedInput_pre2.csv')
df_pre2 = df_pre2.reset_index(drop=True) 
df_pre2.to_csv(data_path, index=False)

# Check dataframe - optional
# df_pre2.head()


# In[15]:


# Now we want to concatenate the singleton rows (df_pre2) with the previous dataframe (df_pre1) and sort the dataframe based on Sample then Locus
# Output goes to "processed" folder

df_pre3 = pd.concat([df_pre1,df_pre2], ignore_index=True)
df_pre3 = df_pre3.sort_values('Sample_Locus', ascending=False)

data_path = os.path.join(dir_path, 'data', 'processed', 'MergedInput_pre3.csv')
df_pre3 = df_pre3.reset_index(drop=True) 
df_pre3.to_csv(data_path, index=False)

# Check dataframe - optional
# df_pre3.tail()


# In[23]:


# This section does some checks to make sure the data is correct - optional
#   For this particular dataset:
#   * in the end there should be 84 samples with 26*2 rows (26 loci with 2 allele calls - alleles call may be the same at a locus).
#   * so number of rows (excluding header) should be 84*26*2 = 4368 (ie. number of samples * number of loci * number of alleles/sample/locus)
# Ouput shows number of samples and only prints the number of loci for each sample if the total doesn't equal the loci x 2 indicated

# Note that the numbers here for checking need to be changed for different input datasets with different number of samples and/or loci

Sample_Names =list(df_pre3['Sample'].unique())
print(f'Number of Samples: {len(Sample_Names)}')
for name in Sample_Names:
    Samples = df_pre3[df_pre3['Sample']== name]
    N = len(Samples)
    if N != 52:
        print(f'Number of loci for sample {name}: {len(Samples)}')
        locus_names = list(Samples['Locus'])
        for locus_name in locus_names:
            print(locus_name)


# In[24]:


# Identify the df_pre3 as the working dataframe
df = df_pre3

# Find unique instances of the mrabase column - which indicates the repeat pattern
mrabase_unique = df['MRABase'].unique()

# Print the unique mrabase entries to screen - optional
# print(mrabase_unique)


# In[27]:


# Prepare to create mutation codes
def find_mra_mut_code(df_col):
    val_unique = df_col.unique()
    code_base = 0
    code_num = []
    code_str = []
    for x in val_unique:
        if (len(x) > 4):
            code_base = code_base +1
            code_num.append(code_base)
            code_str.append(x)

    return code_num, code_str


# In[28]:


mra_code_num, mra_code_str = find_mra_mut_code( df['MRABase'])

# Print codes and mutations to screen - optional
# print(mra_code_num)
# print(mra_code_str)


# In[29]:


# Find unique SnpsFF
snpsff_unique = df['SnpsFF'].unique()

# Print snpsFF to screen - optional
# print(snpsff_unique)


# In[30]:


def find_snps_mut_code(df_col):
    val_unique = df_col.unique()
    code_base = 0
    code_num = []
    code_str = []
    for x in val_unique:
        if isinstance(x, str):
            code_base = code_base +1
            code_num.append(code_base)
            code_str.append(x)

    return code_num, code_str


# In[31]:


snpsff_code_num, snpsff_code_str = find_snps_mut_code( df['SnpsFF'])

# Print snpsFF code number and mutation to screen - optional
# print(snpsff_code_num)
# print(snpsff_code_str)


# In[32]:


snpsrf_unique = df['SnpsRF'].unique()

# Print snpsRF_unique to screen - optional
# print(snpsrf_unique)


# In[33]:


snpsrf_code_num, snpsrf_code_str = find_snps_mut_code( df['SnpsRF'])

# Print snpsRF code number and mutation to screen - optional
# print(snpsrf_code_num)
# print(snpsrf_code_str)


# In[34]:


def create_allele_mut_code(allele, mrabase_mut_code, snpsff_mut_code, snpsrf_mut_code):
    assert mrabase_mut_code < 100
    assert snpsff_mut_code < 100
    assert snpsrf_mut_code < 100
    if allele < 0:
        return allele
    else:
        res = \
            allele*pow(10,6) + \
                mrabase_mut_code*pow(10,4) + \
                    snpsff_mut_code*pow(10,2) + \
                    snpsrf_mut_code
        return res


# In[35]:


def mut_code_from_str(str, str_code):
        try:
            return str_code.index(str) + 1
        except ValueError:
            return 0


# In[36]:


# Prepare to create an output file of mutation codes

class AlleleMutCodeBook:
    def __init__(self, mra_code_str, snpsff_code_str, snpsrf_code_str):
        self.mra_code_str = mra_code_str
        self.snpsff_code_str = snpsff_code_str
        self.snpsrf_code_str = snpsrf_code_str

class AlleleMutCode:
    def __init__(self, *, codebook: AlleleMutCodeBook, allele: int, mrabase_mut_str: str, snpsff_mut_str:str, snpsrf_mut_str:str):

        self.mrabase_mut_str = mrabase_mut_str
        self.snpsff_mut_str = snpsff_mut_str
        self.snpsrf_mut_str = snpsrf_mut_str
        self.mrabase_mut_code = mut_code_from_str(mrabase_mut_str, codebook.mra_code_str)
        self.snpsff_mut_code = mut_code_from_str(snpsff_mut_str, codebook.snpsff_code_str)
        self.snpsrf_mut_code = mut_code_from_str(snpsrf_mut_str, codebook.snpsrf_code_str)
        self.allele_mut_code= create_allele_mut_code(allele, self.mrabase_mut_code, self.snpsff_mut_code, self.snpsrf_mut_code)

import copy
dfout = copy.copy(df)
dfout['allele_mut'] = ""
dfout = dfout.reset_index(drop=True)
mut_code_dict = {}

allele_mut_codebook = AlleleMutCodeBook(mra_code_str, snpsff_code_str, snpsrf_code_str)
for index, row in  df.iterrows():
    allele = row['Allele']
    mrabase_mut_str = row['MRABase']
    snpsff_mut_str = row['SnpsFF']
    snpsrf_mut_str = row['SnpsRF']
    allele_mut = AlleleMutCode(
        codebook = allele_mut_codebook, 
        allele = allele, 
        mrabase_mut_str = mrabase_mut_str, 
        snpsff_mut_str = snpsff_mut_str, 
        snpsrf_mut_str = snpsrf_mut_str
        )
    mut_code_dict[allele_mut.allele_mut_code] = allele_mut
    dfout.at[index, 'allele_mut'] = allele_mut.allele_mut_code

# Check dataframe - optional
# dfout.head()


# In[37]:


data_path = os.path.join(dir_path, 'data', 'output', 'FinalOutput.csv')
dfout = dfout.reset_index(drop=True)
dfout.to_csv(data_path)


# In[38]:


# Mutation Codes
# Output goes to "output" folder

# Create an output file MutationCodes.csv based on manipuation of the FinalOutput.csv file that for each Locus creates a list of Alleles and allele_muts and includes the following new columns
#  - counts the number of occurrences [num_occur] of that allele_mut and 
#  - sums all the NumReads [total_num_reads] for that allele_mut and
#  - reports the [MRAmut_code], [SnpsFF_code], and [SnpsRF_code] for each Allele at each Locus.
# 
# Final file should be sorted according to Locus and then allele_mut. 

in_path = os.path.join(dir_path, 'data', 'output', 'FinalOutput.csv')
out_path = os.path.join(dir_path, 'data', 'output', 'MutationCodes.csv')
dfin = pd.read_csv(in_path)

grps_sl = dfin.groupby('Locus')

df_list = []
for grp_sl_key, grp_sl_df in grps_sl:
    grps_am = grp_sl_df.groupby('allele_mut')
    for grp_am_key, grp_am_df in grps_am:
        if grp_am_key >= 0:
            # grab allele_mut object from dict we created earlier 
            allele_mut = mut_code_dict[grp_am_key]
            if allele_mut.mrabase_mut_code > 0:
                mrabase_mut_str = allele_mut.mrabase_mut_str
            else:
                mrabase_mut_str = ""
            if allele_mut.snpsff_mut_code > 0:
                snpsff_mut_str = allele_mut.snpsff_mut_str
            else:
                snpsff_mut_str = ""
            if allele_mut.snpsrf_mut_code > 0:
                snpsrf_mut_str = allele_mut.snpsrf_mut_str
            else:
                snpsrf_mut_str = ""

            data = {
                "Locus": grp_sl_key,
                "Microsatellite": grp_am_df["Microsatellite"].iloc[0],
                "MRABase": grp_am_df["MRABase"].iloc[0],
                "MRAName": grp_am_df["MRAName"].iloc[0],
                "MRASize": grp_am_df["MRASize"].iloc[0],
                "Allele": grp_am_df["Allele"].iloc[0],
                "allele_mut": grp_am_key,
                "num_occur": len(grp_am_df.index),
                "total_num_reads": grp_am_df["NumReads"].sum(),
                "MRAmut": mrabase_mut_str,
                "MRAmut_code": allele_mut.mrabase_mut_code,
                "SnpsFF": snpsff_mut_str,
                "SnpsFF_code": allele_mut.snpsff_mut_code,
                "SnpsRF": snpsrf_mut_str,
                "SnpsRF_code": allele_mut.snpsrf_mut_code,                
            }
            df_tmp = pd.DataFrame(data, index=[0])
            df_list.append(df_tmp)
            


dfout = pd.concat(df_list, ignore_index=True)


dfout = dfout.reset_index(drop=True)
dfout.to_csv(out_path)

# Check dataframe - optional
# dfout.head()


# In[42]:


# Create a file with One Row Per Individual Ouptut (for input into downstream pipelines)
# Ouput goest to "output" folder

# Create an additional output file based on the FinalOutput.csv that is reformatted to have one row per individual with Allele calls 
# and then one row per individual with allele_mut calls. All other data is removed.
# This ouput includes genotypes with alleles based on length (allele_len) and alleles based on legnth and mutations (allele_mut)
# The output can be easily manipulated in Excel to separate out the genotypes as necessary.

in_path = os.path.join(dir_path, 'data', 'output', 'FinalOutput.csv')
out_path = os.path.join(dir_path, 'data', 'output', 'allele_mut_onerowperind.csv')
dfin = pd.read_csv(in_path)
loci = dfin["Locus"].unique()
loci.sort()

grps_sample = dfin.groupby('Sample')
df_list = []
for grp_sample_key, grp_sample_df in grps_sample:
    row_len = {}
    row_mut = {}
    row_len['Sample'] = grp_sample_key + '_len'
    row_mut['Sample'] = grp_sample_key + '_mut'
    grps_locus = grp_sample_df.groupby('Locus')
    for grp_locus_key, grp_locus_df in grps_locus:
        assert len(grp_locus_df.index) == 2
        for k in range(len(grp_locus_df.index)):
            #print(f"{grp_locus_key} {k} {grp_locus_df['Allele'].iloc[k]}")
            #print(f"{grp_locus_key} {k} {grp_locus_df['allele_mut'].iloc[k]}")
            
            row_len[grp_locus_key + '_allele' + str(k+1)] = grp_locus_df['Allele'].iloc[k]
            row_mut[grp_locus_key + '_allele' + str(k+1)] = grp_locus_df['allele_mut'].iloc[k]

    df_len = pd.DataFrame(row_len, index=[0])
    df_mut = pd.DataFrame(row_mut, index=[0])
    df_list.append(df_len)
    df_list.append(df_mut)

dfout = pd.concat(df_list, ignore_index=True)

dfout = dfout.reset_index(drop=True)
dfout.to_csv(out_path)

# Check the dataframe - optional
# dfout.head()


# In[ ]:




