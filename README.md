# DarkWebAnalysis
REU project, summer 2019


### First code to run:
1. Data_Cleaning.ipynb
   - selects Dream market
   - applies timestamps
   - tokenizes titles, labels as the drug being sold
   - removes dates from 1969-1970, 2017, and the future
   - converts Bitcoin amount to USD
   - saves the dataframe as "drug_data"
2. Filtering_and_EDA_hmm.ipynb
   - removes "not_drugs"
   - gets listings with one category
   - summary statistics
   - filters low frequency drugs and vendors
   - vendor distribution
   - saves as "drug_df"
   - builds HMM test and train set
   - emission probability table
   - saves as "start_prob" and "trans_prob"
### Needed files:
1. product_rating_modified.txt
   - the dataset containing all product reviews
2. drugLookup.py
   - dictionary of drugs

### Other folders and files:
**ArtificialData** - files related to HMM and Bayes tests with artificial timestamps

**Drug Co-Occurence Data** - Indy overdose dataset, most common drug pairs

**OldCode** - outdated files of beginning processes and abandoned or moved code

**PriceAnalysis** - converting Bitcoin rate to USD

**Vendor Revenue** - pie chart of top vendors' revenue earned in the Dream market

**sqlfiles** - SQL of 2016 Dream market product and seller data
