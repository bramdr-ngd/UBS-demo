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
parser = argparse.ArgumentParser(description='Generate product data for Lily demo environments.')
parser.add_argument('-c','--customers', help='customer data file',required=False, default='.data/CrmDataToFilter.csv')
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

def load(file):
    with open(file) as data_file:
        return json.load(data_file)

def load_profile(segnr, segments_data):
    return segments_data[segnr-1]

def pick_random_pct_min_max(array):
    random= r.uniform(size=1)

    for i in range(len(array)):
        if random > array[i]["pct_min"] and random <= array[i]["pct_max"]:
            return array[i]

def pick_CheckingsAccount(i, segments_data):
    return pick_random_pct_min_max(segments_data["Checkings Account"])
def pick_CreditCard(i, segments_data):
    return pick_random_pct_min_max(segments_data["Credit Card"])
def pick_SavingsAccount(i, segments_data):
    return pick_random_pct_min_max(segments_data["Savings Account"])
def pick_InvestmentAccount(i, segments_data):
    return pick_random_pct_min_max(segments_data["Investment Account"])
def pick_MutualFunds(i, segments_data):
    return pick_random_pct_min_max(segments_data["Mutual Funds"])
def pick_Bonds(i, segments_data):
    return pick_random_pct_min_max(segments_data["Bond Product"])
def pick_Annuities(i, segments_data):
    return pick_random_pct_min_max(segments_data["Annuities Product"])
def pick_Stocks(i, segments_data):
    return pick_random_pct_min_max(segments_data["Stock Product"])
def pick_Options(i, segments_data):
    return pick_random_pct_min_max(segments_data["Option Product"])
def pick_RetirementAccount(i, segments_data):
    return pick_random_pct_min_max(segments_data["Retirement Account"])
def pick_LifeInsurance(i, segments_data):
    return pick_random_pct_min_max(segments_data["Life Insurance"])
def pick_PersonalLoan(i, segments_data):
    return pick_random_pct_min_max(segments_data["Personal Loan"])
def pick_Mortgage(i, segments_data):
    return pick_random_pct_min_max(segments_data["Mortgage"])
def pick_HomeEquityLoan(i, segments_data):
    return pick_random_pct_min_max(segments_data["Home Equity Loan"])
def pick_CarLoan(i, segments_data):
    return pick_random_pct_min_max(segments_data["Car Loan"])

def pick_prodid(i, entity):
    return int(entity["id"])

def pick_value(i, entity):
    return (entity["value"])
def pick_value_random(i, entity):
    return r.uniform (entity["value_random"][0],entity["value_random"][1])
def pick_value_random_normal(i, entity):
    return r.normal(entity["value_random"][0],entity["value_random"][1])

def pick_type_blanc(i, entity):
    return (entity["type"])

def pick_type(i, entity):
    return pick_random_pct_min_max((entity["type"]))

def pick_actif(i, entity):
    return (entity["actif"])

def pick_startdate(i, entity):
    return (entity["startdate"])

def pick_enddate(i, entity):
    return (entity["enddate"])

def pick_minstartYYYY(i, startdate):
    return int(startdate[0]["min_date_YYYYMMDD"][0])
def pick_minstartMM(i, startdate):
    return int(startdate[0]["min_date_YYYYMMDD"][1])
def pick_minstartDD(i, startdate):
    return int(startdate[0]["min_date_YYYYMMDD"][2])

def pick_maxstartYYYY(i, startdate):
    return int(startdate[1]["max_date_YYYYMMDD"][0])
def pick_maxstartMM(i, startdate):
    return int(startdate[1]["max_date_YYYYMMDD"][1])
def pick_maxstartDD(i, startdate):
    return int(startdate[1]["max_date_YYYYMMDD"][2])

def pick_minendYYYY(i, enddate):
    return int(enddate[0]["min_date_YYYYMMDD"][0])
def pick_minendMM(i, enddate):
    return int(enddate[0]["min_date_YYYYMMDD"][1])
def pick_minendDD(i, enddate):
    return int(enddate[0]["min_date_YYYYMMDD"][2])

def pick_maxendYYYY(i, enddate):
    return int(enddate[1]["max_date_YYYYMMDD"][0])
def pick_maxendMM(i, enddate):
    return int(enddate[1]["max_date_YYYYMMDD"][1])
def pick_maxendDD(i, enddate):
    return int(enddate[1]["max_date_YYYYMMDD"][2])


# Import customer data
crm_df = pd.read_csv(c_file, sep=';')
#print list(crm_df.columns.values)
#print crm_df

#def pick_channelcategories(n,subgoal):
#    return pick_random_pct_min_max(subgoal["Channel_categories"])

def main():
    segment_ent_data = [
        load(model_file('segment_ent_1.json')),
        load(model_file('segment_ent_2.json')),
        load(model_file('segment_ent_3.json')),
        "",
        load(model_file('segment_ent_5.json')),
        load(model_file('segment_ent_6.json')),
        load(model_file('segment_ent_7.json'))
    ]

    file_out_ent =open(output_file("EntityDataAll.csv"), 'w')
    file_out_ent.write('ENTITY_ID;ID;PRODUCT;WAARDE;START;END;TYPE;SUBTYPE;ACTIF;\n')

    file_out_enthd =open(output_file("EntityDataToLoad.hdr"), 'w')
    file_out_enthd.write('ENTITY_ID;ID;PRODUCT;START;TYPE;SUBTYPE;ACTIF;\n')

    file_out_ent2 =open(output_file("EntityDataToLoad.csv"), 'w')


    pb = Bar('Generating', max=len(crm_df), fill='=', suffix='%(percent)d%%')
    for id in range(1, len(crm_df) + 1):

        idnr1=0 #Checkingsaccount
        idnr2=0 #Credit Card
        idnr3=0 #Savingsaccount
        idnr4A=0 #MutualFunds
        idnr4B=0 #MutualFunds
        idnr5A=0 #flagBonds
        idnr5B=0 #flagBonds
        idnr6=0 #flagAnnuities
        idnr7A=0 #flagStocks
        idnr7B=0 #flagStocks
        idnr8A=0 #flagOptions
        idnr8B=0 #flagOptions
        idnr9=0 #investmentaccount
        idnr10=0 #retirementaccount
        idnr11=0 #flagLifeInsurance
        idnr12=0 #flagParsonalLoan
        idnr13=0 #Mortgage
        idnr14=0 #HomeEquityLoan
        idnr15=0 #CarLoan

        segnr_crm = crm_df.ix[id-1,'segnr']
        profile_data=load_profile(segnr_crm,segment_ent_data)

        if crm_df.ix[id-1,'flagCheckingsAccount']== 1 :
            entity_name=pick_CheckingsAccount(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr1=idnr1+1
            entity_id=entity_id+id*1000+idnr1
            value=pick_value_random_normal(id,entity_name)

            startdate=pick_startdate(id,entity_name)
            enddate=pick_enddate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            min_enddate=datetime.date(pick_minendYYYY(id,enddate),pick_minendMM(id,enddate),pick_minendDD(id,enddate))
            max_enddate=datetime.date(pick_maxendYYYY(id,enddate),pick_maxendMM(id,enddate),pick_maxendDD(id,enddate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            end_date=radar.random_datetime(min_enddate,max_enddate)

            subtype_blanc=pick_type_blanc(id,entity_name)
            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagCreditCard']== 1 :
            entity_name=pick_CreditCard(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr2=idnr2+1
            entity_id=entity_id+id*1000+idnr2
            value=pick_value(id,entity_name)

            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            end_date=start_date + datetime.timedelta(weeks=260)
            subtype=pick_type(id,entity_name)
            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype["name"],actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype["name"],actif))
#1
            if actif=="false" and end_date < datetime.date.today():
                entity_id=pick_prodid(id,entity_name)
                idnr2=idnr2+1
                entity_id=entity_id+id*1000+idnr2
                start_date=end_date
                end_date=start_date + datetime.timedelta(weeks=260)
                if end_date < datetime.date.today() or start_date > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype["name"],actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype["name"],actif))
#2
            if actif=="false" and end_date < datetime.date.today():
                entity_id=pick_prodid(id,entity_name)
                idnr2=idnr2+1
                entity_id=entity_id+id*1000+idnr2
                start_date=end_date
                end_date=start_date + datetime.timedelta(weeks=260)
                if end_date < datetime.date.today() or start_date > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype["name"],actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype["name"],actif))
#3
            if actif=="false" and end_date < datetime.date.today():
                entity_id=pick_prodid(id,entity_name)
                idnr2=idnr2+1
                entity_id=entity_id+id*1000+idnr2
                start_date=end_date
                end_date=start_date + datetime.timedelta(weeks=260)
                if end_date < datetime.date.today() or start_date > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype["name"],actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype["name"],actif))


        if crm_df.ix[id-1,'flagSavingsAccount']== 1 :
            entity_name=pick_SavingsAccount(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr3=idnr3+1
            entity_id=entity_id+id*1000+idnr3
            value=pick_value_random_normal(id,entity_name)

            startdate=pick_startdate(id,entity_name)
            enddate=pick_enddate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            min_enddate=datetime.date(pick_minendYYYY(id,enddate),pick_minendMM(id,enddate),pick_minendDD(id,enddate))
            max_enddate=datetime.date(pick_maxendYYYY(id,enddate),pick_maxendMM(id,enddate),pick_maxendDD(id,enddate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            end_date=radar.random_datetime(min_enddate,max_enddate)

            subtype_blanc=pick_type_blanc(id,entity_name)
            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagMutualFunds']== 1 :
            entity_name=pick_MutualFunds(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr4A=idnr4A+1
            entity_id=entity_id+id*1000+idnr4A
            value=(pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets'])/(crm_df.ix[id-1,'flagInvestmentAccount']+crm_df.ix[id-1,'flagMutualFunds']+crm_df.ix[id-1,'flagBonds']+crm_df.ix[id-1,'flagAnnuities']+crm_df.ix[id-1,'flagStocks']+crm_df.ix[id-1,'flagOptions']+crm_df.ix[id-1,'flagRetirementAccount'])
            valueMF1=value

            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            start_dateMF1=start_date
            randomdays=r.uniform(50,200)
            end_date=start_date + datetime.timedelta(days=randomdays)
            end_dateMF1=end_date
            subtype_blanc=pick_type_blanc(id,entity_name)
            if end_dateMF1 < datetime.date.today() or start_dateMF1 > datetime.date.today():
                actif="false"
            else :
                actif="true"
            actifMF1=actif
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

#1A Renewal of current Mutual Fund
            if actif=="false"  and end_dateMF1 < datetime.date.today():
                entity_id=pick_prodid(id,entity_name)
                idnr4A=idnr4A+1
                entity_id=entity_id+id*1000+idnr4A
                start_date=end_date
                start_dateMFR1=end_date
                randomdays=r.uniform(50,200)
                end_date=start_date + datetime.timedelta(days=randomdays)
                end_dateMFR1=end_date
                value=value+(value*r.uniform(0.1,0.3))
                valueMFR1=value
                if end_dateMFR1 < datetime.date.today() or start_dateMFR1 > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                actifMFR1=actif
                subtype_blanc=pick_type_blanc(id,entity_name)
                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

#1B Adding an extra Mutual Fund
            randomMutualFonds=r.uniform(0,1)
            if randomMutualFonds>=0.8 :
                entity_name=pick_MutualFunds(id,profile_data)
                type=entity_name["name"]
                entity_id=pick_prodid(id,entity_name)
                idnr4B=idnr4B+1
                entity_id=entity_id+id*1000+idnr4B
                value=(crm_df.ix[id-1,'totalAssets']*r.uniform(0.05,0.25))
                valueMF2=value
                randomdays1=r.uniform(5,20)

                min_startdate=start_date + datetime.timedelta(days=randomdays1)
                randomdays2=r.uniform(50,200)
#                randomdays2=r.uniform(20,50)
#                max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate)) + datetime.timedelta(days=randomdays2)
                max_startdate=min_startdate + datetime.timedelta(days=randomdays2)
                start_date=radar.random_datetime(min_startdate,max_startdate)
                start_dateMF2=start_date
                end_date=start_date+datetime.timedelta(days=int(r.uniform(1,2))*365)
                end_dateMF2=end_date
                if end_dateMF2 < datetime.date.today() or start_dateMF2 > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                actifMF2=actif
                subtype_blanc=pick_type_blanc(id,entity_name)
                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))


        if crm_df.ix[id-1,'flagBonds']== 1 :
            entity_name=pick_Bonds(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr5A=idnr5A+1
            entity_id=entity_id+id*1000+idnr5A
            value=(pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets'])/(crm_df.ix[id-1,'flagInvestmentAccount']+crm_df.ix[id-1,'flagMutualFunds']+crm_df.ix[id-1,'flagBonds']+crm_df.ix[id-1,'flagAnnuities']+crm_df.ix[id-1,'flagStocks']+crm_df.ix[id-1,'flagOptions']+crm_df.ix[id-1,'flagRetirementAccount'])
            valueBD1=value
            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            start_dateBD1=start_date
            randomdays=r.uniform(50,200)
            end_date=start_date + datetime.timedelta(days=randomdays)
            end_dateBD1=end_date
            subtype_blanc=pick_type_blanc(id,entity_name)
            if end_dateBD1 < datetime.date.today() or start_dateBD1 > datetime.date.today():
                actif="false"
            else :
                actif="true"
            actifBD1=actif

            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

#1A Renewal of current Bond Product
            if actif=="false" and end_dateMF1 < datetime.date.today():
                entity_id=pick_prodid(id,entity_name)
                idnr5A=idnr5A+1
                entity_id=entity_id+id*1000+idnr5A
                start_date=end_date
                start_dateBDR1=start_date
                randomdays=r.uniform(50,200)
                end_date=start_date + datetime.timedelta(days=randomdays)
                end_dateBDR1=end_date
                value=value+(value*r.uniform(0.1,0.3))
                valueBDR1=value
                if end_dateBDR1 < datetime.date.today() or start_dateBDR1 > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                actifBDR1=actif
                subtype_blanc=pick_type_blanc(id,entity_name)
                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

#1B Adding an extra Bond Product
            randomBonds=r.uniform(0,1)
            if randomBonds>=0.8 :
                entity_name=pick_Bonds(id,profile_data)
                type=entity_name["name"]
                entity_id=pick_prodid(id,entity_name)
                idnr5B=idnr5B+1
                entity_id=entity_id+id*1000+idnr5B
                value=(crm_df.ix[id-1,'totalAssets']*r.uniform(0.05,0.25))
                valueBD2=value
                randomdays=r.uniform(50,200)

                min_startdate=start_date + datetime.timedelta(days=randomdays)
                randomdays=r.uniform(50,200)
                max_startdate=min_startdate + datetime.timedelta(days=randomdays)
                start_date=radar.random_datetime(min_startdate,max_startdate)
                start_dateBD2=start_date
                end_date=start_date+datetime.timedelta(days=int(r.uniform(1,2))*365)
                end_dateBD2=end_date
                if end_dateBD2 < datetime.date.today() or start_dateBD2 > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                actifBD2=actif
                subtype_blanc=pick_type_blanc(id,entity_name)

                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagAnnuities']== 1 :
            entity_name=pick_Annuities(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr6=idnr6+1
            entity_id=entity_id+id*1000+idnr6
            value=(pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets'])/(crm_df.ix[id-1,'flagInvestmentAccount']+crm_df.ix[id-1,'flagMutualFunds']+crm_df.ix[id-1,'flagBonds']+crm_df.ix[id-1,'flagAnnuities']+crm_df.ix[id-1,'flagStocks']+crm_df.ix[id-1,'flagOptions']+crm_df.ix[id-1,'flagRetirementAccount'])

            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            rr=r.uniform(0,1)
            if rr<=0.20:
                end_date=start_date + datetime.timedelta(days=5*365)
            elif rr<=0.40:
                end_date=start_date + datetime.timedelta(days=10*365)
            elif rr<=0.60:
                end_date=start_date + datetime.timedelta(days=15*365)
            elif rr<=0.80:
                end_date=start_date + datetime.timedelta(days=20*365)
            else:
                end_date=start_date + datetime.timedelta(days=25*365)

            subtype_blanc=pick_type_blanc(id,entity_name)
            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagStocks']== 1 :
            entity_name=pick_Stocks(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr7A=idnr7A+1
            entity_id=entity_id+id*1000+idnr7A
            value=(pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets'])/(crm_df.ix[id-1,'flagInvestmentAccount']+crm_df.ix[id-1,'flagMutualFunds']+crm_df.ix[id-1,'flagBonds']+crm_df.ix[id-1,'flagAnnuities']+crm_df.ix[id-1,'flagStocks']+crm_df.ix[id-1,'flagOptions']+crm_df.ix[id-1,'flagRetirementAccount'])
            valueST1=value
            startdate=pick_startdate(id,entity_name)
            enddate=pick_enddate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            start_dateST1=start_date
            min_enddate=datetime.date(pick_minendYYYY(id,enddate),pick_minendMM(id,enddate),pick_minendDD(id,enddate))
            max_enddate=datetime.date(pick_maxendYYYY(id,enddate),pick_maxendMM(id,enddate),pick_maxendDD(id,enddate))
            end_date=radar.random_datetime(min_enddate,max_enddate)
            end_dateST1=end_date
            subtype_blanc=pick_type_blanc(id,entity_name)
            if end_dateST1 < datetime.date.today() or start_dateST1 > datetime.date.today():
                actif="false"
            else :
                actif="true"
            actifST1=actif
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

#1B Adding an extra Stocks Product
            randomStocks=r.uniform(0,1)
            if randomStocks>=0.8 :
                entity_name=pick_Stocks(id,profile_data)
                type=entity_name["name"]
                entity_id=pick_prodid(id,entity_name)
                idnr7B=idnr7B+1
                entity_id=entity_id+id*1000+idnr7B
                value=(crm_df.ix[id-1,'totalAssets']*r.uniform(0.05,0.25))
                valueST2=value
                randomdays1=r.uniform(30,180)

                min_startdate=start_date + datetime.timedelta(days=randomdays1)
                randomdays2=r.uniform(50,200)
                max_startdate=min_startdate + datetime.timedelta(days=randomdays2)
#                max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
                start_date=radar.random_datetime(min_startdate,max_startdate)
                start_dateST2=start_date
                min_enddate=datetime.date(pick_minendYYYY(id,enddate),pick_minendMM(id,enddate),pick_minendDD(id,enddate))
                max_enddate=datetime.date(pick_maxendYYYY(id,enddate),pick_maxendMM(id,enddate),pick_maxendDD(id,enddate))
                end_date=radar.random_datetime(min_enddate,max_enddate)
                end_dateST2=end_date
                if end_dateST2 < datetime.date.today() or start_dateST2 > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                actifST2=actif
                subtype_blanc=pick_type_blanc(id,entity_name)

                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))


        if crm_df.ix[id-1,'flagOptions']== 1 :
            entity_name=pick_Options(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr8A=idnr8A+1
            entity_id=entity_id+id*1000+idnr8A
            value=(pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets'])/(crm_df.ix[id-1,'flagInvestmentAccount']+crm_df.ix[id-1,'flagMutualFunds']+crm_df.ix[id-1,'flagBonds']+crm_df.ix[id-1,'flagAnnuities']+crm_df.ix[id-1,'flagStocks']+crm_df.ix[id-1,'flagOptions']+crm_df.ix[id-1,'flagRetirementAccount'])
            valueOP1=value
            startdate=pick_startdate(id,entity_name)
            enddate=pick_enddate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            start_dateOP1=start_date
            min_enddate=datetime.date(pick_minendYYYY(id,enddate),pick_minendMM(id,enddate),pick_minendDD(id,enddate))
            max_enddate=datetime.date(pick_maxendYYYY(id,enddate),pick_maxendMM(id,enddate),pick_maxendDD(id,enddate))
#            start_date=radar.random_datetime(min_startdate,max_startdate)
            end_date=radar.random_datetime(min_enddate,max_enddate)
            end_dateOP1=end_date
            subtype_blanc=pick_type_blanc(id,entity_name)
            if end_dateOP1 < datetime.date.today() or start_dateOP1 > datetime.date.today():
                actif="false"
            else :
                actif="true"
            actifOP1=actif
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

#1B Adding an extra Options Product
            randomOptions=r.uniform(0,1)
            if randomOptions>=0.8 :
                entity_name=pick_Stocks(id,profile_data)
                type=entity_name["name"]
                entity_id=pick_prodid(id,entity_name)
                idnr8B=idnr8B+1
                entity_id=entity_id+id*1000+idnr8B
                value=(crm_df.ix[id-1,'totalAssets']*r.uniform(0.05,0.25))
                valueOP2=value
                randomdays1=r.uniform(30,180)

                min_startdate=start_date + datetime.timedelta(days=randomdays1)
                randomdays2=r.uniform(50,200)
                max_startdate=min_startdate + datetime.timedelta(days=randomdays2)

#                max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
                start_date=radar.random_datetime(min_startdate,max_startdate)
                start_dateOP2=start_date
                min_enddate=datetime.date(pick_minendYYYY(id,enddate),pick_minendMM(id,enddate),pick_minendDD(id,enddate))
                max_enddate=datetime.date(pick_maxendYYYY(id,enddate),pick_maxendMM(id,enddate),pick_maxendDD(id,enddate))
                end_date=radar.random_datetime(min_enddate,max_enddate)
                end_dateOP2=end_date

                subtype_blanc=pick_type_blanc(id,entity_name)

                if end_dateOP2 < datetime.date.today() or start_dateOP2 > datetime.date.today():
                    actif="false"
                else :
                    actif="true"
                actifOP2=actif
                file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
                file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagMutualFunds']== 1 or crm_df.ix[id-1,'flagBonds']== 1 or crm_df.ix[id-1,'flagStocks']== 1  or crm_df.ix[id-1,'flagOptions']== 1:
            entity_name=pick_InvestmentAccount(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr9=idnr9+1
            entity_id=entity_id+id*1000+idnr9
            value=0

            if crm_df.ix[id-1,'flagMutualFunds']== 1:
                if actifMF1=="true":
                    value=value + valueMF1
                if actifMFR1=="true":
                    value=value + valueMFR1
                if randomMutualFonds>=0.8:
                    if actifMF2=="true":
                        value=value + valueMF2

            if crm_df.ix[id-1,'flagBonds']== 1:
                if actifBD1=="true":
                    value=value + valueBD1
                if actifBDR1=="true":
                    value=value + valueBDR1
                if randomBonds>=0.8:
                    if actifBD2=="true":
                        value=value + valueBD2

            if crm_df.ix[id-1,'flagStocks']== 1:
                if actifST1=="true":
                    value=value + valueST1
                if randomStocks>=0.8:
                    if actifST2=="true":
                        value=value + valueST2

            if crm_df.ix[id-1,'flagOptions']== 1:
                if actifOP1=="true":
                    value=value + valueOP1
                if randomOptions>=0.8:
                    if actifOP2=="true":
                        value=value + valueOP2

            start_date=datetime.date(2999,1,1)
            if crm_df.ix[id-1,'flagMutualFunds']== 1:
                if start_dateMF1 <=start_date:
                    start_date=start_dateMF1
                if start_dateMFR1 <=start_date:
                    start_date=start_dateMFR1
                if randomMutualFonds>=0.8:
                    if start_dateMF2 <=start_date:
                        start_date=start_dateMF2

            if crm_df.ix[id-1,'flagBonds']== 1:
                if start_dateBD1 <=start_date:
                    start_date=start_dateBD1
                if start_dateBDR1 <=start_date:
                    start_date=start_dateBDR1
                if randomBonds>=0.8:
                    if start_dateBD2 <=start_date:
                        start_date=start_dateBD2


            if crm_df.ix[id-1,'flagStocks']== 1:
                if start_dateST1 <=start_date:
                    start_date=start_dateST1
                if randomStocks>=0.8:
                    if start_dateST2 <=start_date:
                        start_date=start_dateST2

            if crm_df.ix[id-1,'flagOptions']== 1:
                if start_dateOP1 <=start_date:
                    start_date=start_dateOP1
                if randomOptions>=0.8:
                    if start_dateOP2 <=start_date:
                        start_date=start_dateOP2
            end_date=datetime.date(2999,1,1)

            if end_date < datetime.date.today() :
               actif="false"
            else :
               actif="true"

            subtype=""
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype,actif))


        if crm_df.ix[id-1,'flagRetirementAccount']== 1 and crm_df.ix[id-1,'age']<= 65 :
            entity_name=pick_RetirementAccount(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr10=idnr10+1
            entity_id=entity_id+id*1000+idnr10
            value=(pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets'])/(crm_df.ix[id-1,'flagInvestmentAccount']+crm_df.ix[id-1,'flagMutualFunds']+crm_df.ix[id-1,'flagBonds']+crm_df.ix[id-1,'flagAnnuities']+crm_df.ix[id-1,'flagStocks']+crm_df.ix[id-1,'flagOptions']+crm_df.ix[id-1,'flagRetirementAccount'])

            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            yearstoend=int(65-crm_df.ix[id-1,'age'])

            end_date=start_date + datetime.timedelta(days=yearstoend*365)

            subtype_blanc=pick_type_blanc(id,entity_name)

            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"
            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagLifeInsurance']== 1 :
            entity_name=pick_LifeInsurance(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr11=idnr11+1
            entity_id=entity_id+id*1000+idnr11
            value=pick_value_random(id,entity_name)*crm_df.ix[id-1,'monthlyIncome']

            startdate=pick_startdate(id,entity_name)
            enddate=pick_enddate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            min_enddate=datetime.date(pick_minendYYYY(id,enddate),pick_minendMM(id,enddate),pick_minendDD(id,enddate))
            max_enddate=datetime.date(pick_maxendYYYY(id,enddate),pick_maxendMM(id,enddate),pick_maxendDD(id,enddate))
            end_date=radar.random_datetime(min_enddate,max_enddate)

            subtype_blanc=pick_type_blanc(id,entity_name)

            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"

            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagPersonalLoan']== 1 :
            entity_name=pick_PersonalLoan(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr12=idnr12+1
            entity_id=entity_id+id*1000+idnr12
            value=pick_value_random(id,entity_name)*crm_df.ix[id-1,'monthlyIncome']

            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            diffdays=(datetime.date.today()-start_date)*int(r.uniform(1,3))
            end_date=start_date+diffdays

            subtype_blanc=pick_type_blanc(id,entity_name)

            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"

            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagMortgage']== 1 and crm_df.ix[id-1,'houseOwner']== 1:
            entity_name=pick_Mortgage(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr13=idnr13+1
            entity_id=entity_id+id*1000+idnr13
            value=pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets']

            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)

            randomLooptijd=r.uniform(0,1)
            if randomLooptijd<0.33 :
                end_date=start_date+datetime.timedelta(days=15*365)
            elif randomLooptijd<0.66 :
                end_date=start_date+datetime.timedelta(days=20*365)
            else:
                end_date=start_date+datetime.timedelta(days=25*365)

            subtype_blanc=pick_type_blanc(id,entity_name)

            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"

            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagHomeEquityLoan']== 1 and crm_df.ix[id-1,'houseOwner']== 1:
            entity_name=pick_HomeEquityLoan(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr14=idnr14+1
            entity_id=entity_id+id*1000+idnr14
            value=pick_value_random(id,entity_name)*crm_df.ix[id-1,'totalAssets']

            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            randomLooptijd=r.uniform(0,1)
            if randomLooptijd<0.33 :
                end_date=start_date+datetime.timedelta(days=15*365)
            elif randomLooptijd<0.66 :
                end_date=start_date+datetime.timedelta(days=20*365)
            else:
                end_date=start_date+datetime.timedelta(days=25*365)

            subtype_blanc=pick_type_blanc(id,entity_name)

            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"

            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        if crm_df.ix[id-1,'flagCarLoan']== 1:
            entity_name=pick_CarLoan(id,profile_data)
            type=entity_name["name"]
            entity_id=pick_prodid(id,entity_name)
            idnr15=idnr15+1
            entity_id=entity_id+id*1000+idnr15


            startdate=pick_startdate(id,entity_name)
            min_startdate=datetime.date(pick_minstartYYYY(id,startdate),pick_minstartMM(id,startdate),pick_minstartDD(id,startdate))
            max_startdate=datetime.date(pick_maxstartYYYY(id,startdate),pick_maxstartMM(id,startdate),pick_maxstartDD(id,startdate))
            start_date=radar.random_datetime(min_startdate,max_startdate)
            randomLooptijd=int(r.uniform(2,5))
            end_date=start_date+datetime.timedelta(days=randomLooptijd*365)

            if randomLooptijd==2 :
                value=int(r.uniform(500,3699))
            elif randomLooptijd==3 :
                value=int(r.uniform(3700,7499))
            elif randomLooptijd==4 :
                value=int(r.uniform(7500,9999))
            else:
                value=int(r.uniform(10000,150000))

            subtype_blanc=pick_type_blanc(id,entity_name)

            if end_date < datetime.date.today() or start_date > datetime.date.today():
                actif="false"
            else :
                actif="true"

            file_out_ent.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],value,start_date,end_date,type,subtype_blanc,actif))
            file_out_ent2.write('%s;%s;%s;%s;%s;%s;%s;\n' %(entity_id,id,entity_name["name"],start_date,type,subtype_blanc,actif))

        pb.next()

if __name__ == "__main__":
    main()
