#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@topic: MultinomialHMM(baseline)
@author: junzhuang
@ref: 
    https://github.com/hmmlearn/hmmlearn
    https://cloud.tencent.com/developer/article/1179007
    https://blog.csdn.net/u011311291/article/details/78722262
@README:
    1. install hmmlearn by "pip install hmmlearn";
    2. dependent: numpy, hmmlearn, sklearn;
    3. parameters should match the format;
    4. observed dataset and sequence should be encoded;
    5. run: python hmm1.py
"""

import numpy as np
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder

class Hmm:
    def __init__(self, states, observations, ems_prob):
        """
        @ parameters:
            states (list): The sequence of hidden state.
            observations (list): The sequence of observations.
            ems_prob (matrix): Emission probability with size = len(states) x len(observations).
        """
        self.states = states
        self.observations = observations
        self.ems_prob = ems_prob

    def hmm_BaumWelch(self, data, n_iter=100, n_train=10):
        """
        @ parameters:
            data (matrix): The encoded observed sequence of hidden state
            n_iter (int): The iteration of hmm.MultinomialHMM.
            n_train (int): The number of trainings.
        @ return:
            start_prob (list): Start probability with size = 1 x len(states).
            trans_prob (matrix): Transition probability matrix with size = len(states) x len(states).
        """
        # Check the input format
        if len(data) < 2 or len(data[0]) < 1:
            return print("The input dataset should be 2D.")
        if len(self.states) < 1 or n_iter < 1 or n_train < 1:
            return print("Please input positive integer number for parameters.")
        # Initialize the parameters
        score0 = float("-inf")
        start_prob = 0
        trans_prob = 0
        # Build the model
        model = hmm.MultinomialHMM(n_components=len(self.states), n_iter=int(n_iter))
        # Run "n_train" times to train the model and select the best parameters.
        for _ in range(0, int(n_train)):
            model.fit(data)
            #print("Model fitted in round {0}!".format(_))
            # score: the larger, the better.
            scores = sum([model.score(data[i]) for i in range(len(data))]) 
            #print(scores)
            if scores > score0:
                start_prob = model.startprob_
                trans_prob = model.transmat_  
            score0 = max(score0, scores)
        return start_prob, trans_prob

    def hmm_Viterbi(self, obs_seq, start_prob, trans_prob, n_train=10, verbose=True):
        """
        @ parameters:
            obs_seq (list): An encoded observed sequence of hidden state.
            start_prob (list): Start probability with size = 1 x len(states).
            trans_prob (matrix): Transition probability matrix with size = len(states) x len(states).
            n_train (int): The training times.
            verbose (boolean): Print out the comment if True.
        @ return:
            vendor0 (list): Predicted sequence of hidden state.
        """
        # Check the input format
        if len(obs_seq) < 1:
            return print("The length of observed sequence should be larger than 1.")
        if len(self.states) < 1 or n_train < 1:
            return print("Please input positive integer number for parameters.")
        if len(self.states) != (len(trans_prob) or len(trans_prob[0])):
            return print("The size of trans_prob is not correct.")
        if len(start_prob) != len(trans_prob):
            return print("The size of start_prob and trans_prob doesn't match.")
        # Build the model and initialize the parameters
        model = hmm.MultinomialHMM(n_components=len(self.states))
        model.startprob_= start_prob
        model.transmat_ = trans_prob
        model.emissionprob_ = self.ems_prob
        logprob0 = float("-inf")
        vendor0 = 0
        # Run "n_train" times to train the model and select the best parameters.
        for _ in range(0, int(n_train)):
            # decode: Given parameters and observed sequence, employ Viterbi algorithm to predict the hidden state.
            # obs_seq must be list rather than array.
            logprob, vendors = model.decode(list(obs_seq), algorithm="viterbi") 
            if logprob > logprob0: # update "vendors" when logprob is larger than previous one.
                vendor0 = vendors
            logprob0 = max(logprob0, logprob)
        if verbose:
            print("The best logprob is: ", logprob0)
        return vendor0

    def seq_encoded(self, obs_seq):
        # Encode the observed sequence if necessary
        return LabelEncoder().fit_transform([self.observations.index(obs_seq[i]) \
                for i in range(len(obs_seq)) if obs_seq[i] in self.observations]) 

    def data_encoded(self, data_dseq):
        # Encode the observed dataset
        return [self.seq_encoded(self.observations, data_dseq[i]) \
                for i in range(len(data_dseq))]


if __name__ == '__main__':
    # Initialize the parameters and model
    states = ["vendor1", "vendor2", "vendor3", "vendor4", "vendor5"]
    observations = ["drug1", "drug2", "drug3"]
    ems_prob = np.array([[9.97860613e-01, 2.13881271e-03, 5.74009958e-07],
                         [4.41131862e-05, 9.99955887e-01, 4.05913054e-34],
                         [1.80783778e-01, 2.04285247e-01, 6.14930975e-01],
                         [7.72785012e-06, 9.99992272e-01, 4.43047659e-40],
                         [7.55409261e-14, 1.00000000e+00, 1.39151157e-53]])
    #states = vlist # totally 213 vendors
    #observations = dlist # totally 24 drugs

    hmm_ = Hmm(states, observations, ems_prob)

    data_dseq_ec = np.array([[0,1,0,2,1,2],
                             [0,2,1,1,0,2],
                             [0,0,1,1,2,1]]) # three drugs: 0,1,2
    obs_seq_ec = [2, 0, 1, 1, 2, 0]
    #data_dseq_ec = hmm_.data_encoded(data_dseq) # encode the observed dataset
    #data_dseq_ec = np.array(data_dseq_ec)
    #obs_seq = data_dseq[-1]
    #obs_seq_ec = hmm_.seq_encoded(obs_seq) # encode the observed sequence

    # Employ Baum-Welch algorithm to estimate the parameters
    start_prob, trans_prob = hmm_.hmm_BaumWelch(data_dseq_ec, n_iter=20, n_train=5)
    print("start probability ∏: \n", start_prob)
    print("transition probability A: \n", trans_prob)
    print("emission probability B: \n", ems_prob)

    # Employ Viterbi algorithm to estimate the parameters
    # https://stackoverflow.com/questions/34379911/how-to-run-hidden-markov-models-in-python-with-hmmlearn
    vendors = hmm_.hmm_Viterbi(obs_seq_ec, start_prob, trans_prob, n_train=10, verbose=True)
    obs_seq0 = obs_seq_ec
    #obs_seq0 = [observations.index(obs_seq[i]) for i in range(len(obs_seq)) if obs_seq[i] in observations]
    print("Drugs: \n", ", ".join(map(lambda x: observations[x], list(obs_seq0))))
    print("Vendors: \n", ", ".join(map(lambda x: states[x], vendors)))

"""
Result:

1. estimate the parameters:
start probability ∏: 
 [  7.40366857e-17   2.29729554e-10   7.50470461e-17   6.17480133e-08   9.99999938e-01]
transition probability A: 
 [[  1.69620596e-01   5.38395620e-14   8.30379404e-01   1.61564878e-15   9.23428411e-16]
 [  8.32545181e-01   5.28340187e-03   3.07870136e-05   1.88002574e-02   1.43340372e-01]
 [  2.07247856e-01   3.96936004e-14   7.92752144e-01   2.34605240e-16   7.71906844e-17]
 [  7.01823819e-01   7.78821772e-03   9.04328730e-06   2.97940815e-02   2.60584838e-01]
 [  2.56924341e-05   3.03331591e-01   1.96977582e-09   4.66841258e-01   2.29801457e-01]]
emission probability B: 
 [[  9.97860613e-01   2.13881271e-03   5.74009958e-07]
 [  4.41131862e-05   9.99955887e-01   4.05913054e-34]
 [  1.80783778e-01   2.04285247e-01   6.14930975e-01]
 [  7.72785012e-06   9.99992272e-01   4.43047659e-40]
 [  7.55409261e-14   1.00000000e+00   1.39151157e-53]]

2. prediction:
Drugs: drug3, drug1, drug2, drug2, drug3, drug1
Vendors: vendor 3, vendor 1, vendor 3, vendor 3, vendor 3, vendor 1
The best logprob is: -45.07970787404897
"""

"""
DeprecationWarning:
Function logsumexp is deprecated;
sklearn.utils.extmath.logsumexp was deprecated in version 0.19 and will be removed in 0.21.
Use scipy.misc.logsumexp instead.

solution:
    find out base.py from anaconda/pkgs/.../lib/hmmlearn/
    replace "from sklearn.utils.extmath import logsumexp"
    to "from scipy.misc import logsumexp"
"""
