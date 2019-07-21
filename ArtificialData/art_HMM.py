
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import compress

from datetime import datetime
from dateutil.parser import parse

import math
import os
import copy
import pickle

from itertools import groupby
from operator import itemgetter
from hmmlearn import hmm


# In[2]:


# Read in data (from pickle file)
import pickle
file = open('art_data.pkl','rb')
data = pickle.load(file)
file.close()

file = open('art_train.pkl','rb')
train = pickle.load(file)
file.close()

file = open('art_test.pkl','rb')
test = pickle.load(file)
file.close()


# ## Get subset of data for HMM

# In[3]:


# Number of train/test sequences to use
n_train = 270
n_test = 90
len_seq = 100 # length of each sequence

# Get subset of train/test set
v_train = np.array(train['vendor_name'][-n_train*len_seq:])
d_train = np.array(train['drug'][-n_train*len_seq:])
v_test = np.array(test['vendor_name'][:n_test*len_seq])
d_test = np.array(test['drug'][:n_test*len_seq])


# In[4]:


# Get probability for a variable given another variable
def get_cond_probDist(category, var, given_var):
#     Function gets probability distribution of 'var' given 'given_var' is 'category'
#     Args: 'category' is the class of given_var
#           'var' is the random variable for which the prob. dist. is computed
#           'given_var' is the random variable which is given
#     Returns: series, representing proportion of total for each drug
    subset = train[train[given_var] == category]
    tally = subset[given_var].groupby(subset[var]).count()
    return(tally/np.sum(tally))

# Create dictionary to predict using Bayes' Rule (i.e. using conditional probability)
def makeEmissionProbTable(var = 'drug', given_var = 'vendor_name'):
#     Function returns a dictionary with sorted probabilities for 'var' given 'given_var'
#     Args: 'var' is the name of the variable to predict
#           'given_var' is the name of the given variable
#     Returns: dictionary with keys for each possible outcome of 'given_var', and values corresponding to 
#                 sorted probabilities for each outcome of 'var'
    
    # Get list of unique vendors and of unique drugs
    cols = train[var].unique()
    rows = train[given_var].unique()

    #Create conditional probability dataframe
    cond_prob_df = pd.DataFrame(columns = cols)
    
    #Insert given variable name column
    cond_prob_df.insert(0, given_var, rows)
    
    # Apply function to dataframe
    cond_prob_df.iloc[:,1:] =         cond_prob_df[given_var].apply(get_cond_probDist, var = var, given_var = given_var)
    
    # fill NA values with 0
    cond_prob_df = cond_prob_df.fillna(0)
    
    # Set index to be given variable
    cond_prob_df = cond_prob_df.set_index(given_var)
  
    return(cond_prob_df)

# Create emission probability table
ems_prob_table = makeEmissionProbTable()
ems_prob = np.array(ems_prob_table, dtype=np.float) # convert to float
ems_prob.shape


# In[5]:


# Functions to encode and decode the sequences
def encode(seq, encoder):
    code = np.array([encoder[element] for element in seq])
    return code

def decode(code, codebook):
    seq = [codebook[element] for element in code]
    return seq

# Encode drugs for training
drug_categories = list(ems_prob_table)
drug_keys = range(0, len(drug_categories))
drug_encoder = dict(zip(drug_categories, drug_keys))
drug_codebook = dict(zip(drug_keys, drug_categories))
d_train_encoded = encode(d_train, drug_encoder)
d_test_encoded = encode(d_test, drug_encoder)

# Make vendor codebook (for evaluation)
vendor_list = list(ems_prob_table.index)
vendor_keys = range(0, len(vendor_list))
vendor_codebook = dict(zip(vendor_keys, vendor_list))


# In[6]:


# Reshape data for model
v_train = v_train.reshape((n_train,len_seq))
d_train_encoded = d_train_encoded.reshape((n_train,len_seq))
v_test = v_test.reshape((n_test,len_seq))
d_test_encoded = d_test_encoded.reshape((n_test,len_seq))


# ## Algorithms

# In[7]:


# 使用Baum-Welch算法来估计参数，然后使用Viterbi算法来预测隐状态数列。

def hmm_BaumWelch(data, n_states, n_iter=100, n_train=10):
    """
    @ parameters:
        data (matrix): The encoded observed sequence of hidden state
        n_states (int): The length of sequence for hidden state. 
        n_iter (int): The iteration of hmm.MultinomialHMM.
        n_train (int): The training times.
    @ return:
        start_prob (list): Start probability with size = 1 x n_states.
        trans_prob (matrix): Transition probability matrix with size = n_states x n_states.
    """
    # Check the input format
    if len(data) < 2 or len(data[0]) < 1:
        return print("The input dataset should be 2D.")
    if n_states < 1 or n_iter < 1 or n_train < 1:
        return print("Please input positive integer number for parameters.")
    # Initialize the parameters
    score0 = float("-inf")
    start_prob = 0
    trans_prob = 0
    # Build the model
    model = hmm.MultinomialHMM(n_components=n_states, n_iter=int(n_iter))
    # Run "n_train" times to train the model and select the best parameters.
    for _ in range(0, int(n_train)):
        model.fit(data) # 模型的拟合比较耗时
        print("Model fitted in round {0}!".format(_))
        # hmm2.0里的score函数接受2D作为输入格式
        scores = sum([model.score([data[i]]) for i in range(len(data))]) #score越大越好（若带负号，则绝对值越小越好）
        print(scores)
        if scores > score0:
            start_prob = model.startprob_
            trans_prob = model.transmat_  
            # 发射概率已知，这里无须估计。
        score0 = max(score0, scores)
    return start_prob, trans_prob

# https://stackoverflow.com/questions/34379911/how-to-run-hidden-markov-models-in-python-with-hmmlearn
def hmm_Viterbi(obs_seq, start_prob, trans_prob, ems_prob, n_states, n_train=10, verbose=True):
    """
    @ parameters:
        obs_seq (list): An encoded observed sequence of hidden state.
        start_prob (list): Start probability with size = 1 x n_states.
        trans_prob (matrix): Transition probability matrix with size = n_states x n_states.
        ems_prob (matrix): Emission probability with size = len(vlist) x len(dlist).
        n_states (int): The length of sequence for hidden state. 
        n_train (int): The training times.
        verbose (boolean): Print out the comment if True.
    @ return:
        vendor0 (list): Predicted sequence of hidden state.
    """
    # Check the input format
    if len(obs_seq) < 1:
        return print("The length of observed sequence should be larger than 1.")
    if n_states < 1 or n_train < 1:
        return print("Please input positive integer number for parameters.")
    if n_states != (len(trans_prob) or len(trans_prob[0])):
        return print("The size of trans_prob is not correct.")
    if len(start_prob) != len(trans_prob):
        return print("The size of start_prob and trans_prob doesn't match.")    
    # Build the model and initialize the parameters
    model = hmm.MultinomialHMM(n_components=n_states)
    model.startprob_= start_prob
    model.transmat_ = trans_prob
    model.emissionprob_ = ems_prob
    logprob0 = float("-inf")
    vendor0 = 0
    # Run "n_train" times to train the model and select the best parameters.
    for _ in range(0, int(n_train)):
        # decode: Given parameters and observed sequence, employ Viterbi algorithm to predict the hidden state.
        logprob, vendors = model.decode(list(obs_seq), algorithm="viterbi") # obs_seq must be list rather than array.
        if logprob > logprob0: # update "vendors" when logprob is larger than previous one.
            vendor0 = vendors
        logprob0 = max(logprob0, logprob)
    if verbose:
        print("The best logprob is: ", logprob0) #该参数反映模型拟合的好坏,数值越大越好。
    return vendor0

def evaluation(hs_seq_pred, hs_seq_gt, verbose=True):
    # 评价预测结果：Compute the accuracy
    if verbose:
        print("The set of predicted hidden state sequence: \n", set(hs_seq_pred))
        print("-"*90)
        print("The set of groundtruth hidden state sequence: \n", set(hs_seq_gt))
    cnt = 0
    for i in range(len(hs_seq_pred)):
        if hs_seq_pred[i] == hs_seq_gt[i]:
            cnt += 1
    return round(cnt/len(hs_seq_pred), 4)


# ## Apply Baum-Welch

# In[15]:


import time

data_dseq_ec = d_train_encoded

start_time = time.time()
# Employ Baum-Welch algorithm to estimate the parameters
start_prob, trans_prob = hmm_BaumWelch(d_train_encoded, len(vendor_list), n_iter=10, n_train=10)
end_time = time.time()
print('Training_time:',round(end_time-start_time,2),'seconds.')


# In[9]:


d_train_encoded.shape


# ## Save parameters to file

# In[10]:


import pickle
file = open('start_prob_art'+str(datetime.now()),'wb')
pickle.dump(start_prob, file)
file.close()

file = open('trans_prob_art'+str(datetime.now()),'wb')
pickle.dump(trans_prob, file)
file.close()

# ## Decode hidden sequence using Viterbi

# In[11]:


# 测试：预测和评价
def testing(test_obs, test_hs, idx, drug_codebook, vendor_codebook, verbose=True):
    obs_seq = test_obs[idx]
    obs_seq_ec = obs_seq.reshape(-1,1)

    # Employ Viterbi algorithm to estimate the parameters
    vendors = hmm_Viterbi(obs_seq_ec, start_prob, trans_prob, ems_prob, len(vendor_list), n_train=5, verbose = verbose)
    
    # Evaluation（对预测结果进行评价-accuracy）
    hs_seq_pred = [vendor_list[vendor_idx] for vendor_idx in vendors]
    hs_seq_gt = test_hs[idx]
    acc = evaluation(hs_seq_pred, hs_seq_gt, verbose=False)
    
    actual_drugs = decode(obs_seq, drug_codebook)
    actual_vendors = hs_seq_gt
    predicted_vendors = decode(vendors, vendor_codebook)
    
    df = pd.DataFrame({'drug':actual_drugs, 'actual_vendor': actual_vendors, 'predicted_vendor':predicted_vendors})
    df['correct'] = df['actual_vendor'] == df['predicted_vendor']

    return(df)

# Scenario3: select all samples from the testing set.
results = pd.concat([testing(d_test_encoded, v_test, idx, drug_codebook, vendor_codebook)                for idx in range(len(d_test_encoded))])


# ## Evaluate results

# In[12]:


print(len(results.actual_vendor.value_counts()))
print(len(results.predicted_vendor.value_counts()))

n_correct = results.correct.value_counts()[True]
n_wrong = results.correct.value_counts()[False]
accuracy = n_correct/(n_correct+n_wrong)
print('Accuracy:',round(100*accuracy,2),'%')

