#!/usr/bin/python
import json
import argparse
from progress.bar import Bar
from numpy.random import seed
from numpy.random import RandomState
from datetime import datetime, timedelta
import datetime as dt
import pandas as pd
import random
import radar
import arrow

# globals
seedValue = 1234
seed(seed=seedValue)
r = RandomState(seedValue)
random.seed(seedValue)

# Read command line args
parser = argparse.ArgumentParser(description='Generate customer ITX data for Lily demo environments.')
parser.add_argument('-n','--nrmonths', type=int, help='Number of months to generate interactions',required=False, default=6)
parser.add_argument('-o','--output', help='output folder',required=False, default='.data')
parser.add_argument('-m','--model', help='model file folder',required=False, default='data-generate-model')
parser.add_argument('-r','--refdate', help='reference date (YYYY-MM-DD) used to calculate the end data as the Sunday after', default=arrow.utcnow().format('YYYY-MM-DD'))
parser.add_argument('--progress', dest="progress", help='output progress bar', action='store_true')
parser.add_argument('--no-progress', dest="progress", help='do not output progress bar', action='store_false')
parser.set_defaults(progress=True)
args = parser.parse_args()

nr_months = args.nrmonths
o_folder = args.output
m_folder = args.model

refdate = args.refdate
progress = args.progress

# functions
def get_next_weekday(startdate, weekday):
    """
    @startdate: given date, in format '2013-05-25'
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    d = datetime.strptime(startdate, '%Y-%m-%d')
    t = timedelta((7 + weekday - d.weekday()) % 7)
    return (d + t).strftime('%Y-%m-%d')

def output_file(file_name):
    return o_folder + "/" + file_name

def output_file_min_max_ext(file_name, ext):
    return output_file(file_name + str(mindate) + "_" + str(maxdate) + "." + ext)

def load(file):
    with open(file) as data_file:
        return json.load(data_file)

def model_file(file_name):
    return m_folder + "/" + file_name

def load_profile(segnr, segments_data):
    return segments_data[segnr-1]

def pick_random_pct_min_max(array):
    random= r.uniform(size=1)

    for i in range(len(array)):
        if random > array[i]["pct_min"] and random <= array[i]["pct_max"]:
            return array[i]

def pick_goalcategories(n, segments_data):
    return pick_random_pct_min_max(segments_data["Goal_categories"])

def pick_subgoalcategories(n, goal):
    return pick_random_pct_min_max(goal["Subgoal_categories"])

def pick_channelcategories(n,subgoal):
    return pick_random_pct_min_max(subgoal["Channel_categories"])

def pick_itx_psp(i,segments_data):
    return r.randint(int(segments_data["NbrItx_FlagPSP"][0]),int(segments_data["NbrItx_FlagPSP"][1]))
#     return segments_data["NbrItx_FlagPSP"][0]

def pick_itx_nopsp(i,segments_data):
    return r.randint(segments_data["NbrItx_NoFlagPSP"][0],segments_data["NbrItx_NoFlagPSP"][1])

def pick_amount(n, subgoal):
    return int(subgoal["Amount"][0])

def pick_amountU(n, subgoal):
    return r.uniform(subgoal["Amount"][0],subgoal["Amount"][1])

def pick_amountDebitN(n, subgoal):
    return r.normal(subgoal["AmountDebit"][0],subgoal["AmountDebit"][1])

def pick_amountCreditN(n, subgoal):
    return r.normal(subgoal["AmountCredit"][0],subgoal["AmountCredit"][1])

def pick_amountDebitU(n, subgoal):
    return r.uniform(subgoal["AmountDebit"][0],subgoal["AmountDebit"][1])

def pick_amountCreditU(n, subgoal):
    return r.uniform(subgoal["AmountCredit"][0],subgoal["AmountCredit"][1])

def pick_paymentTypecategories(n,subgoal):
    return pick_random_pct_min_max(subgoal["Payment_categories"])

def pick_offerTypecategories(n,subgoal):
    return pick_random_pct_min_max(subgoal["Offer_categories"])

def pick_memocategories(n,subgoal):
    return pick_random_pct_min_max(subgoal["Memo_categories"])

def pick_accountTypes(n,subgoal):
    return pick_random_pct_min_max(subgoal["AccountTypes"])

#def addSecs(tm, secs):
#    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
#    fulldate = fulldate + datetime.timedelta(seconds=secs)
#    return fulldate.time()

# Import customer data
crm_df = pd.read_csv(output_file('CrmDataToFilter.csv'), sep=';')
#print list(crm_df.columns.values)
#print crm_df['id']

enddatex=get_next_weekday(refdate,6)
enddatex=arrow.get(enddatex)
startdate=enddatex.replace(months=-nr_months).format('YYYY-MM-DD')
startdatex=arrow.get(startdate)
startdateMinus2Month=enddatex.replace(months=-2).format('YYYY-MM-DD')
startdatexMinus2Month=arrow.get(startdateMinus2Month)
startdateMinus14Days=enddatex.replace(days=-14).format('YYYY-MM-DD')
startdatexMinus14Days=arrow.get(startdateMinus14Days)


mindate=dt.date(int(startdatex.year),int(startdatex.month),int(startdatex.day))
mindateMinus2Month=dt.date(int(startdatexMinus2Month.year),int(startdatexMinus2Month.month),int(startdatexMinus2Month.day))
mindateMinus14Days=dt.date(int(startdatexMinus14Days.year),int(startdatexMinus14Days.month),int(startdatexMinus14Days.day))
maxdate=dt.date(int(enddatex.year),int(enddatex.month),int(enddatex.day))

print "Interactions will span period: "
print "  start: " + str(mindate)
print "  end:   " + str(maxdate)

def main():
    print "Loading model files ..."
#    segments = load('segments.json')
    segment_itx_data = [
        load(model_file('segment_itx_1.json')),
        load(model_file('segment_itx_2.json')),
        load(model_file('segment_itx_3.json')),
        "",
        load(model_file('segment_itx_5.json')),
        load(model_file('segment_itx_6.json')),
        load(model_file('segment_itx_7.json'))
    ]
    print "... done"

    print "Opening output files and writing headers ..."
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#        => Standard Interactions cfr. itx.json - files

    file_out_itx_ca =open(output_file_min_max_ext("ItxData_CA_", "csv"), 'w')
    file_hdr_itx_ca =open(output_file_min_max_ext("ItxData_CA_", "hdr"), 'w')
    file_hdr_itx_ca.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ca_atm =open(output_file_min_max_ext("ItxData_CA_ATM_", "csv"), 'w')
    file_hdr_itx_ca_atm =open(output_file_min_max_ext("ItxData_CA_ATM_", "hdr"), 'w')
    file_hdr_itx_ca_atm.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ca_branch =open(output_file_min_max_ext("ItxData_CA_Branch_", "csv"), 'w')
    file_hdr_itx_ca_branch =open(output_file_min_max_ext("ItxData_CA_Branch_", "hdr"), 'w')
    file_hdr_itx_ca_branch.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ca_callcenter =open(output_file_min_max_ext("ItxData_CA_CallCenter_", "csv"), 'w')
    file_hdr_itx_ca_callcenter =open(output_file_min_max_ext("ItxData_CA_CallCenter_", "hdr"), 'w')
    file_hdr_itx_ca_callcenter.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ca_mobileapp =open(output_file_min_max_ext("ItxData_CA_MobileApp_", "csv"), 'w')
    file_hdr_itx_ca_mobileapp =open(output_file_min_max_ext("ItxData_CA_MobileApp_", "hdr"), 'w')
    file_hdr_itx_ca_mobileapp.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ca_web =open(output_file_min_max_ext("ItxData_CA_Web_", "csv"), 'w')
    file_hdr_itx_ca_web =open(output_file_min_max_ext("ItxData_CA_Web_", "hdr"), 'w')
    file_hdr_itx_ca_web.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_pu=open(output_file_min_max_ext("ItxData_PU_", "csv"), 'w')
    file_hdr_itx_pu=open(output_file_min_max_ext("ItxData_PU_", "hdr"), 'w')
    file_hdr_itx_pu.write('id;itxseq;date;time;goal;subgoal;paymentType;channel;amount\n')

    file_out_itx_pu_purch=open(output_file_min_max_ext("ItxData_PU_Purchases_", "csv"), 'w')
    file_hdr_itx_pu_purch=open(output_file_min_max_ext("ItxData_PU_Purchases_", "hdr"), 'w')
    file_hdr_itx_pu_purch.write('id;itxseq;date;time;goal;subgoal;paymentType;channel;amount\n')

    file_out_itx_cw=open(output_file_min_max_ext("ItxData_CW_", "csv"), 'w')
    file_hdr_itx_cw=open(output_file_min_max_ext("ItxData_CW_", "hdr"), 'w')
    file_hdr_itx_cw.write('id;itxseq;date;time;goal;subgoal;channel;paymentType;amount\n')

    file_out_itx_cw_atm=open(output_file_min_max_ext("ItxData_CW_ATM_", "csv"), 'w')
    file_hdr_itx_cw_atm=open(output_file_min_max_ext("ItxData_CW_ATM_", "hdr"), 'w')
    file_hdr_itx_cw_atm.write('id;itxseq;date;time;goal;subgoal;channel;paymentType;amount\n')

    file_out_itx_cw_branch=open(output_file_min_max_ext("ItxData_CW_Branch_", "csv"), 'w')
    file_hdr_itx_cw_branch=open(output_file_min_max_ext("ItxData_CW_Branch_", "hdr"), 'w')
    file_hdr_itx_cw_branch.write('id;itxseq;date;time;goal;subgoal;channel;paymentType;amount\n')

    file_out_itx_at=open(output_file_min_max_ext("ItxData_AT_", "csv"), 'w')
    file_hdr_itx_at=open(output_file_min_max_ext("ItxData_AT_", "hdr"), 'w')
    file_hdr_itx_at.write('id;itxseq;date;time;goal;subgoal;channel;amount;memo\n')

    file_out_itx_at_atm=open(output_file_min_max_ext("ItxData_AT_ATM_", "csv"), 'w')
    file_hdr_itx_at_atm=open(output_file_min_max_ext("ItxData_AT_ATM_", "hdr"), 'w')
    file_hdr_itx_at_atm.write('id;itxseq;date;time;goal;subgoal;channel;amount;memo\n')

    file_out_itx_at_branch=open(output_file_min_max_ext("ItxData_AT_Branch_", "csv"), 'w')
    file_hdr_itx_at_branch=open(output_file_min_max_ext("ItxData_AT_Branch_", "hdr"), 'w')
    file_hdr_itx_at_branch.write('id;itxseq;date;time;goal;subgoal;channel;amount;memo\n')

    file_out_itx_at_callcenter=open(output_file_min_max_ext("ItxData_AT_CallCenter_", "csv"), 'w')
    file_hdr_itx_at_callcenter=open(output_file_min_max_ext("ItxData_AT_CallCenter_", "hdr"), 'w')
    file_hdr_itx_at_callcenter.write('id;itxseq;date;time;goal;subgoal;channel;amount;memo\n')

    file_out_itx_at_mobileapp=open(output_file_min_max_ext("ItxData_AT_MobileApp_", "csv"), 'w')
    file_hdr_itx_at_mobileapp=open(output_file_min_max_ext("ItxData_AT_MobileApp_", "hdr"), 'w')
    file_hdr_itx_at_mobileapp.write('id;itxseq;date;time;goal;subgoal;channel;amount;memo\n')

    file_out_itx_at_web=open(output_file_min_max_ext("ItxData_AT_Web_", "csv"), 'w')
    file_hdr_itx_at_web=open(output_file_min_max_ext("ItxData_AT_Web_", "hdr"), 'w')
    file_hdr_itx_at_web.write('id;itxseq;date;time;goal;subgoal;channel;amount;memo\n')

    file_out_itx_pm=open(output_file_min_max_ext("ItxData_PM_", "csv"), 'w')
    file_hdr_itx_pm=open(output_file_min_max_ext("ItxData_PM_", "hdr"), 'w')
    file_hdr_itx_pm.write('id;itxseq;date;time;goal;subgoal;channel;amount;accountType\n')

    file_out_itx_pm_branch=open(output_file_min_max_ext("ItxData_PM_Branch_", "csv"), 'w')
    file_hdr_itx_pm_branch=open(output_file_min_max_ext("ItxData_PM_Branch_", "hdr"), 'w')
    file_hdr_itx_pm_branch.write('id;itxseq;date;time;goal;subgoal;channel;amount;accountType\n')

    file_out_itx_pm_callcenter=open(output_file_min_max_ext("ItxData_PM_CallCenter_", "csv"), 'w')
    file_hdr_itx_pm_callcenter=open(output_file_min_max_ext("ItxData_PM_CallCenter_", "hdr"), 'w')
    file_hdr_itx_pm_callcenter.write('id;itxseq;date;time;goal;subgoal;channel;amount;accountType\n')

    file_out_itx_pm_web=open(output_file_min_max_ext("ItxData_PM_Web_", "csv"), 'w')
    file_hdr_itx_pm_web=open(output_file_min_max_ext("ItxData_PM_Web_", "hdr"), 'w')
    file_hdr_itx_pm_web.write('id;itxseq;date;time;goal;subgoal;channel;amount;accountType\n')

    file_out_itx_ce=open(output_file_min_max_ext("ItxData_CE_", "csv"), 'w')
    file_out_hdr_ce=open(output_file_min_max_ext("ItxData_CE_", "hdr"), 'w')
    file_out_hdr_ce.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ce_branch =open(output_file_min_max_ext("ItxData_CE_Branch_", "csv"), 'w')
    file_hdr_itx_ce_branch =open(output_file_min_max_ext("ItxData_CE_Branch_", "hdr"), 'w')
    file_hdr_itx_ce_branch.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ce_callcenter =open(output_file_min_max_ext("ItxData_CE_CallCenter_", "csv"), 'w')
    file_hdr_itx_ce_callcenter =open(output_file_min_max_ext("ItxData_CE_CallCenter_", "hdr"), 'w')
    file_hdr_itx_ce_callcenter.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ce_email =open(output_file_min_max_ext("ItxData_CE_Email_", "csv"), 'w')
    file_hdr_itx_ce_email =open(output_file_min_max_ext("ItxData_CE_Email_", "hdr"), 'w')
    file_hdr_itx_ce_email.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ce_mobileapp =open(output_file_min_max_ext("ItxData_CE_MobileApp_", "csv"), 'w')
    file_hdr_itx_ce_mobileapp =open(output_file_min_max_ext("ItxData_CE_MobileApp_", "hdr"), 'w')
    file_hdr_itx_ce_mobileapp.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_ce_web =open(output_file_min_max_ext("ItxData_CE_Web_", "csv"), 'w')
    file_hdr_itx_ce_web =open(output_file_min_max_ext("ItxData_CE_Web_", "hdr"), 'w')
    file_hdr_itx_ce_web.write('id;itxseq;date;time;goal;subgoal;channel;amount\n')

    file_out_itx_of=open(output_file_min_max_ext("ItxData_OF_", "csv"), 'w')
    file_hdr_itx_of=open(output_file_min_max_ext("ItxData_OF_", "hdr"), 'w')
    file_hdr_itx_of.write('id;itxseq;date;time;goal;subgoal;channel;amount;offerType\n')

    file_out_itx_of_branch=open(output_file_min_max_ext("ItxData_OF_Branch_", "csv"), 'w')
    file_hdr_itx_of_branch=open(output_file_min_max_ext("ItxData_OF_Branch_", "hdr"), 'w')
    file_hdr_itx_of_branch.write('id;itxseq;date;time;goal;subgoal;channel;amount;offerType\n')

    file_out_itx_of_callcenter=open(output_file_min_max_ext("ItxData_OF_CallCenter_", "csv"), 'w')
    file_hdr_itx_of_callcenter=open(output_file_min_max_ext("ItxData_OF_CallCenter_", "hdr"), 'w')
    file_hdr_itx_of_callcenter.write('id;itxseq;date;time;goal;subgoal;channel;amount;offerType\n')

    file_out_itx_of_email=open(output_file_min_max_ext("ItxData_OF_Email_", "csv"), 'w')
    file_hdr_itx_of_email=open(output_file_min_max_ext("ItxData_OF_Email_", "hdr"), 'w')
    file_hdr_itx_of_email.write('id;itxseq;date;time;goal;subgoal;channel;amount;offerType\n')

    file_out_itx_of_mobileapp=open(output_file_min_max_ext("ItxData_OF_MobileApp_", "csv"), 'w')
    file_hdr_itx_of_mobileapp=open(output_file_min_max_ext("ItxData_OF_MobileApp_", "hdr"), 'w')
    file_hdr_itx_of_mobileapp.write('id;itxseq;date;time;goal;subgoal;channel;amount;offerType\n')

    file_out_itx_of_web=open(output_file_min_max_ext("ItxData_OF_Web_", "csv"), 'w')
    file_hdr_itx_of_web=open(output_file_min_max_ext("ItxData_OF_Web_", "hdr"), 'w')
    file_hdr_itx_of_web.write('id;itxseq;date;time;goal;subgoal;channel;amount;offerType\n')

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#       => Create Interactions for additional use cases

    file_out_itx_mobileapp=open(output_file_min_max_ext("ItxData_MobileApp_", "csv"), 'w')
    file_hdr_itx_mobileapp=open(output_file_min_max_ext("ItxData_MobileApp_", "hdr"), 'w')
    file_hdr_itx_mobileapp.write('id;date;time;goal;subgoal;channel\n')

    file_out_itx_carflow=open(output_file_min_max_ext("ItxData_CarFlow_", "csv"), 'w')
    file_hdr_itx_carflow=open(output_file_min_max_ext("ItxData_CarFlow_", "hdr"), 'w')
    file_hdr_itx_carflow.write('id;date;time;goal;subgoal;channel;currentPageId;simulationtype;simulationloanamount;simulationdownpayment;simulationmonthlypayment;simulationpaymentrate;simulationduration;simulationtradeinvalue;simulationcashrebate\n')

    file_out_itx_carloginweb=open(output_file_min_max_ext("ItxData_CarLoginWeb_", "csv"), 'w')
    file_hdr_itx_carloginweb=open(output_file_min_max_ext("ItxData_CarLoginWeb_", "hdr"), 'w')
    file_hdr_itx_carloginweb.write('id;date;time;goal;subgoal;channel\n')

    file_out_itx_carcontentweb=open(output_file_min_max_ext("ItxData_CarContentWeb_", "csv"), 'w')
    file_hdr_itx_carcontentweb=open(output_file_min_max_ext("ItxData_CarContentWeb_", "hdr"), 'w')
    file_hdr_itx_carcontentweb.write('id;date;time;goal;subgoal;channel;currentPageId\n')

    file_out_itx_carsimweb=open(output_file_min_max_ext("ItxData_CarSimWeb_", "csv"), 'w')
    file_hdr_itx_carsimweb=open(output_file_min_max_ext("ItxData_CarSimWeb_", "hdr"), 'w')
    file_hdr_itx_carsimweb.write('id;date;time;goal;subgoal;channel;simulationtype;simulationloanamount;simulationdownpayment;simulationmonthlypayment;simulationpaymentrate;simulationduration;simulationtradeinvalue;simulationcashrebate;currentpageid\n')

    file_out_itx_loc=open(output_file_min_max_ext("ItxData_Loc_", "csv"), 'w')
    file_hdr_itx_loc=open(output_file_min_max_ext("ItxData_Loc_", "hdr"), 'w')
    file_hdr_itx_loc.write('id;date;time;curentlocation;latitude;longitude\n')

    print "... done"

    if (progress):
        pb = Bar('Generating', max=len(crm_df), fill='=')
    else:
        print "Generating for %s customers" % (len(crm_df))

    for id in range(1, len(crm_df) + 1):
        segnr_crm = crm_df.ix[id-1,'segnr']
        profile_data=load_profile(segnr_crm,segment_itx_data)
        flagPFSP = crm_df.ix[id-1,'flagPFSP']

# Create Interactions based on itx-profile
        if flagPFSP == 1 :
            nbritx=pick_itx_psp(id-1,profile_data)
        else :
            nbritx=pick_itx_nopsp(id-1,profile_data)

        #print id,segnr_crm,nbritx
        nbritx=nbritx*10
# *************************************************************************************************************************************************************************************
#       Create Interactions for additional use cases
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#        => Mobile App use case
        hasMobileApp = crm_df.ix[id-1,'hasMobileApp']
        regMobileApp = crm_df.ix[id-1,'regMobileApp']
        if hasMobileApp==1 :
            downloadDateMobileApp=radar.random_datetime(mindateMinus2Month,maxdate)
            time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
            goal="Install App"
            subgoal="View offer landing page"
            channel="Mobile"
            file_out_itx_mobileapp.write('%s;%s;%s;%s;%s;%s\n' %(id,downloadDateMobileApp,time,goal,subgoal,channel))
            if regMobileApp==1 :
                regDateMobileApp=radar.random_datetime(downloadDateMobileApp,maxdate)
                time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                goal="Create profile"
                subgoal="Create new profile via mobile app"
                channel="Mobile"
                file_out_itx_mobileapp.write('%s;%s;%s;%s;%s;%s\n' %(id,regDateMobileApp,time,goal,subgoal,channel))

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#        => Car Loan Page vists
        if id in (11703,33957,24538,18155,49896,10184,47059,24957,18317,1294,32960,47329,10049,20502,19196,36313,30874,29797,3592,32143,21815,48466,20364,16725,47888,11356,17292,46740,22459,
                 33004,4544,32945,1761,8876,19092,31204,784,36719,16451,5356,6011,42194,47187,16130,38111,1832,21882,19802,11775,42125,11516,34010,2820,49850,9266,47163,1658,13755,31796,
                 32515,20567,2868,12474,41390,12175,16384,41711,16940,47028,19378,10318,43429,23207,11512,24763,40858,21205,16910,3565,28428,9982,47734,39141,22413,22790,43009,4447,14388,322,
                 9943,34911,36368,19447,22620,19022,3355,32985,12098,23358,44145,47174,16985,11857,21750,7837,41545,6740,2221,27070,41486,23758,5284,39963,30665,43844,15158,36959,28582,35759,
                 17414,37005,6921,49001,31492,15674,10932,13777,3778,48145,20135,23964,28752,26438,25658,5668,25199,12758,47764,2658,14225,11865,1089,17201,3438,18750,706,44547,49102,40276,
                 2266,11486,9758,48360,45669,17138,49345,3291,16124,17674,45308,31441,8861,37831,6283,32213,9379,4680,45342,29306,12778,23861,14254,839,11535,37137,3309,42251,30260,11725,
                 28295,16928,29165,15746,14924,7454,11836,42211,22676,19438,35442,9203,11891,35404,42026,18002,4106,423,3544,49126,38098,45736,2002,28093,42729,3019,18343,35618,9436,15326,
                 45448,1293,23193,3921,43749,34791,9726,26140,10548,13224,9499,32254,14452,9788,3143,37733,48530,1466,24251,20718,499,20407,29850,20161,5979,33006,49394,25383,12696,43810,
                 40268,32932,19131,39306,13842,13352,44469,6551,29001,46586,1379,2142,25378,33903,49820,10331,23603,41829,18679,38294,36619,47838,29329,12303,19008,9239,19588,16767,6684,24529,
                 10218,449,43403,23408,19598,30395,18771,16954,45954,42849,31002,16113,39765,45197,16952,18538,8937,46986,3408,43700,40555,21880,3362,46618,6732,13674,1819,4131,21861,35420,
                 42068,10589,27360,22535,7410,38610,8484,13834,31251,6090,22380,42526,7485,23750,45397,5708,48453,43051,29796,8346,3395,18332,30426,20330,32677,49934,7138,33477,36097,48632,
                 40649,15391,14491,6203,5331,37926,23117,12182,13862,24555,14989,13136,46557,43260,592,25168,3694,6415,8970,19023,4107,17378,39788,26884,38556,38792,3064,26103,15913,28437,
                 31491,8459,27121,9479,33845,42909,26743,42648,509,8989,19772,30731,11062,19554,40027,48598,21825,12892,6361,7754,39192,5058,38072,25718,20185,19631,27663,5054,9281,20820,
                 29923,1065,8925,33912,1540,37375,44305,22759,23730,43399,44644,41548,47930,12415,7292,31427,23057,9891,46489,26831,4514,22750,29662,12870,49767,8428,34916,33526,48057,43305,
                 2025,47181,41282,2860,29859,16395,35279,29848,48416,21747,44657,34140,39900,29915,7804,5955,30526,28718,39239,42751,24809,23089,22150,31916,19976,1269,5026,46150,40122,3304,
                 35878,4412,29761,16896,18066,5843,39436,43043,24816,6613,4289,13636,35090,16334,24760,3488,2467,2380,36325,1642,38361,38038,32701,37327,16414,32919,19017,28377,2445,39522,
                 13987,1906,11707,45160,8534,43970,36494,48600,36479,2234,38166,47768,27217,47333,44617,23264,400,20134,32490,42318,43632,75,41326,11187,21454,31068,595,47032,22348,47565,
                 29803,6801,16746,27728,44099,35964,16664,40589,101,21520,49476,4169,37900,36319,47679,42154,40746,46142,49771,12489,34378,34984,30542,6012,45369,46870,39040,4490,42326,11440,
                 15666,18889,27237,34370,32184,41891,24788,7222,38483,11097,43959,41273,11152,10956,19634,28290,1126,40585,37373,40498,45639,46461,32769,3344,14533,35590,19192,18973,45267,9577,
                 42576,5975,49544,4033,43400,45374,11603,8240,20317,36433,5371,24170,27569,7515,5983,42515,39802,2641,41404,37157,18595,42302,3003,26879,42426,33595,26271,35794,4875,45176,
                 20655,18753,11953,39931,22961,45454,48824,20866,34621,37986,32557,36602,44165,36554,629,25297,44342,34111,13178,26089,40067,31218,27024,46046,2539,24985,33318,36597,47203,43919,
                 18814,23034,27563,17377,17151,44218,12799,607,34584,1501,36081,19452,41761,6879,37923,42645,37196,36501,43224,41554,19389,42518,23280,1219,26448,28200,29993,2836,18276,17320,
                 6908,25996,6923,23421,11800,17011,26218,49250,31593,11726,3081,12177,37812,34048,7080,32782,21198,26944,41811,32524,9069,32654,18959,40768,13728,30383,17635,29197,9853,28811,
                 44543,8317,12934,19946,24897,27160,23179,12883,19627,38237,24512,22721,38085,47575,1015,7872,19535,41747,9133,23944,10174,2265,37630,13942,15504,30332,15886,27488,32284,44564,
                 49675,35739,47076,47414,19282,30885,22356,34592,46903,25798,42871,12906,42973,44443,43485,11227,10263,15316,10929,45402,24604,1912,31706,41653,22122,39922,38889,29965,36915,29536,
                 5945,35539,12842,6141,6272,43673,16724,10479,7616,15481,23336,49704,33868,33046,39135,2904,19408,38193,6381,3591,24409,33723,20285,30951,10339,39315,38788,26286,37079,6360,
                 39075,12938,17832,37056,33569,18093,46446,22211,1115,45207,42512,25563,721,40420,20699,33397,9209,1499,35272,37857,5641,39679,967,40367,42759,43031,19252,5890,12480,33599,
                 22926,3764,49353,10541,26975,1251,29972,16085,20056,38378,43163,37472,25441,22014,5472,39709,10515,28363,41748,16722,14122,10232,42873,32427,47286,6379,47827,48099,29956,28629,
                 9892,35783,3043,25263,25047,4781,34068,40191,48719,36739,47369,24414,43064,12591,24342,42900,8223,32743,30058,41681,8526,27071,20895,9812,9568,29488,1189,49678,16748,8958,
                 7941,35461,22783,19194,21063,21694,12675,37156,13949,39567,7291,23493,25852,13918,21255,46240,29203,30094,29491,15799,45618,9368,26443,29639,23898,3282,47804,2916,29415,30042,
                 28105,20429,6238,48123,3480,11872,11149,9997,40677,26425,5638,35425,42733,24387,25076,10962,23135,3363,28096,24236,49622,6554,18114,21041,18522,4327,31946,42502,12063,11281,
                 21530,4989,13908,34972,37158,31693,17846,39506,4271,19633,41374,45946,26992,6956,6672,11965,4435,20914,22478,45298,6290,5995,42649,36130,18580,19864,32639,42310,27631,46797,
                 29852,30634,44778,19923,47371,24846,35333,19619,8946,43297,12560,12424,31822,23240,40461,9223,2937,44217,7713,39832,46101,43722,11174,736,38563,19345,32984,5984,20585,19137,
                 25889,41024,31238,1427,5119,27206,1129,27103,17661,48347,24571,17821,16624,27049,19019,45259,19650,23660,44160,45382,22085,12276,12039,39064,5615,22595,10823,21689,33534,27085,
                 22463,14190,26477,9744,6566,29539,17592,708,43799,27883,11129,1973,27276,17412,13547,8128,21426,39872,12852,22649,1213,24616,31085,12396,30659,39739,30558,18867,10551,25430,
                 39529,15889,32613,1048,29042,47291,22986,29225,12224,1500,42434,2557,573,26478,41245,17317,7255,10447,29495,42228,5776,17152,2268,44245,4760,48215,16999,608,46608,6641,
                 25456,21368,8974,21740,7270,33774,43021,35414,49914,30761,35032,44697,38141,33808,33570,29602,9158,12895,22741,13246,27538,10370,9495,25164,32406,20275,42558,21691,22045,20654,
                 25432,22339,17709,45070,42763,38323,13798,28112,6695,34806,40891,8020,39663,13695,17330,38469,7880,37925,46832,32355,27715,28448,28748,12933,36775,6315,18069,48247,13772,6998,
                 29156,38639,7899,31536,13826,28747,23362,11183,35749,21355,5574,26339,49116,20132,4223,41861,8369,6356,19990,4716,24993,7276,26638,19854,44756,39795,26025,48993,49186,30979,
                 13970,20966,8843,10818,11190,12406,2948,46463,7126,13374,32998,26381,22866,27414,35322,10950,33362,14152,3334,41731,25953,19994,15820,53,38058,44380,10104,42190,4136,20818,
                 41621,23978,41328,28665,29105,23778,13936,6174,6581,26875,46960,1623,8348,3899,9951,3649,10310,2157,25801,30461,42110,28396,32037,1329,40444,39389,18852,4303,28414,18517,
                 32087,1910,33225,28071,1473,26276,11075,26670,39962,14286,19669,28195,3348,34383,19573,30115,3281,43806,7613,9646,35009,48187,12361,9903,35074,16389,14097,11457,49193,15732,
                 2657,33474,42311,47142,27269,15597,24552,24811,40618,22180,41570,23104,43629,39125,22328,20393,9581,3240,12760,28846,3464,44389,15781,36084,22473,45486,37919,42119,45780,23705,
                 36149,44307,48316,33421,20234,7135,19383,41110,33987,9444,35848,47544,3132,21498,38618,32153,47742,23969,3538,48431,3517,30375,2242,10594,29789,45285,25844,17360,10439,31959,
                 24280,27110,4998,399,48635,17019,37696,20768,11674,15877,9098,36153,37269,43321,42907,39433,22280,48790,36128,7975,19176,2740,5887,10591,20644,39625,38444,11880,19391,3372,
                 1227,27363,20865,2283,27531,16027,2391,21103,20426,8677,22208,18550,21592,37504,30960,39222,1088,36567,16918,29686,14118,12319,17921,22847,46509,4359,25817,32310,28031,27371,
                 16363,23467,6962,48424,29241,39456,36794,32270,45937,19603,13830,10253,24422,26761,11160,14900,33643,46592,29370,326,1850,8217,4675,27102,19592,43323,11258,4364,35153,12292,
                 4861,22732,39263,49570,26501,7945,17321,23733,1296,32269,5319,15571,1005,16286,40647,7166,24442,33491,9183,14860,47332,27066,9704,19697,21189,13020,49872,10656,32981,22668,
                 14028,30534,33770,33173,36806,2058,42112,18113,31447,42134,28502,10011,23128,15066,15855,8230,38501,16743,36561,23111,21085,13599,7306,17028,5678,25615,9545,9819,44009,5854,
                 26615,17208,44415,30473,18705,27193,37308,20537,29013,9705,1953,17067,23735,47629,14583,12291,49802,39363,38850,5852,18459,2103,22552,15924,15789,6395,33843,1731,31292,11901,
                 20242,26249,42000,36741,38067,25843,12229,21501,42887,48246,18928,36664,45503,43971,982,24730,36254,5019,25652,35296,33023,49976,49450,10088,34632,15988,8879,13472,373,33081,
                 45274,26285,22667,11963,47707,23383,5888,5092,3391,45796,14267,27433,36985,19291,42065,26200,4557,39074,14329,3289,15557,29072,36210,12520,5689,39372,30248,40501,13613,22362,
                 40727,49427,19950,24180,14801,3920,6480,40407,14681,7980,4228,28435,22881,41420,3700,47422,18120,13664,31814):
            t1=r.randint(1,100)
            t2=r.randint(1,100)

            if t1<=90 :
                date=radar.random_datetime(mindateMinus14Days,maxdate)
                time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,55))
                goal="request information"
                subgoal="run login"
                channel="web"
                file_out_itx_carloginweb.write('%s;%s;%s;%s;%s;%s\n' %(id,date,time,goal,subgoal,channel))
           
                goal1="consume content"
                subgoal1="consume general content"
                currentpageid="simulation"
                file_out_itx_carcontentweb.write('%s;%s;%s;%s;%s;%s;%s\n' %(id,date,time,goal1,subgoal1,channel,currentpageid))
        
                if t2<=70 :
                    date=date
                    time=time
                    goal="request information"
                    subgoal="run simulation"
                    channel="web"
                    simulationtype="car loan"
                    simulationloanamount=r.randint(40000,80000)
                    simulationdownpayment=r.randint(400,800)
                    simulationmonthlypayment=r.randint(400,800)
                    simulationpaymentrate=r.randint(2,5)
                    simulationduration=r.randint(40,60)
                    simulationtradeinvalue="3000"
                    simulationcashrebate="0"
                    currentpageid="simulation"


                    file_out_itx_carsimweb.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,date,time,goal,subgoal,channel,simulationtype
                          ,simulationloanamount
                          ,simulationdownpayment
                          ,simulationmonthlypayment
                          ,simulationpaymentrate
                          ,simulationduration
                          ,simulationtradeinvalue
                          ,simulationcashrebate
                          ,currentpageid))

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#        => Location Itx
        locationTracking = crm_df.ix[id-1,'currentLocationTracking']
        if locationTracking==1 :
            for i in range(0,13) :
                actualdate=mindateMinus14Days + timedelta(days=i)
                time=dt.time(r.randint(0,23),r.randint(0,59),r.randint(0,59))
                z1=r.randint(1,100)
#switch location of Krista Johnson between New York and Boston
                if id == 3346 and z1>33.32:
                    z1=10
#switch location of Desmond Thomas between New York and Boston
                if id == 22639  and z1>33.32:
                    z1=30

                if z1<=16.66 :
                    currentLocation="New York"
                    latitude=40.7143528
                    longitude=-74.0059731
                    file_out_itx_loc.write('%s;%s;%s;%s;%s;%s\n' %(id,actualdate,time,currentLocation,latitude,longitude))
                elif z1<=33.32 :
                    currentLocation="Boston"
                    latitude=42.35854392
                    longitude=-71.04309082
                    file_out_itx_loc.write('%s;%s;%s;%s;%s;%s\n' %(id,actualdate,time,currentLocation,latitude,longitude))
                elif z1<=49.98 :
                    currentLocation="Washington"
                    latitude=38.9072
                    longitude=-77.0369
                    file_out_itx_loc.write('%s;%s;%s;%s;%s;%s\n' %(id,actualdate,time,currentLocation,latitude,longitude))
                elif z1<=66.64 :
                    currentLocation="Los Angeles"
                    latitude=34.0522
                    longitude=-118.2437
                    file_out_itx_loc.write('%s;%s;%s;%s;%s;%s\n' %(id,actualdate,time,currentLocation,latitude,longitude))
                elif z1<=83.3 :
                    currentLocation="Chicago"
                    latitude=41.8781
                    longitude=-87.6298
                    file_out_itx_loc.write('%s;%s;%s;%s;%s;%s\n' %(id,actualdate,time,currentLocation,latitude,longitude))
                else:
                    currentLocation="San Francisco"
                    latitude=37.7749
                    longitude=-122.4194
                    file_out_itx_loc.write('%s;%s;%s;%s;%s;%s\n' %(id,actualdate,time,currentLocation,latitude,longitude))
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#        => Standard Interactions cfr. itx.json - files
        for j in range(0,nbritx) :
            goal=pick_goalcategories(j,profile_data)

            if goal["name"]=="consult account" and crm_df.ix[id-1,'totalActiveProducts']> 0 :
#                nbrITX_CA=nbrITX_CA+1
                subgoal=pick_subgoalcategories(j,goal)
                channel=pick_channelcategories(j,subgoal)
                if channel["name"]=="Mobile App" and regMobileApp==0 :
                    channel["name"]="Web"
                date=radar.random_datetime(mindate,maxdate)
                time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                amount=pick_amount(j,subgoal)
                file_out_itx_ca.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="ATM":
                    file_out_itx_ca_atm.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Branch":
                    file_out_itx_ca_branch.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Call Center":
                    file_out_itx_ca_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Mobile App":
                    date=radar.random_datetime(regDateMobileApp,maxdate)
                    file_out_itx_ca_mobileapp.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Web":
                    file_out_itx_ca_web.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))

            elif goal["name"]=="make purchase" and crm_df.ix[id-1,'flagCheckingsAccount']==1 and crm_df.ix[id-1,'flagCreditCard']==1:
#                nbrITX_PU=nbrITX_PU+1
                subgoal=pick_subgoalcategories(j,goal)
                channel=pick_channelcategories(j,subgoal)
                if channel["name"]=="Mobile App" and regMobileApp==0 :
                    channel["name"]="Web"
                date=radar.random_datetime(mindate,maxdate)
                time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                paymentType=pick_paymentTypecategories(j,subgoal)
                if paymentType["name"]=="credit":
                    amount=pick_amountCreditN(j,subgoal)
                else:
                    amount=pick_amountDebitN(j,subgoal)
                file_out_itx_pu.write('%s;%s;%s;%s;%s;%s;%s;%s;%5.2f\n' %(id,j,date,time,goal["name"],subgoal["name"],paymentType["name"],channel["name"],amount))
                file_out_itx_pu_purch.write('%s;%s;%s;%s;%s;%s;%s;%s;%5.2f\n' %(id,j,date,time,goal["name"],subgoal["name"],paymentType["name"],channel["name"],amount))
            elif goal["name"]=="manage personal finances" and crm_df.ix[id-1,'flagCheckingsAccount']==1 and crm_df.ix[id-1,'flagCreditCard']==1:
#                nbrITX_CW=nbrITX_CW+1
                subgoal=pick_subgoalcategories(j,goal)
                channel=pick_channelcategories(j,subgoal)
                if channel["name"]=="Mobile App" and regMobileApp==0 :
                    channel["name"]="Web"
                if subgoal["name"]=="withdraw cash":
                    paymentType=pick_paymentTypecategories(j,subgoal)
                    if paymentType["name"]=="credit":
                        amount=pick_amountCreditU(j,subgoal)*10
                    else:
                        amount=pick_amountDebitU(j,subgoal)*10
                    file_out_itx_cw.write('%s;%s;%s;%s;%s;%s;%s;%s;%6.2f\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],paymentType["name"],amount))
                if channel["name"]=="ATM":
                    file_out_itx_cw_atm.write('%s;%s;%s;%s;%s;%s;%s;%s;%6.2f\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],paymentType["name"],amount))
                if channel["name"]=="Branch":
                    file_out_itx_cw_branch.write('%s;%s;%s;%s;%s;%s;%s;%s;%6.2f\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],paymentType["name"],amount))

            elif goal["name"]=="process offer" :
#                nbrITX_OF=nbrITX_OF+1
                subgoal=pick_subgoalcategories(j,goal)
                channel=pick_channelcategories(j,subgoal)
                if channel["name"]=="Mobile App" and regMobileApp==0 :
                    channel["name"]="Web"
                date=radar.random_datetime(mindate,maxdate)
                time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                offerType=pick_offerTypecategories(j,subgoal)
                amount=pick_amount(j,subgoal)
                file_out_itx_of.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,offerType["name"]))
                if channel["name"]=="Branch":
                    file_out_itx_of_branch.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,offerType["name"]))
                if channel["name"]=="Call Center":
                    file_out_itx_of_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,offerType["name"]))
                if channel["name"]=="Email":
                    file_out_itx_of_email.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,offerType["name"]))
                if channel["name"]=="Mobile App":
                    date=radar.random_datetime(regDateMobileApp,maxdate)
                    file_out_itx_of_mobileapp.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,offerType["name"]))
                if channel["name"]=="Web":
                    file_out_itx_of_web.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,offerType["name"]))


            elif goal["name"]=="execute payment transaction" and crm_df.ix[id-1,'flagCheckingsAccount']==1 and crm_df.ix[id-1,'flagSavingsAccount']==1:
#                nbrITX_AT=nbrITX_AT+1
                subgoal=pick_subgoalcategories(j,goal)
                channel=pick_channelcategories(j,subgoal)
                if channel["name"]=="Mobile App" and regMobileApp==0 :
                    channel["name"]="Web"
                date=radar.random_datetime(mindate,maxdate)
                time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                amount=pick_amountU(j,subgoal)*crm_df.ix[id-1,'monthlyIncome']
                file_out_itx_at.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                if channel["name"]=="ATM":
                    file_out_itx_at_atm.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                if channel["name"]=="Branch":
                    file_out_itx_at_branch.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                if channel["name"]=="Call Center":
                    file_out_itx_at_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                if channel["name"]=="Mobile App":
                    date=radar.random_datetime(regDateMobileApp,maxdate)
                    file_out_itx_at_mobileapp.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                if channel["name"]=="Web":
                    file_out_itx_at_web.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))

            elif goal["name"]=="manage personal finances" and crm_df.ix[id-1,'flagCheckingsAccount']==1 and crm_df.ix[id-1,'flagSavingsAccount']==1:
#                nbrITX_AT=nbrITX_AT+1
                subgoal=pick_subgoalcategories(j,goal)
                channel=pick_channelcategories(j,subgoal)
                if subgoal["name"]=="make deposit":
                    if channel["name"]=="Mobile App" and regMobileApp==0 :
                        channel["name"]="Web"
                    date=radar.random_datetime(mindate,maxdate)
                    time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                    amount=pick_amountU(j,subgoal)*crm_df.ix[id-1,'monthlyIncome']
                    memo=pick_memocategories(j,subgoal)
                    file_out_itx_at.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,memo["name"]))
                    if channel["name"]=="ATM":
                        file_out_itx_at_atm.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,memo["name"]))
                    if channel["name"]=="Branch":
                        file_out_itx_at_branch.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,memo["name"]))
                    if channel["name"]=="Call Center":
                        file_out_itx_at_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,memo["name"]))
                    if channel["name"]=="Mobile App":
                        date=radar.random_datetime(regDateMobileApp,maxdate)
                        file_out_itx_at_mobileapp.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,memo["name"]))
                    if channel["name"]=="Web":
                        file_out_itx_at_web.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,memo["name"]))


                elif subgoal["name"]=="account transfer":
                    channel=pick_channelcategories(j,subgoal)
                    if channel["name"]=="Mobile App" and regMobileApp==0 :
                        channel["name"]="Web"
                    date=radar.random_datetime(mindate,maxdate)
                    time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                    amount=pick_amountU(j,subgoal)*crm_df.ix[id-1,'monthlyIncome']
                    file_out_itx_at.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                    if channel["name"]=="ATM":
                        file_out_itx_at_atm.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                    if channel["name"]=="Branch":
                        file_out_itx_at_branch.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                    if channel["name"]=="Call Center":
                        file_out_itx_at_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                    if channel["name"]=="Mobile App":
                        date=radar.random_datetime(regDateMobileApp,maxdate)
                        file_out_itx_at_mobileapp.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))
                    if channel["name"]=="Web":
                        file_out_itx_at_web.write('%s;%s;%s;%s;%s;%s;%s;%8.2f;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,""))

            elif goal["name"]=="manage product portfolio" and crm_df.ix[id-1,'totalActiveProducts']> 0:
#                nbrITX_PM=nbrITX_PM+1
                subgoal=pick_subgoalcategories(j,goal)
                if subgoal["name"]=="close an existing account" or subgoal["name"]=="open a new account" :
                    channel=pick_channelcategories(j,subgoal)
                    if channel["name"]=="Mobile App" and regMobileApp==0 :
                        channel["name"]="Web"
                    date=radar.random_datetime(mindate,maxdate)
                    time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                    amount=pick_amount(j,subgoal)
                    accountType=pick_accountTypes(j,subgoal)
                    file_out_itx_pm.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))
                    if channel["name"]=="Branch":
                        file_out_itx_pm_branch.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))
                    if channel["name"]=="Call Center":
                        file_out_itx_pm_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))
                    if channel["name"]=="Web":
                        file_out_itx_pm_web.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))
                else :
                    channel=pick_channelcategories(j,subgoal)
                    if channel["name"]=="Mobile App" and regMobileApp==0 :
                        channel["name"]="Web"
                    date=radar.random_datetime(mindate,maxdate)
                    time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                    amount=pick_amount(j,subgoal)
                    accountType=pick_accountTypes(j,subgoal)
                    file_out_itx_pm.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))
                    if channel["name"]=="Branch":
                        file_out_itx_pm_branch.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))
                    if channel["name"]=="Call Center":
                        file_out_itx_pm_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))
                    if channel["name"]=="Web":
                        file_out_itx_pm_web.write('%s;%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount,accountType["name"]))

            elif goal["name"]=="contact" :
#                nbrITX_CE=nbrITX_CE+1
                subgoal=pick_subgoalcategories(j,goal)
                channel=pick_channelcategories(j,subgoal)
                if channel["name"]=="Mobile App" and regMobileApp==0 :
                   channel["name"]="Web"
                date=radar.random_datetime(mindate,maxdate)
                time=dt.time(r.randint(6,21),r.randint(0,59),r.randint(0,59))
                amount=pick_amount(j,subgoal)
                file_out_itx_ce.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Branch":
                    file_out_itx_ce_branch.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Call Center":
                    file_out_itx_ce_callcenter.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Email":
                    file_out_itx_ce_email.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Mobile App":
                    date=radar.random_datetime(regDateMobileApp,maxdate)
                    file_out_itx_ce_mobileapp.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))
                if channel["name"]=="Web":
                    file_out_itx_ce_web.write('%s;%s;%s;%s;%s;%s;%s;%s\n' %(id,j,date,time,goal["name"],subgoal["name"],channel["name"],amount))



        if (progress):
            pb.next()
        else:
            print "Done for id %s" % (id)
            if (id == len(crm_df)):
                print "Done!"

if __name__ == "__main__":
    main()
