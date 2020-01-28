
import numpy as np
import scipy as sp
import pandas as pd

import scipy.special as special
import scipy.stats as stats
import matplotlib.pyplot as plt

def df_sample(df,column):

    return df[column].dropna().values

def gamma_fitting(sample,nbins,filename):

    xs = np.linspace(50,sample.max(),100)

    a_hat, loc_hat, scale_hat = stats.gamma.fit(sample)
    ps_hat = stats.gamma.pdf(xs,a_hat,loc=loc_hat,scale=scale_hat)

    plt.clf()
    fig = plt.figure(1,figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.plot(xs,ps_hat,lw=2,label='fitted')

    ax.hist(sample,density=True,histtype='stepfilled',alpha=0.2,bins=nbins)
    plt.savefig(filename)

    return (a_hat,loc_hat,scale_hat)

def chi2_fitting(sample,nbins,filename):

    xs = np.linspace(50,sample.max(),100)

    df_hat, loc_hat, scale_hat = stats.chi2.fit(sample)
    ps_hat = stats.chi2.pdf(xs,df_hat,loc=loc_hat,scale=scale_hat)

    plt.clf()
    fig = plt.figure(1,figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.plot(xs,ps_hat,lw=2,label='fitted')

    ax.hist(sample,density=True,histtype='stepfilled',alpha=0.2,bins=nbins)
    plt.savefig(filename)

    return (df_hat,loc_hat,scale_hat)

def make_sample_mean_set(df_hat,loc_hat,scale_hat,sample_size,set_size):

    lst = []
    for i in range(0,set_size):
        avg = stats.chi2.rvs(df=df_hat,loc=loc_hat,scale=scale_hat,size=sample_size)
        lst.append(avg)
    
    return np.array(lst)

