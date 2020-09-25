import sqlite3
import pandas as pd
import os
import seaborn as sns
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from itertools import combinations, permutations
import statsmodels.api as sm
from statsmodels.formula.api import ols
import os


def get_df_from_SQL(table_name, cur):
    cur.execute(f'select * from {table_name};')
    df = pd.DataFrame(cur.fetchall())
    df.columns = [i[0] for i in cur.description]
    return df

def get_table_names(conn):
    query = """
            select name from sqlite_master where type='table';
            """
    res = conn.execute(query).fetchall()
    table_names = [r[0] for r in res]
    return table_names

def get_table_column_names(conn, table_name):
    query = f"""
            pragma table_info({table_name})
            """
    res = conn.execute(query).fetchall()
    col_names = [r[1] for r in res]
    return col_names

def display_table_head(conn, table_name):
    query = f"""
            select * from {table_name}
            """
    df = pd.read_sql(query, conn)
    display(df.head(4))
    return

def detect_abnormality(lst_of_distributions):
    count = 0
    for i in lst_of_distributions:
        shapiro = stats.shapiro(i)
        if shapiro[1] < 0.05:
            print(f"The distribution at index {count} is not normally distributed")
        count += 1

def anova_test(formula, df):
    lm = ols(formula, df).fit()
    table = sm.stats.anova_lm(lm, typ=2)
    return table

def bootstrap_em(distribution, n=1000):
    means_list = []
    for i in range(n):
        means_list.append(np.random.choice(distribution, len(distribution), replace=True).mean())
    return means_list

def check_skew_kurtosis(sample):
    skew = scs.skew(sample)
    if np.abs(skew)<0.5:
        print ('The data are pretty symmetrical with skew={}'.format(skew))
    elif (np.abs(skew)>0.5 and np.abs(skew)<1):
        print ('The data are moderately skewed with skew={}'.format(skew))
    else:
        print ('The data are highly skewed with skew={}'.format(skew))
    kurtosis = scs.kurtosis(df_test['count'])
    if kurtosis<3:
        print ('Platykurtic: the distribution is shorter and tails are thinner with kurtosis={}'.format(kurtosis))
    elif kurtosis>3:
        print ('Leptokurtic: the distribution with longer and fatter tails with kurtosis={}'.format(kurtosis))
    else:
        print ('Mesokurtic: the diftribution is close to normal distribution')

def cohens_d(arr1, arr2):
    cohens_d = (np.mean(arr1) - np.mean(arr2)) / (np.sqrt((np.std(arr1) ** 2 + np.std(arr2) ** 2) / 2))
    return cohens_d

def welch_t(a, b):
    numerator = a.mean() - b.mean()
    denominator = np.sqrt((a.var(ddof=1)/a.size) +(b.var(ddof=1)/b.size))
  
    return np.abs(numerator/denominator)

def welch_df(a, b):
    s1 = a.var(ddof=1)
    s2 = b.var(ddof=1)
    N1 = a.size
    N2 = b.size
    
    numerator = (s1/N1 + s2/N2)**2
    
    denominator = ((s1/N1)**2)/(N1-1) + ((s2/N2)**2)/(N2-1)
    return numerator/denominator

def p_value(a, b, two_sided=False):
    t = welch_t(a, b)
    df = welch_df(a, b)
    p = 1 - stats.t.cdf(t,df)
    if two_sided:
        return p*2
    else:
        return p

