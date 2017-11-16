#!/usr/bin/python
import json
import random
import argparse
from numpy.random import seed
from numpy.random import RandomState
import datetime
import pandas as pd
import radar
from progress.bar import Bar
import math

# globals
seedValue = 1234
seed(seed=seedValue)
r = RandomState(seedValue)
random.seed(seedValue)

# Read command line args
parser = argparse.ArgumentParser(description='Generate account data for Lily demo environments.')
parser.add_argument('-c','--customers', help='customer data file',required=False, default='.data/EntityDataAll.csv')
parser.add_argument('-o','--output', help='output folder',required=False, default='.data')
parser.add_argument('-m','--model', help='model file folder',required=False, default='data-generate-model')
args = parser.parse_args()

o_folder = args.output
m_folder = args.model
c_file = args.customers

# functions
def output_file(file_name):
    return o_folder + "/" + file_name

def model_file(file_name):
    return m_folder + "/" + file_name


# Import entity data
entity_df = pd.read_csv(c_file, sep=';')
#print list(entity_df.columns.values)
#print entity_df


def main():

    file_out_acc =open(output_file("AccountData.csv"), 'w')

    file_out_acchd =open(output_file("AccountData.hdr"), 'w')
    file_out_acchd.write('ACCOUNT_ID;CATEGORY;SUB_CATEGORY;BALANCE;ACTIVE\n')

    file_out_acc2 =open(output_file("AccountDataAll.csv"), 'w')
    file_out_acc2.write('ACCOUNT_ID;CATEGORY;SUB_CATEGORY;BALANCE;ACTIVE\n')

    idnr=0
    pb = Bar('Generating', max=len(entity_df), fill='=', suffix='%(percent)d%%')
    for id in range(1, len(entity_df) + 1):
        accountid= entity_df.ix[id-1,'ENTITY_ID']
        category= entity_df.ix[id-1,'PRODUCT']
        sub_category= entity_df.ix[id-1,'SUBTYPE']
        if sub_category != sub_category :
            sub_category=''
        if entity_df.ix[id-1,'VALUE'] != 0 :
            balance = entity_df.ix[id-1,'VALUE']
        else :
            balance = ''
        if balance != balance :
            balance=''
        active= entity_df.ix[id-1,'ACTIVE']

        file_out_acc.write('%s;%s;%s;%s;%s\n' %(accountid,category,sub_category,balance,active))
        file_out_acc2.write('%s;%s;%s;%s;%s\n' %(accountid,category,sub_category,balance,active))


        pb.next()

if __name__ == "__main__":
    main()
