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

# globals
seedValue = 1234
seed(seed=seedValue)
r = RandomState(seedValue)
random.seed(seedValue)

# Read command line args
parser = argparse.ArgumentParser(description='Generate account_role data for Lily demo environments.')
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

    file_out_accr =open(output_file("AccountRoleData.csv"), 'w')
    #file_out_accr.write('ID;ACCOUNT_ID;ROLE;START_DATE;END_DATE;\n')

    file_out_accrhd =open(output_file("AccountRoleData.hdr"), 'w')
    file_out_accrhd.write('CUSTOMER_ID;ACCOUNT_ID;ROLE\n')

    file_out_accr2 =open(output_file("AccountRoleDataAll.csv"), 'w')
    file_out_accr2.write('CUSTOMER_ID;ACCOUNT_ID;ROLE\n')

    idnr=0
    pb = Bar('Generating', max=len(entity_df), fill='=', suffix='%(percent)d%%')
    for id in range(1, len(entity_df) + 1):
        idnr= entity_df.ix[id-1,'ID']
        accountid= entity_df.ix[id-1,'ENTITY_ID']
        x=r.uniform(size=1)
        if x<=0.50:
           role='primary account holder'
        else :
           role='joint account holder'
        startdate= entity_df.ix[id-1,'START']
        enddate= entity_df.ix[id-1,'END']
        file_out_accr.write('%s;%s;%s\n' %(idnr,accountid,role))
        file_out_accr2.write('%s;%s;%s\n' %(idnr,accountid,role))


        pb.next()

if __name__ == "__main__":
    main()
