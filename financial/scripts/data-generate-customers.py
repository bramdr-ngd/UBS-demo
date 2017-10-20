#!/usr/bin/python
import argparse
from progress.bar import Bar
import json
from numpy.random import seed
from numpy.random import RandomState
import pandas as pd
import datetime
import radar
from scipy.interpolate import interp1d
import numpy as np

#TODO remove blank spaces when writing float values e.g. %10.2f
#TODO generate folder structure for target file if not exists

# globals
seedValue = 1234
seed(seed=seedValue)
r = RandomState(seedValue)

# Read command line args
parser = argparse.ArgumentParser(description='Generate customer CRM data for Lily demo environments.')
parser.add_argument('-n','--nrrecords', type=int, help='Number of records to generate',required=False, default=10)
parser.add_argument('-o','--output', help='output folder',required=False, default='.data')
parser.add_argument('-m','--model', help='model file folder',required=False, default='data-generate-model')
args = parser.parse_args()

nr_records = args.nrrecords
o_folder = args.output
m_folder = args.model

# functions
def output_file(file_name):
    return o_folder + "/" + file_name

def model_file(file_name):
    return m_folder + "/" + file_name

def load(file):
    with open(file) as data_file:
        return json.load(data_file)

def pick_segment(id, segments, segments_data):
    segnr = pick_random_pct_min_max(segments)["segnr"]

    # Fix Krista Johnson for our sales people
    if (id == 3346):
        segnr = 2

    return segments_data[segnr-1]

def pick_age_category(i, segment):
    age_category=pick_random_pct_min_max(segment["age_categories"])
    if (i == 22639):
        age_category["name"] = "35-49"
    return age_category
#    return pick_random_pct_min_max(segment["age_categories"])

def pick_age(i, age_category):
    age=r.randint(age_category["random_age"][0], age_category["random_age"][1])
    if (i == 22639):
        age = 46
    return age
#    return r.randint(age_category["random_age"][0], age_category["random_age"][1])

def pick_occupation(i, segment):
    return pick_random_pct_min_max(segment["occupation_categories"])

def pick_lifestage(i, segment):
    return pick_random_pct_min_max(segment["lifestage_categories"])

def pick_isStudent(i, segment, age):
    if age<=24 :
        isStudent=pick_random_pct_min_max(segment["isStudent_categories"])
        isStudent_recode=int(isStudent["name"])
    else :
        isStudent_recode=0

    return isStudent_recode

def pick_isRetired(i, segment, age):
    if age>=55 and age <=65 :
        isRetired=pick_random_pct_min_max(segment["isRetired_categories"])
        isRetired_recode=int(isRetired["name"])
    elif age>65:
        isRetired_recode=1
    else :
        isRetired_recode=0

    return isRetired_recode

def pick_education(i, segment):
    return pick_random_pct_min_max(segment["education_categories"])

def pick_maritalStatus(i, segment):
    return pick_random_pct_min_max(segment["maritalStatus_categories"])

def pick_monthlyIncome(i, segment):
    return r.uniform(segment["Random_monthlyIncome"][0], segment["Random_monthlyIncome"][1])

def pick_nbrChildren(i, segment):
    return pick_random_pct_min_max(segment["nbrChildren_categories"])

def pick_mainNationality(i, segment):
    return pick_random_pct_min_max(segment["mainNationality_categories"])

def pick_mainLanguage(i, segment):
    return pick_random_pct_min_max(segment["mainLanguage_categories"])

def pick_houseOwner(i, segment):
    return pick_random_pct_min_max(segment["houseOwner_categories"])

def pick_homeTenant(i, segment, houseOwner):
    if houseOwner["name"]== "1":
        homeTenant = 0
    else :
        homeTenant=1

    return homeTenant

def pick_valueProperty(i, segment):
    return pick_random_pct_min_max(segment["valueProperty_categories"])

def pick_nbrPropertiesOwned(i, segment, houseOwner):
    if houseOwner["name"]== "1":
        nbrPropertiesOwned = pick_random_pct_min_max(segment["nbrPropertiesOwned_categories"])
        nbrPropertiesOwned_recode = nbrPropertiesOwned["name"]
    else :
        nbrPropertiesOwned_recode="0"

    return nbrPropertiesOwned_recode

def pick_landLord(i, segment, houseOwner):
    if houseOwner["name"]== "1":
        landLord = pick_random_pct_min_max(segment["landLord_categories"])
        landLord_recode = landLord["name"]
    else :
        landLord_recode="0"

    return landLord_recode

def pick_wealthyRegion(i, segment):
    return pick_random_pct_min_max(segment["wealthyRegion_categories"])

def pick_shareOfWallet(i, segment):
    return r.randint(segment["Random_shareOfWallet"][0],segment["Random_shareOfWallet"][1])

def pick_shareOfWalletHoldings(i, segment):
    return r.randint(segment["Random_shareOfWalletHoldings"][0],segment["Random_shareOfWalletHoldings"][1])

def pick_shareOfWalletSize(i, segment):
    return r.randint(segment["Random_shareOfWalletSize"][0],segment["Random_shareOfWalletSize"][1])

def pick_totalBankProducts(i, segment):
    return r.randint(segment["Random_totalBankProducts"][0],segment["Random_totalBankProducts"][1])

def pick_flagPFSP(i, segment):
    return pick_random_pct_min_max(segment["flagPFSP_categories"])

def pick_flagCheckingsAccount(i, segment):
    return pick_random_pct_min_max(segment["flagCheckingsAccount_categories"])

def pick_flagCreditCard(i, segment):
    return pick_random_pct_min_max(segment["flagCreditCard_categories"])

def pick_flagPayment(i, segment):
    return pick_random_pct_min_max(segment["flagPayment_categories"])

def pick_flagSavingsAccount(i, segment):
    return pick_random_pct_min_max(segment["flagSavingsAccount_categories"])

def pick_flagInvestmentAccount(i, segment):
    return pick_random_pct_min_max(segment["flagInvestmentAccount_categories"])

def pick_flagMutualFunds(i, segment):
    return pick_random_pct_min_max(segment["flagMutualFunds_categories"])

def pick_flagBonds(i, segment):
    return pick_random_pct_min_max(segment["flagBonds_categories"])

def pick_flagAnnuities(i, segment):
    return pick_random_pct_min_max(segment["flagAnnuities_categories"])

def pick_flagStocks(i, segment):
    return pick_random_pct_min_max(segment["flagStocks_categories"])

def pick_flagOptions(i, segment):
    return pick_random_pct_min_max(segment["flagOptions_categories"])

def pick_flagRetirementAccount(i, segment):
    return pick_random_pct_min_max(segment["flagRetirementAccount_categories"])

def pick_flagLifeInsurance(i, segment):
    return pick_random_pct_min_max(segment["flagLifeInsurance_categories"])

def pick_flagPersonalLoan(i, segment):
    return pick_random_pct_min_max(segment["flagPersonalLoan_categories"])

def pick_flagMortgage(i, segment):
    return pick_random_pct_min_max(segment["flagMortgage_categories"])

def pick_flagHomeEquityLoan(i, segment):
    return pick_random_pct_min_max(segment["flagHomeEquityLoan_categories"])

def pick_flagCarLoan(i, segment):
    carloan=pick_random_pct_min_max(segment["flagCarLoan_categories"])
    if (i == 22639):
        carloan["name"]="0"
    return carloan
#    return  pick_random_pct_min_max(segment["flagCarLoan_categories"])

def pick_startdate_flagCarLoanpreCampaign(i, segment,carloan):

    # STARTDATE
    x = (np.array([-6*365, 0, 150, 180, 210, 365]) + 6*365) / (7*365.)
    y = np.array([10, 20, 20, 20, 20, 20]) / 20.
    z = interp1d(x, y)

    start_datecarLoanpre=datetime.date(segment["startdate_flagCarLoanpreCampaign"][0],segment["startdate_flagCarLoanpreCampaign"][1],segment["startdate_flagCarLoanpreCampaign"][2])
    timeX = generateDistribution(z)
    randomLooptijd = int(timeX * (7*365))
    start_datecarLoanpre = start_datecarLoanpre + datetime.timedelta(days = randomLooptijd)
    if carloan["name"]=="1":
        start_datecarLoanpre_recode=start_datecarLoanpre
    else :
        start_datecarLoanpre_recode="1970-01-01"
    return start_datecarLoanpre_recode

def pick_startdate_flagCarLoanpostCampaign(i, segment,carLoanSale):
    start_datecarLoanpost=datetime.date(segment["startdate_flagCarLoanpostCampaign"][0],segment["startdate_flagCarLoanpostCampaign"][1],segment["startdate_flagCarLoanpostCampaign"][2])
    randomLooptijd = r.randint(0,59)
    start_datecarLoanpost = start_datecarLoanpost + datetime.timedelta(days = randomLooptijd)
    if carLoanSale["name"]=="1":
        start_datecarLoanpost_recode=start_datecarLoanpost
    else :
        start_datecarLoanpost_recode=start_datecarLoanpost
    return start_datecarLoanpost_recode

def pick_flagLoan(i, segment):
    return pick_random_pct_min_max(segment["flagLoan_categories"])

def pick_totalActiveProducts(i, segment):
    return r.randint(segment["Random_totalActiveProducts"][0],segment["Random_totalActiveProducts"][1])

def pick_totalReferrals(i, segment):
    return int(r.uniform(segment["Random_totalReferrals"][0],segment["Random_totalReferrals"][1]))

def pick_satisfaction(i, segment):
    return r.uniform(segment["Random_satisfaction"][0],segment["Random_satisfaction"][1])

def pick_churnScore(i, segment):
    return r.uniform(segment["Random_churnScore"][0], segment["Random_churnScore"][1])

def pick_flagOnlineBanking(i, segment):
    return pick_random_pct_min_max(segment["flagOnlineBanking_categories"])

def pick_flagOnlineBillPayment(i, segment):
    return pick_random_pct_min_max(segment["flagOnlineBillPayment_categories"])

def pick_flagMobilePayment(i, segment):
    return pick_random_pct_min_max(segment["flagMobilePayment_categories"])

def pick_flagReloadablePrepaidCards(i, segment):
    return pick_random_pct_min_max(segment["flagReloadablePrepaidCards_categories"])

def pick_totalAssets(i, segment):
    return r.randint(segment["Random_totalAssets"][0],segment["Random_totalAssets"][1])

def pick_flagDebtCollection(i, segment,totalAssets):
    if (id == 3346 or id ==22639):
        flagDebtCollection_recode="0"
    elif totalAssets<30000 :
        flagDebtCollection=pick_random_pct_min_max(segment["flagDebtCollection_categories"])
        flagDebtCollection_recode=flagDebtCollection["name"]
    else :
        flagDebtCollection_recode="0"
    return flagDebtCollection_recode

def pick_affNightLife(i, segment):
    return r.randint(segment["Random_affNightLife"][0],segment["Random_affNightLife"][1])

def pick_affSport(i, segment):
    return r.randint(segment["Random_affSport"][0],segment["Random_affSport"][1])

def pick_affHealthFitness(i, segment):
    return r.randint(segment["Random_affHealthFitness"][0],segment["Random_affHealthFitness"][1])

def pick_affOutdoor(i, segment):
    return r.randint(segment["Random_affOutdoor"][0],segment["Random_affOutdoor"][1])

def pick_affLuxuryShopper(i, segment):
    return r.randint(segment["Random_affLuxuryShopper"][0],segment["Random_affLuxuryShopper"][1])

def pick_affMovie(i, segment):
    return r.randint(segment["Random_affMovie"][0],segment["Random_affMovie"][1])

def pick_affPetLovers(i, segment):
    return r.randint(segment["Random_affPetLovers"][0],segment["Random_affPetLovers"][1])

def pick_affFastFood(i, segment):
    return r.randint(segment["Random_affFastFood"][0],segment["Random_affFastFood"][1])

def pick_affValueShopper(i, segment):
    return r.randint(segment["Random_affValueShopper"][0],segment["Random_affValueShopper"][1])

def pick_affTechnophiles(i, segment):
    return r.randint(segment["Random_affTechnophiles"][0],segment["Random_affTechnophiles"][1])

def pick_affGreenLiving(i, segment):
    return r.randint(segment["Random_affGreenLiving"][0],segment["Random_affGreenLiving"][1])

def pick_affMusic(i, segment):
    return r.randint(segment["Random_affMusic"][0],segment["Random_affMusic"][1])

def pick_affFoodies(i, segment):
    return r.randint(segment["Random_affFoodies"][0],segment["Random_affFoodies"][1])

def pick_affCooking(i, segment):
    return r.randint(segment["Random_affCooking"][0],segment["Random_affCooking"][1])

def pick_affShutterbugs(i, segment):
    return r.randint(segment["Random_affShutterbugs"][0],segment["Random_affShutterbugs"][1])

def pick_affSavvyParents(i, segment):
    return r.randint(segment["Random_affSavvyParents"][0],segment["Random_affSavvyParents"][1])

def pick_affDIY(i, segment):
    return r.randint(segment["Random_affDIY"][0],segment["Random_affDIY"][1])

def pick_affAuto(i, segment):
    return r.randint(segment["Random_affAuto"][0],segment["Random_affAuto"][1])

def pick_affFashionistas(i, segment):
    return r.randint(segment["Random_affFashionistas"][0],segment["Random_affFashionistas"][1])

def pick_affBeautyMavens(i, segment):
    return r.randint(segment["Random_affBeautyMavens"][0],segment["Random_affBeautyMavens"][1])

def pick_affHomeDecor(i, segment):
    return r.randint(segment["Random_affHomeDecor"][0],segment["Random_affHomeDecor"][1])

def pick_affPolitical(i, segment):
    return r.randint(segment["Random_affPolitical"][0],segment["Random_affPolitical"][1])

def pick_affAvidInvestor(i, segment):
    return r.randint(segment["Random_affAvidInvestor"][0],segment["Random_affAvidInvestor"][1])

def pick_affThrillSeeker(i, segment):
    return r.randint(segment["Random_affThrillSeeker"][0],segment["Random_affThrillSeeker"][1])

def pick_affBargainHunter(i, segment):
    return r.randint(segment["Random_affBargainHunter"][0],segment["Random_affBargainHunter"][1])

def pick_affTravelBuff(i, segment):
    return r.randint(segment["Random_affTravelBuff"][0],segment["Random_affTravelBuff"][1])

def pick_affLuxuryTravel(i, segment):
    return r.randint(segment["Random_affLuxuryTravel"][0],segment["Random_affLuxuryTravel"][1])

def pick_affFamilyVacation(i, segment):
    return r.randint(segment["Random_affFamilyVacation"][0],segment["Random_affFamilyVacation"][1])

def pick_affBeachTravel(i, segment):
    return r.randint(segment["Random_affBeachTravel"][0],segment["Random_affBeachTravel"][1])

def pick_affWinterTravel(i, segment):
    return r.randint(segment["Random_affWinterTravel"][0],segment["Random_affWinterTravel"][1])

def pick_affNewsJunky(i, segment):
    return r.randint(segment["Random_affNewsJunky"][0],segment["Random_affNewsJunky"][1])

def pick_affArtTheater(i, segment):
    return r.randint(segment["Random_affArtTheater"][0],segment["Random_affArtTheater"][1])

def pick_affGamer(i, segment):
    return r.randint(segment["Random_affGamer"][0],segment["Random_affGamer"][1])

def pick_affTV(i, segment):
    return r.randint(segment["Random_affTV"][0],segment["Random_affTV"][1])

def pick_flagContactAbilityLandline(i, segment):
    return pick_random_pct_min_max(segment["flagContactAbilityLandline_categories"])
def pick_flagContactAbilityMobileCall(i, segment):
    return pick_random_pct_min_max(segment["flagContactAbilityMobileCall_categories"])
def pick_flagContactAbilityEmail(i, segment):
    return pick_random_pct_min_max(segment["flagContactAbilityEmail_categories"])
def pick_flagContactAbilityMobileTxt(i, segment,flagContactAbilityMobileCall):
    if flagContactAbilityMobileCall["name"]== "1":
        flagContactAbilityMobileTxt = pick_random_pct_min_max(segment["flagContactAbilityMobileTxt_categories"])
        flagContactAbilityMobileTxt_recode = flagContactAbilityMobileTxt["name"]
    else :
        flagContactAbilityMobileTxt_recode="0"

    return flagContactAbilityMobileTxt_recode
def pick_flagContactAbilityDirectMail(i, segment):
    return pick_random_pct_min_max(segment["flagContactAbilityDirectMail_categories"])
def pick_flagContactAbilityInternet(i, segment):
    return pick_random_pct_min_max(segment["flagContactAbilityInternet_categories"])
def pick_flagContactAbilityTwitter(i, segment,flagContactAbilityInternet):
    if flagContactAbilityInternet["name"]== "1":
        flagContactAbilityTwitter = pick_random_pct_min_max(segment["flagContactAbilityTwitter_categories"])
        flagContactAbilityTwitter_recode = flagContactAbilityTwitter["name"]
    else :
        flagContactAbilityTwitter_recode="0"

    return flagContactAbilityTwitter_recode

def pick_flagContactAbilityFaceBook(i, segment,flagContactAbilityInternet):
    if flagContactAbilityInternet["name"]== "1":
        flagContactAbilityFaceBook = pick_random_pct_min_max(segment["flagContactAbilityFaceBook_categories"])
        flagContactAbilityFaceBook_recode = flagContactAbilityFaceBook["name"]
    else :
        flagContactAbilityFaceBook_recode="0"

    return flagContactAbilityFaceBook_recode

def pick_flagContactAbilityLinkedIn(i, segment,flagContactAbilityInternet):
    if flagContactAbilityInternet["name"]== "1":
        flagContactAbilityLinkedIn = pick_random_pct_min_max(segment["flagContactAbilityLinkedIn_categories"])
        flagContactAbilityLinkedIn_recode = flagContactAbilityLinkedIn["name"]
    else :
        flagContactAbilityLinkedIn_recode="0"

    return flagContactAbilityLinkedIn_recode
def pick_contactLandlineActive(i, segment,flagContactAbilityLandline):
    if flagContactAbilityLandline["name"]== "1":
        contactLandlineActive = pick_random_pct_min_max(segment["contactLandlineActive_categories"])
        contactLandlineActive_recode = contactLandlineActive["name"]
    else :
        contactLandlineActive_recode="0"

    return contactLandlineActive_recode
def pick_contactMobileActive(i, segment,flagContactAbilityMobileCall):
    if flagContactAbilityMobileCall["name"]== "1":
        contactMobileActive = pick_random_pct_min_max(segment["contactMobileActive_categories"])
        contactMobileActive_recode = contactMobileActive["name"]
    else :
        contactMobileActive_recode="0"

    return contactMobileActive_recode
def pick_contactDirectMailActive(i, segment,flagContactAbilityDirectMail):
    if flagContactAbilityDirectMail["name"]== "1":
        contactDirectMailActive = pick_random_pct_min_max(segment["contactDirectMailActive_categories"])
        contactDirectMailActive_recode = contactDirectMailActive["name"]
    else :
        contactDirectMailActive_recode="0"

    return contactDirectMailActive_recode


def pick_contactEmailActive(i, segment,flagContactAbilityEmail):
    if flagContactAbilityEmail["name"]== "1":
        contactEmailActive = pick_random_pct_min_max(segment["contactEmailActive_categories"])
        contactEmailActive_recode = contactEmailActive["name"]
    else :
        contactEmailActive_recode="0"

    return contactEmailActive_recode
def pick_contactTwitterActive(i, segment,flagContactAbilityTwitter):
    if flagContactAbilityTwitter== "1":
        contactTwitterActive = pick_random_pct_min_max(segment["contactTwitterActive_categories"])
        contactTwitterActive_recode = contactTwitterActive["name"]
    else :
        contactTwitterActive_recode="0"

    return contactTwitterActive_recode
def pick_contactFacebookActive(i, segment,flagContactAbilityFaceBook):
    if flagContactAbilityFaceBook== "1":
        contactFacebookActive = pick_random_pct_min_max(segment["contactFacebookActive_categories"])
        contactFacebookActive_recode = contactFacebookActive["name"]
    else :
        contactFacebookActive_recode="0"

    return contactFacebookActive_recode
def pick_contactLinkedinActive(i, segment,flagContactAbilityLinkedIn):
    if flagContactAbilityLinkedIn== "1":
        contactLinkedinActive = pick_random_pct_min_max(segment["contactLinkedinActive_categories"])
        contactLinkedinActive_recode = contactLinkedinActive["name"]
    else :
        contactLinkedinActive_recode="0"

    return contactLinkedinActive_recode
def pick_contactInternetChatActive(i, segment,flagContactAbilityInternet):
    if flagContactAbilityInternet["name"]== "1":
        contactInternetChatActive = pick_random_pct_min_max(segment["contactInternetChatActive_categories"])
        contactInternetChatActive_recode = contactInternetChatActive["name"]
    else :
        contactInternetChatActive_recode="0"

    return contactInternetChatActive_recode
def pick_flagOptOut(i, segment):
    return pick_random_pct_min_max(segment["flagOptOut_categories"])
def pick_flagOptIn(i, segment,flagOptOut):
    if flagOptOut["name"]== "1":
        flagOptIn = "0"
    else :
        flagOptIn="1"

    return flagOptIn
def pick_flagDoNotCall(i, segment,flagContactAbilityLandline,flagContactAbilityMobileCall):
    if flagContactAbilityLandline["name"]== "1" or flagContactAbilityMobileCall["name"]== "1":
        flagDoNotCall = pick_random_pct_min_max(segment["flagDoNotCall_categories"])
        flagDoNotCall_recode = flagDoNotCall["name"]
    else :
        flagDoNotCall_recode="1"

    return flagDoNotCall_recode
def pick_flag3rdPartyOptOut(i, segment):
    return pick_random_pct_min_max(segment["flag3rdPartyOptOut_categories"])
def pick_flag3rdPartyOptIn(i, segment,flag3rdPartyOptOut):
    if flag3rdPartyOptOut["name"]== "0":
        flag3rdPartyOptIn = "1"
    else :
        flag3rdPartyOptIn="0"

    return flag3rdPartyOptIn

def pick_preferredchannel(i, segment):
    return pick_random_pct_min_max(segment["preferredChannel_categories"])

def pick_preferredCommunicationDevice(i, segment):
    return pick_random_pct_min_max(segment["preferredCommunicationDevice_categories"])

def pick_preferredContactChannel(i, segment):
    return pick_random_pct_min_max(segment["preferredContactChannel_categories"])

def pick_preferredContactDevice(i, segment):
    return pick_random_pct_min_max(segment["preferredContactDevice_categories"])

def pick_preferredInboundChannel(i, segment):
    return pick_random_pct_min_max(segment["preferredInboundChannel_categories"])

def pick_preferredchannellocation(i, segment, preferredChannel, isStudent, isRetired):
    if isStudent==0 and isRetired==0 and preferredChannel["name"]=="Branch":
        preferredchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredchannellocation_recode="Branch - " + str(preferredchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredChannel["name"]=="Mobile App":
        preferredchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredchannellocation_recode="Mobile App - " + str(preferredchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredChannel["name"]=="Call":
        preferredchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredchannellocation_recode="Call - " + str(preferredchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredChannel["name"]=="Web":
        preferredchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredchannellocation_recode="Web - " + str(preferredchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredChannel["name"]=="Email":
        preferredchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredchannellocation_recode="Email - " + str(preferredchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredChannel["name"]=="Online Chat":
        preferredchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredchannellocation_recode="Online Chat - " + str(preferredchannellocation["name"])
    elif (isStudent==1 or isRetired==1) and preferredChannel["name"]=="Branch":
        preferredchannellocation_recode="Branch - " + "Home"
    elif (isStudent==1 or isRetired==1) and preferredChannel["name"]=="Mobile App":
        preferredchannellocation_recode="Mobile App - " + "Home"
    elif (isStudent==1 or isRetired==1) and  preferredChannel["name"]=="Call":
        preferredchannellocation_recode="Call - " + "Home"
    elif (isStudent==1 or isRetired==1) and  preferredChannel["name"]=="Web":
        preferredchannellocation_recode="Web - " + "Home"
    elif (isStudent==1 or isRetired==1) and  preferredChannel["name"]=="Email":
        preferredchannellocation_recode="Email - " + "Home"
    elif (isStudent==1 or isRetired==1) and  preferredChannel["name"]=="Online Chat":
        preferredchannellocation_recode="Online Chat - " + "Home"
    else :
        preferredchannellocation_recode=""

    return preferredchannellocation_recode

def pick_preferredchanneltime(i, segment,preferredChannel):
    if preferredChannel["name"]=="Branch":
        preferredchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredchanneltime_recode="Branch - " + preferredchanneltime["name"]
    elif preferredChannel["name"]=="Mobile App":
        preferredchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredchanneltime_recode="Mobile App - " + preferredchanneltime["name"]
    elif preferredChannel["name"]=="Call":
        preferredchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredchanneltime_recode="Call - " + preferredchanneltime["name"]
    elif preferredChannel["name"]=="Web":
        preferredchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredchanneltime_recode="Web - " + preferredchanneltime["name"]
    elif preferredChannel["name"]=="Email":
        preferredchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredchanneltime_recode="Email - " + preferredchanneltime["name"]
    elif preferredChannel["name"]=="Online Chat":
        preferredchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredchanneltime_recode="Online Chat - " + preferredchanneltime["name"]
    else :
        preferredchanneltime_recode=""

    return preferredchanneltime_recode

def pick_preferredcommunicationdevicelocation(i, segment, preferredCommunicationDevice,isStudent,isRetired):
    if isStudent==0 and isRetired==0 and preferredCommunicationDevice["name"]=="Phone":
        preferredcommunicationdevicelocation=pick_random_pct_min_max(segment["location_categories"])
        preferredcommunicationdevicelocation_recode="Phone - " + str(preferredcommunicationdevicelocation["name"])
    elif isStudent==0 and isRetired==0 and preferredCommunicationDevice["name"]=="Tablet":
        preferredcommunicationdevicelocation=pick_random_pct_min_max(segment["location_categories"])
        preferredcommunicationdevicelocation_recode="Tablet - " + str(preferredcommunicationdevicelocation["name"])
    elif isStudent==0 and isRetired==0 and preferredCommunicationDevice["name"]=="Desktop":
        preferredcommunicationdevicelocation=pick_random_pct_min_max(segment["location_categories"])
        preferredcommunicationdevicelocation_recode="Desktop - " + str(preferredcommunicationdevicelocation["name"])
    elif isStudent==0 and isRetired==0 and preferredCommunicationDevice["name"]=="Atm":
        preferredcommunicationdevicelocation=pick_random_pct_min_max(segment["location_categories"])
        preferredcommunicationdevicelocation_recode="Atm - " + str(preferredcommunicationdevicelocation["name"])
    elif (isStudent==1 or isRetired==1) and preferredCommunicationDevice["name"]=="Phone":
        preferredcommunicationdevicelocation_recode="Phone - " + "Home"
    elif (isStudent==1 or isRetired==1) and preferredCommunicationDevice["name"]=="Tablet":
        preferredcommunicationdevicelocation_recode="Tablet - " + "Home"
    elif (isStudent==1 or isRetired==1) and preferredCommunicationDevice["name"]=="Desktop":
        preferredcommunicationdevicelocation_recode="Desktop - " + "Home"
    elif (isStudent==1 or isRetired==1) and preferredCommunicationDevice["name"]=="Atm":
        preferredcommunicationdevicelocation_recode="Atm - " + "Home"
    else :
        preferredcommunicationdevicelocation_recode=""

    return preferredcommunicationdevicelocation_recode

def pick_preferredcommunicationdevicetime(i, segment, preferredCommunicationDevice):
    if preferredCommunicationDevice["name"]=="Phone":
        preferredcommunicationdevicetime=pick_random_pct_min_max(segment["time_categories"])
        preferredcommunicationdevicetime_recode="Phone - " + str(preferredcommunicationdevicetime["name"])
    elif preferredCommunicationDevice["name"]=="Tablet":
        preferredcommunicationdevicetime=pick_random_pct_min_max(segment["time_categories"])
        preferredcommunicationdevicetime_recode="Tablet - " + str(preferredcommunicationdevicetime["name"])
    elif preferredCommunicationDevice["name"]=="Desktop":
        preferredcommunicationdevicetime=pick_random_pct_min_max(segment["time_categories"])
        preferredcommunicationdevicetime_recode="Desktop - " + str(preferredcommunicationdevicetime["name"])
    elif preferredCommunicationDevice["name"]=="Atm":
        preferredcommunicationdevicetime=pick_random_pct_min_max(segment["time_categories"])
        preferredcommunicationdevicetime_recode="Atm - " + str(preferredcommunicationdevicetime["name"])
    else :
        preferredcommunicationdevicetime_recode=""

    return preferredcommunicationdevicetime_recode

def pick_preferredinboundchannellocation(i, segment, preferredInboundChannel,isStudent,isRetired):
    if isStudent==0 and isRetired==0 and preferredInboundChannel["name"]=="Call":
        preferredinboundchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredinboundchannellocation_recode="Call - " + str(preferredinboundchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredInboundChannel["name"]=="Email":
        preferredinboundchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredinboundchannellocation_recode="Email - " + str(preferredinboundchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredInboundChannel["name"]=="Sms":
        preferredinboundchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredinboundchannellocation_recode="Sms - " + str(preferredinboundchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredInboundChannel["name"]=="Facebook":
        preferredinboundchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredinboundchannellocation_recode="Facebook - " + str(preferredinboundchannellocation["name"])
    elif isStudent==0 and isRetired==0 and preferredInboundChannel["name"]=="Twitter":
        preferredinboundchannellocation=pick_random_pct_min_max(segment["location_categories"])
        preferredinboundchannellocation_recode="Twitter - " + str(preferredinboundchannellocation["name"])
    elif (isStudent==1 or isRetired==1) and preferredInboundChannel["name"]=="Call":
        preferredinboundchannellocation_recode="Call - " + "Home"
    elif  (isStudent==1 or isRetired==1) and preferredInboundChannel["name"]=="Email":
        preferredinboundchannellocation_recode="Email - " + "Home"
    elif  (isStudent==1 or isRetired==1) and preferredInboundChannel["name"]=="Sms":
        preferredinboundchannellocation_recode="Sms - " + "Home"
    elif  (isStudent==1 or isRetired==1) and preferredInboundChannel["name"]=="Facebook":
        preferredinboundchannellocation_recode="Facebook - " + "Home"
    elif  (isStudent==1 or isRetired==1) and preferredInboundChannel["name"]=="Twitter":
        preferredinboundchannellocation_recode="Twitter - " + "Home"
    else :
        preferredinboundchannellocation_recode=""

    return preferredinboundchannellocation_recode

def pick_preferredinboundchanneltime(i, segment, preferredInboundChannel):
    if preferredInboundChannel["name"]=="Call":
        preferredinboundchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredinboundchanneltime_recode="Call - " + str(preferredinboundchanneltime["name"])
    elif preferredInboundChannel["name"]=="Email":
        preferredinboundchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredinboundchanneltime_recode="Email - " + str(preferredinboundchanneltime["name"])
    elif preferredInboundChannel["name"]=="Sms":
        preferredinboundchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredinboundchanneltime_recode="Sms - " + str(preferredinboundchanneltime["name"])
    elif preferredInboundChannel["name"]=="Facebook":
        preferredinboundchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredinboundchanneltime_recode="Facebook - " + str(preferredinboundchanneltime["name"])
    elif preferredInboundChannel["name"]=="Twitter":
        preferredinboundchanneltime=pick_random_pct_min_max(segment["time_categories"])
        preferredinboundchanneltime_recode="Twitter - " + str(preferredinboundchanneltime["name"])
    else :
        preferredinboundchanneltime_recode=""

    return preferredinboundchanneltime_recode

def pick_isawareBrand(i, segment):
    return pick_random_pct_min_max(segment["awareBrand_categories"])

def pick_isInterested(i, segment,awareBrand):
    if awareBrand["name"]=="1" :
        isInterested=pick_random_pct_min_max(segment["interested_categories"])
        isInterested_recode=isInterested["name"]
    else :
        isInterested_recode="0"

    return isInterested_recode

def pick_isConsidering(i, segment,awareBrand,isInterested):
    if awareBrand["name"]=="1" and isInterested=="1":
        isConsidering=pick_random_pct_min_max(segment["considering_categories"])
        isConsidering_recode=isConsidering["name"]
    else :
        isConsidering_recode="0"

    return isConsidering_recode

def pick_hasPurchased(i, segment,awareBrand):
    if awareBrand["name"]=="1" :
        hasPurchased=pick_random_pct_min_max(segment["purchased_categories"])
        hasPurchased_recode=hasPurchased["name"]
    else :
        hasPurchased_recode="0"

    return hasPurchased_recode

def pick_hasChairmanRole(i, segment,isStudent,isRetired,age):
    if isStudent==0 and isRetired==0 and age>=40 :
        hasChairmanRole=pick_random_pct_min_max(segment["chairman_categories"])
        hasChairmanRole_recode=hasChairmanRole["name"]
    else :
        hasChairmanRole_recode="0"
    return hasChairmanRole_recode

def pick_hasBoardRole(i, segment,isStudent,isRetired,age):
    if isStudent==0 and isRetired==0 and age>=40 :
        hasBoardRole=pick_random_pct_min_max(segment["boardman_categories"])
        hasBoardRole_recode=hasBoardRole["name"]
    else :
        hasBoardRole_recode="0"
    return hasBoardRole_recode

def pick_firstProfJob(i, segment,isStudent,age):
    if isStudent==0 and age>=18 and age<=25 :
        firstProfJob=pick_random_pct_min_max(segment["firstjob_categories"])
        firstProfJob_recode=firstProfJob["name"]
    else :
        firstProfJob_recode="0"
    return firstProfJob_recode

def pick_isJobHunting(i, segment, isStudent, isRetired):
    if isStudent==0 and isRetired==0 :
        JobHunting=pick_random_pct_min_max(segment["jobhunting_categories"])
        JobHunting_recode=JobHunting["name"]
    else :
        JobHunting_recode="0"
    return JobHunting_recode

def pick_isLeavingNest(i, segment, isStudent, age):
    if isStudent==0 and age>=18 and age<=24 :
        LeavingNest=pick_random_pct_min_max(segment["leavingnest_categories"])
        LeavingNest_recode=LeavingNest["name"]
    else :
        LeavingNest_recode="0"
    return LeavingNest_recode

def pick_nbrTimesMoved(i, segment, flagLeavingNest):
    if flagLeavingNest=="0" :
        nbrTimesMoved=pick_random_pct_min_max(segment["nbrtimesmoved_categories"])
        nbrTimesMoved_recode=nbrTimesMoved["name"]
    else :
        nbrTimesMoved_recode="0"
    return nbrTimesMoved_recode

def pick_isRecentRetirement(i, segment, isRetired, age):
    if isRetired==1 and age>=50 and age<=67 :
        RecentRetirement=pick_random_pct_min_max(segment["recentretirement_categories"])
        RecentRetirement_recode=RecentRetirement["name"]
    else :
        RecentRetirement_recode="0"
    return RecentRetirement_recode

def pick_residenceCountryBirth(i, segment):
    return pick_random_pct_min_max(segment["residencecountrybirth_categories"])

def pick_onlineBuyMoment(i, segment):
    return pick_random_pct_min_max(segment["onlineBuyMoment_categories"])

def pick_att2Competition(i, segment):
    return pick_random_pct_min_max(segment["att2Competition_categories"])

def pick_competitivePricing(i, segment):
    return pick_random_pct_min_max(segment["competitivePricing_categories"])

def pick_locationWork(i, segment, isStudent, isRetired):
    if isStudent==0 and isRetired==0 :
        locationWork=pick_random_pct_min_max(segment["locationWork_categories"])
        locationWork_recode=locationWork["name"]
    else :
        locationWork_recode="Not at work"
    return locationWork_recode

def pick_jobSector(i, segment, isStudent, isRetired):
    if isStudent==0 and isRetired==0 :
        jobSector=pick_random_pct_min_max(segment["jobSector_categories"])
        jobSector_recode=jobSector["name"]
    else :
        jobSector_recode="Not at work"
    return jobSector_recode

def pick_onlineBuyDevice(i, segment):
    return pick_random_pct_min_max(segment["onlineBuyDevice_categories"])

def pick_consumptionDevice(i, segment):
    return pick_random_pct_min_max(segment["consumptionDevice_categories"])

def pick_consumptionLocation(i, segment, isStudent, isRetired):
    if isStudent==0 and isRetired==0 :
        consumptionLocation=pick_random_pct_min_max(segment["consumptionLocation_categories"])
        consumptionLocation_recode=consumptionLocation["name"]
    else :
        consumptionLocation_recode="Home"
    return consumptionLocation_recode

def pick_onlineBuyLocation(i, segment):
    return pick_random_pct_min_max(segment["onlineBuyLocation_categories"])

def pick_hasMobileApp(i, segment):
    return pick_random_pct_min_max(segment["hasMobileApp"])


def pick_regMobileApp(i,segment, hasMobileApp):
    if hasMobileApp["name"]=="1":
        regMobileApp=pick_random_pct_min_max(segment["regMobileApp"])
        regMobileApp_recode=regMobileApp["name"]
    else :
        regMobileApp_recode="0"
    return regMobileApp_recode

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

def pick_flagEmployed(i, segment,isStudent,isRetired):
    if isStudent==0 and isRetired==0 :
        flagEmployed=pick_random_pct_min_max(segment["flagEmployed_categories"])
        flagEmployed_recode=flagEmployed["name"]
    else :
        flagEmployed_recode="0"
    return flagEmployed_recode

def pick_socialClassInd(i, segment):
    return pick_random_pct_min_max(segment["socialClassInd_categories"])

def pick_cohort(i, segment):
    return pick_random_pct_min_max(segment["cohort_categories"])

def pick_residenceType(i, segment):
    return pick_random_pct_min_max(segment["residenceType_categories"])

def pick_activityLevel(i, segment):
    return pick_random_pct_min_max(segment["activityLevel_categories"])

def pick_desContactFreq(i, segment):
    return pick_random_pct_min_max(segment["desContactFreq_categories"])

def pick_desContactTiming(i, segment):
    return pick_random_pct_min_max(segment["desContactTiming_categories"])

def pick_contactChannelVariety(i, segment):
    return pick_random_pct_min_max(segment["contactChannelVariety_categories"])

def pick_totalRecRevenue(i, segment):
    return r.normal(segment["Random_totalRecRevenue"][0],segment["Random_totalRecRevenue"][1])

def pick_totalNonRecRevenue(i, segment):
    return r.normal(segment["Random_totalNonRecRevenue"][0],segment["Random_totalNonRecRevenue"][1])


def pick_proportionShareOfWallet(i, segment):
    propShareOfWallet=pick_random_pct_min_max(segment["proportionShareOfWallet_categories"])
    if propShareOfWallet["name"]=="0-25" :
        proportionShareOfWallet=r.randint(0,25)
    elif propShareOfWallet["name"]=="26-50" :
        proportionShareOfWallet=r.randint(26,50)
    elif propShareOfWallet["name"]=="51-75" :
        proportionShareOfWallet=r.randint(51,75)
    else :
        proportionShareOfWallet=r.randint(75,100)

    return proportionShareOfWallet

def pick_flagSelfEmployed(i, segment,flagEmployed):
    if flagEmployed=="1" :
        flagSelfEmployed=pick_random_pct_min_max(segment["flagSelfEmployed_categories"])
        flagSelfEmployed_recode=flagSelfEmployed["name"]
    else :
        flagSelfEmployed_recode="0"
    return flagSelfEmployed_recode

def pick_currentLocationTracking(i, segment):
    currentLocation= pick_random_pct_min_max(segment["currentLocationTracking_categories"])
    if (i == 3346 |i == 22639 ):
        currentLocation["name"]="1"
    return currentLocation

def pick_oldModelCategories(i, segment):
    return pick_random_pct_min_max(segment["oldModel_categories"])

def generate_oldModelProb_values(i,oldModel):
    if oldModel["name"]=="0-1%":
        oldModelProb_val=r.uniform(0,0.99)
    elif oldModel["name"]=="1-2%":
        oldModelProb_val=r.uniform(1.00,1.99)
    elif oldModel["name"]=="2-3%":
        oldModelProb_val=r.uniform(2.00,2.99)
    elif oldModel["name"]=="3-4%":
        oldModelProb_val=r.uniform(3.00,3.99)
    elif oldModel["name"]=="4-5%":
        oldModelProb_val=r.uniform(4.00,4.99)
    elif oldModel["name"]=="5-6%":
        oldModelProb_val=r.uniform(5.00,5.99)
    elif oldModel["name"]=="6-7%":
        oldModelProb_val=r.uniform(6.00,6.99)
    elif oldModel["name"]=="7-8%":
        oldModelProb_val=r.uniform(7.00,7.99)
    elif oldModel["name"]=="8-9%":
        oldModelProb_val=r.uniform(8.00,8.99)
    elif oldModel["name"]=="9-10%":
        oldModelProb_val=r.uniform(9,9.99)
    elif oldModel["name"]=="10-15%":
        oldModelProb_val=r.uniform(10,14.99)
    elif oldModel["name"]=="15-20%":
        oldModelProb_val=r.uniform(15.00,19.99)
    elif oldModel["name"]=="20-30%":
        oldModelProb_val=r.uniform(20.00,29.99)
    elif oldModel["name"]=="30-40%":
        oldModelProb_val=r.uniform(30.00,39.99)
    elif oldModel["name"]=="40-50%":
        oldModelProb_val=r.uniform(40.00,49.99)
    elif oldModel["name"]=="50-60%":
        oldModelProb_val=r.uniform(50.00,59.99)
    elif oldModel["name"]=="60-70%":
        oldModelProb_val=r.uniform(60.00,69.99)
    elif oldModel["name"]=="70-80%":
        oldModelProb_val=r.uniform(70.00,79.99)
    elif oldModel["name"]=="80-90%":
        oldModelProb_val=r.uniform(80.00,89.99)
    else :
        oldModelProb_val=r.uniform(90.00,99.99)
    return oldModelProb_val

def pick_newModelCategories(i, segment):
    return pick_random_pct_min_max(segment["newModel_categories"])

def generate_newModelProb_values(i,newModel):
    if newModel["name"]=="0-1%":
        newModelProb_val=r.uniform(0,0.99)
    elif newModel["name"]=="1-2%":
        newModelProb_val=r.uniform(1.00,1.99)
    elif newModel["name"]=="2-3%":
        newModelProb_val=r.uniform(2.00,2.99)
    elif newModel["name"]=="3-4%":
        newModelProb_val=r.uniform(3.00,3.99)
    elif newModel["name"]=="4-5%":
        newModelProb_val=r.uniform(4.00,4.99)
    elif newModel["name"]=="5-6%":
        newModelProb_val=r.uniform(5.00,5.99)
    elif newModel["name"]=="6-7%":
        newModelProb_val=r.uniform(6.00,6.99)
    elif newModel["name"]=="7-8%":
        newModelProb_val=r.uniform(7.00,7.99)
    elif newModel["name"]=="8-9%":
        newModelProb_val=r.uniform(8.00,8.99)
    elif newModel["name"]=="9-10%":
        newModelProb_val=r.uniform(9,9.99)
    elif newModel["name"]=="10-15%":
        newModelProb_val=r.uniform(10,14.99)
    elif newModel["name"]=="15-20%":
        newModelProb_val=r.uniform(15.00,19.99)
    elif newModel["name"]=="20-30%":
        newModelProb_val=r.uniform(20.00,29.99)
    elif newModel["name"]=="30-40%":
        newModelProb_val=r.uniform(30.00,39.99)
    elif newModel["name"]=="40-50%":
        newModelProb_val=r.uniform(40.00,49.99)
    elif newModel["name"]=="50-60%":
        newModelProb_val=r.uniform(50.00,59.99)
    elif newModel["name"]=="60-70%":
        newModelProb_val=r.uniform(60.00,69.99)
    elif newModel["name"]=="70-80%":
        newModelProb_val=r.uniform(70.00,79.99)
    elif newModel["name"]=="80-90%":
        newModelProb_val=r.uniform(80.00,89.99)
    else :
        newModelProb_val=r.uniform(90.00,99.99)
    return newModelProb_val

def pick_bannerCategories(i, segment):
    return pick_random_pct_min_max(segment["postCampaign_categories"])

def pick_bannerClicks(i, postCampaignBannerCat):
    return pick_random_pct_min_max(postCampaignBannerCat["clicks"])

def pick_salesCarLoan(i, postCampaignBannerCat):
    return pick_random_pct_min_max(postCampaignBannerCat["sales"])

def pick_salesChannel(i, postCampaignBannerCat,carLoanSale):
    if carLoanSale["name"]=="1":
        sales_channel_carLoan=pick_random_pct_min_max(postCampaignBannerCat["sales_channel"])
        sales_channel_carLoan_recode=sales_channel_carLoan["name"]
    else :
        sales_channel_carLoan_recode="no sale"
    return sales_channel_carLoan_recode

def pick_carLoanSim(i, postCampaignBannerCat,carLoanSale):
    if carLoanSale["name"]=="1":
        simulations=pick_random_pct_min_max(postCampaignBannerCat["simulations_sale"])
        simulations_recode=simulations["name"]
    elif carLoanSale["name"]=="0":
        simulations=pick_random_pct_min_max(postCampaignBannerCat["simulations_nosale"])
        simulations_recode=simulations["name"]
    else :
        simulations_recode="0"
    return simulations_recode

def pick_random_pct_min_max(array):
    #    random= r.rand()
    random= r.uniform(size=1)

    for i in range(len(array)):
        if random > array[i]["pct_min"] and random <= array[i]["pct_max"]:
            return array[i]

def generateDistribution(function):
    x = r.rand()
    y = function(x)
    if r.rand() <= y:
        return x
    return generateDistribution(function)

def write_header_to_filter(file_to_filter):
    file_to_filter.write('id;segment;segnr;age_category;age;Occupation;lifestage;flagStudent;flagRetired;education;maritalStatus;monthlyIncome;monthlyIncomeReal;nbrChildren;mainNationality;primaryLanguage;flagEmployed;flagSelfEmployed;')
    file_to_filter.write('houseOwner;homeTenant;flagValueProperty;nbrPropertiesOwned;flagLandLord;flagWealthyRegion;socialClassInd;residenceType;')
    file_to_filter.write('shareOfWallet;shareOfWalletHoldings;shareOfWalletSize;totalBankProducts;flagPFSP;cohort;activityLevel;proportionShareOfWallet;')
    file_to_filter.write('flagCheckingsAccount;flagCreditCard;flagPayment;flagSavingsAccount;flagInvestmentAccount;')
    file_to_filter.write('flagMutualFunds;flagBonds;flagAnnuities;flagStocks;flagOptions;')
    file_to_filter.write('flagRetirementAccount;flagLifeInsurance;flagPersonalLoan;flagMortgage;flagHomeEquityLoan;')
    file_to_filter.write('flagCarLoan;startdate_flagCarLoan;flagLoan;totalActiveProducts;')
    file_to_filter.write('totalReferrals;satisfaction;scoreChurn;flagOnlineBanking;flagOnlineBillPayment;flagMobilePayment;flagReloadablePrepaidCards;')
    file_to_filter.write('totalAssets;totalRecRevenue;totalNonRecRevenue;flagDebtCollection;')
    file_to_filter.write('affNightLife;affSport;affHealthFitness;affOutdoor;affLuxuryShopper;affMovie;affPetLovers;affFastFood;affValueShopper;affTechnophiles;affGreenLiving;affMusic;')
    file_to_filter.write('affFoodies;affCooking;affShutterbugs;affSavvyParents;affDIY;affAuto;affFashionistas;affBeautyMavens;affHomeDecor;affPolitical;affAvidInvestor;affThrillSeeker;')
    file_to_filter.write('affBargainHunter;affTravelBuff;affLuxuryTravel;affFamilyVacation;affBeachTravel;affWinterTravel;affNewsJunky;affArtTheater;affGamer;affTV;')
    file_to_filter.write('flagContactAbilityLandline;flagContactAbilityMobileCall;flagContactAbilityEmail;flagContactAbilityMobileTxt;flagContactAbilityDirectMail;flagContactAbilityInternet;')
    file_to_filter.write('flagContactAbilityTwitter;flagContactAbilityFaceBook;flagContactAbilityLinkedIn;contactLandlineActive;contactMobileActive;contactDirectMailActive;contactEmailActive;')
    file_to_filter.write('contactTwitterActive;contactFacebookActive;contactLinkedinActive;contactInternetChatActive;flagOptOut;flagOptIn;flagDoNotCall;flag3rdPartyOptOut;flag3rdPartyOptIn;')
    file_to_filter.write('preferredChannel;preferredChannelByLocation;preferredChannelByTime;preferredCommunicationDevice;preferredCommunicationDeviceByLocation;preferredCommunicationDeviceByTime;preferredContactChannel;preferredContactDevice;preferredInboundChannel;preferredInboundChannelByLocation;preferredInboundChannelByTime;locationWork;onlineBuyDevice;consumptionDevice;consumptionLocation;onlineBuyLocation;jobSector;desContactFreq;desContactTiming;contactChannelVariety;')
    file_to_filter.write('awareBrand;interested;considering;purchased;onlineBuyMoment;att2Competition;competitivePricing;')
    file_to_filter.write('flagChairmanRoles;flagBoardRoles;flagFirstProfJob;flagJobHunting;flagLeavingNest;nbrTimesMoved;flagRecentRetirement;flagResidenceBirth;')
    file_to_filter.write('hasMobileApp;regMobileApp;')
    file_to_filter.write('gender;title;first_name;middle_name;last_name;street_address;res_city;state;zipcode;res_country;email_address;phone_number;city_population;city_density;')
    file_to_filter.write('currentLocationTracking;oldModelProb_cat;oldModelProb_val;newModelProb_cat;newModelProb_val;postCampaignBanners;bannersDisplay;bannersClick;carLoanSale;carLoanSaleChannel;carLoanSim;carLoanStartDatePost\n')

def write_header_to_load(file_to_load):
    file_to_load.write('id;segment;segnr;age_category;age;Occupation;lifestage;flag_Student;flag_Retired;education;marital_Status;monthly_Income;monthly_Income_Real;nbr_Children;main_Nationality;primary_Language;flag_Employed;flag_Self_Employed;')
    file_to_load.write('flag_House_Owner;flag_Home_Tenant;flag_Value_Property;nbr_Properties_Owned;flag_LandLord;flag_Wealthy_Region;social_Class_Ind;residence_Type;')
    file_to_load.write('share_Of_Wallet;share_Of_Wallet_Holdings;share_Of_Wallet_Size;total_Bank_Products;flag_PFSP;cohort;activity_Level;proportion_Share_Of_Wallet;')
    file_to_load.write('satisfaction;flag_Online_Banking;flag_Online_Bill_Payment;flag_Mobile_Payment;flag_Reloadable_Prepaid_Cards;')
    file_to_load.write('total_Assets;total_Rec_Revenue;total_Non_Rec_Revenue;flag_Debt_Collection;')
    file_to_load.write('aff_Night_Life;aff_Sport;aff_Health_Fitness;aff_Outdoor;aff_Luxury_Shopper;aff_Movie;aff_Pet_Lovers;aff_Fast_Food;aff_Value_Shopper;aff_Technophiles;aff_Green_Living;aff_Music;')
    file_to_load.write('aff_Foodies;aff_Cooking;aff_Shutterbugs;aff_Savvy_Parents;aff_DIY;aff_Auto;aff_Fashionistas;aff_Beauty_Mavens;aff_Home_Decor;aff_Political;aff_Avid_Investor;aff_Thrill_Seeker;')
    file_to_load.write('aff_Bargain_Hunter;aff_Travel_Buff;aff_Luxury_Travel;aff_Family_Vacation;aff_Beach_Travel;aff_Winter_Travel;aff_News_Junky;aff_Art_Theater;aff_Gamer;aff_TV;')
    file_to_load.write('flag_Contact_Ability_Landline;flag_Contact_Ability_Mobile_Call;flag_Contact_Ability_Email;flag_Contact_Ability_Mobile_Txt;flag_Contact_Ability_Direct_Mail;flag_Contact_Ability_Internet;')
    file_to_load.write('flag_Contact_Ability_Twitter;flag_Contact_Ability_Face_Book;flag_Contact_Ability_Linked_In;contact_Landline_Active;contact_Mobile_Active;contact_Direct_Mail_Active;contact_Email_Active;')
    file_to_load.write('contact_Twitter_Active;contact_Facebook_Active;contact_Linkedin_Active;contact_Internet_Chat_Active;flag_Opt_Out;flag_Opt_In;flag_Do_Not_Call;flag_3_rd_Party_Opt_Out;flag_3_rd_Party_Opt_In;')

    file_to_load.write('preferred_Channel;preferred_Channel_By_Location;preferred_Channel_By_Time_of_day;preferred_Device;preferred_Device_By_Location;preferred_Device_By_Time_of_day;pref_Contact_Channel;pref_Contact_Device;pref_Inbound_Channel;pref_Inbound_Location;pref_Inbound_Timing;location_Work;online_Buy_Device;consumption_Device;consumption_Location;online_Buy_Location;job_Sector;des_Contact_Freq;des_Contact_Timing;contact_Channel_Variety;')
    file_to_load.write('aware_Brand;interested;considering;purchased;online_Buy_Moment;att_2_Competition;competitive_Pricing;')
    file_to_load.write('flag_Chairman_Roles;flag_Board_Roles;flag_First_Prof_Job;flag_Job_Hunting;flag_Leaving_Nest;nbr_Times_Moved;flag_Recent_Retirement;flag_Residence_country_Birth;')
    file_to_load.write('gender;title;first_name;middle_name;last_name;street_address;res_city;state;zipcode;res_country;email_address;phone_number;city_population;city_density\n')
#    file_to_load.write('gender;title;first_name;middle_name;last_name;street_address;res_city;state;zipcode;res_country;email_address;phone_number;city_population;city_density;')
#    file_to_load.write('oldmodel_Probabilities;newmodel_Probabilities;post_Campaign_Banner_Categories\n')

def write_affinities_info(file_to_filter, file_to_load,id, segment):
    affNightLife = pick_affNightLife(id, segment)
    affSport = pick_affSport(id, segment)
    affHealthFitness = pick_affHealthFitness(id, segment)
    affOutdoor = pick_affOutdoor(id, segment)
    affLuxuryShopper = pick_affLuxuryShopper(id, segment)
    affMovie = pick_affMovie(id, segment)
    affPetLovers = pick_affPetLovers(id, segment)
    affFastFood = pick_affFastFood(id, segment)
    affValueShopper = pick_affValueShopper(id, segment)
    affTechnophiles = pick_affTechnophiles(id, segment)
    affGreenLiving = pick_affGreenLiving(id, segment)
    affMusic = pick_affMusic(id, segment)
    file_to_filter.write("%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;" % (
        affNightLife, affSport, affHealthFitness, affOutdoor, affLuxuryShopper, affMovie, affPetLovers, affFastFood,
        affValueShopper, affTechnophiles, affGreenLiving, affMusic))

    file_to_load.write("%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;" % (
        affNightLife, affSport, affHealthFitness, affOutdoor, affLuxuryShopper, affMovie, affPetLovers, affFastFood,
        affValueShopper, affTechnophiles, affGreenLiving, affMusic))

def write_affinities_info2(file_to_filter, file_to_load,id, segment):
    affFoodies = pick_affFoodies(id, segment)
    affCooking = pick_affCooking(id, segment)
    affShutterbugs = pick_affShutterbugs(id, segment)
    affSavvyParents = pick_affSavvyParents(id, segment)
    affDIY = pick_affDIY(id, segment)
    affAuto = pick_affAuto(id, segment)
    affFashionistas = pick_affFashionistas(id, segment)
    affBeautyMavens = pick_affBeautyMavens(id, segment)
    affHomeDecor = pick_affHomeDecor(id, segment)
    affPolitical = pick_affPolitical(id, segment)
    affAvidInvestor = pick_affAvidInvestor(id, segment)
    affThrillSeeker = pick_affThrillSeeker(id, segment)
    affBargainHunter = pick_affBargainHunter(id, segment)
    affTravelBuff = pick_affTravelBuff(id, segment)
    affLuxuryTravel = pick_affLuxuryTravel(id, segment)
    affFamilyVacation = pick_affFamilyVacation(id, segment)
    affBeachTravel = pick_affBeachTravel(id, segment)
    affWinterTravel = pick_affWinterTravel(id, segment)
    affNewsJunky = pick_affNewsJunky(id, segment)
    affArtTheater = pick_affArtTheater(id, segment)
    affGamer = pick_affGamer(id, segment)
    affTV = pick_affTV(id, segment)
    file_to_filter.write("%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;" % (
        affFoodies,affCooking,affShutterbugs,affSavvyParents,affDIY,affAuto,affFashionistas,affBeautyMavens,
        affHomeDecor,affPolitical,affAvidInvestor,affThrillSeeker,affBargainHunter,affTravelBuff,affLuxuryTravel,
        affFamilyVacation,affBeachTravel,affWinterTravel,affNewsJunky,affArtTheater,affGamer,affTV))

    file_to_load.write("%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;" % (
        affFoodies,affCooking,affShutterbugs,affSavvyParents,affDIY,affAuto,affFashionistas,affBeautyMavens,
        affHomeDecor,affPolitical,affAvidInvestor,affThrillSeeker,affBargainHunter,affTravelBuff,affLuxuryTravel,
        affFamilyVacation,affBeachTravel,affWinterTravel,affNewsJunky,affArtTheater,affGamer,affTV))

def write_bank_assets_info(file_to_filter,file_to_load, id, segment):
    totalAssets = pick_totalAssets(id, segment)
    totalRecRevenue=pick_totalRecRevenue(id,segment)
    totalNonRecRevenue=pick_totalNonRecRevenue(id,segment)
    flagDebtCollection = pick_flagDebtCollection(id, segment,totalAssets)

    file_to_filter.write("%7.0f;%7.1f;%7.1f;%s;" % (totalAssets,totalRecRevenue,totalNonRecRevenue,flagDebtCollection))
    file_to_load.write("%7.0f;%7.1f;%7.1f;%s;" % (totalAssets,totalRecRevenue,totalNonRecRevenue,flagDebtCollection))
    
def write_bank_customer_info(file_to_filter,file_to_load, id, segment):
    totalReferrals = pick_totalReferrals(id, segment)
    satisfaction = pick_satisfaction(id, segment)
    churnScore = pick_churnScore(id, segment)
    flagOnlineBanking = pick_flagOnlineBanking(id, segment)
    flagOnlineBillPayment = pick_flagOnlineBillPayment(id, segment)
    flagMobilePayment = pick_flagMobilePayment(id, segment)
    flagReloadablePrepaidCards = pick_flagReloadablePrepaidCards(id, segment)
    file_to_filter.write("%1.0f;%5.2f;%5.2f;%s;%s;%s;%s;" % (
        totalReferrals, satisfaction, churnScore, flagOnlineBanking["name"], flagOnlineBillPayment["name"],
        flagMobilePayment["name"], flagReloadablePrepaidCards["name"])
    )
    file_to_load.write("%5.2f;%s;%s;%s;%s;" % (
        satisfaction, flagOnlineBanking["name"], flagOnlineBillPayment["name"],
        flagMobilePayment["name"], flagReloadablePrepaidCards["name"])
    )


def write_bank_loan_info(file_to_filter, id, segment):
    flagCarLoan = pick_flagCarLoan(id, segment)
    startdate_flagCarLoanpreCampaign=pick_startdate_flagCarLoanpreCampaign(id,segment,flagCarLoan)
    flagLoan = pick_flagLoan(id, segment)
    totalActiveProducts = pick_totalActiveProducts(id, segment)
    file_to_filter.write("%s;%s;%s;%2.0f;" % (flagCarLoan["name"],startdate_flagCarLoanpreCampaign, flagLoan["name"], totalActiveProducts))


def write_bank_savings_info(file_to_filter, id, segment):
    flagRetirementAccount = pick_flagRetirementAccount(id, segment)
    flagLifeInsurance = pick_flagLifeInsurance(id, segment)
    flagPersonalLoan = pick_flagPersonalLoan(id, segment)
    flagMortgage = pick_flagMortgage(id, segment)
    flagHomeEquityLoan = pick_flagHomeEquityLoan(id, segment)
    file_to_filter.write("%s;%s;%s;%s;%s;" % (
        flagRetirementAccount["name"], flagLifeInsurance["name"], flagPersonalLoan["name"], flagMortgage["name"],
        flagHomeEquityLoan["name"])
    )


def write_bank_investments_info(file_to_filter, id, segment):
    flagMutualFunds = pick_flagMutualFunds(id, segment)
    flagBonds = pick_flagBonds(id, segment)
    flagAnnuities = pick_flagAnnuities(id, segment)
    flagStocks = pick_flagStocks(id, segment)
    flagOptions = pick_flagOptions(id, segment)
    file_to_filter.write("%s;%s;%s;%s;%s;" % (
        flagMutualFunds["name"], flagBonds["name"], flagAnnuities["name"], flagStocks["name"], flagOptions["name"])
    )


def write_bank_accounts_info(file_to_filter, id, segment):
    flagCheckingsAccount = pick_flagCheckingsAccount(id, segment)
    flagCreditCard = pick_flagCreditCard(id, segment)
    flagPayment = pick_flagPayment(id, segment)
    flagSavingsAccount = pick_flagSavingsAccount(id, segment)
    flagInvestmentAccount = pick_flagInvestmentAccount(id, segment)
    file_to_filter.write("%s;%s;%s;%s;%s;" % (
        flagCheckingsAccount["name"], flagCreditCard["name"], flagPayment["name"], flagSavingsAccount["name"],
        flagInvestmentAccount["name"])
    )


def write_bank_portfolio_info(file_to_filter,file_to_load, id, segment):
    shareOfWallet = pick_shareOfWallet(id, segment)
    shareOfWalletHoldings = pick_shareOfWalletHoldings(id, segment)
    shareOfWalletSize = pick_shareOfWalletSize(id, segment)
    totalBankProducts = pick_totalBankProducts(id, segment)
    flagPFSP = pick_flagPFSP(id, segment)
    cohort = pick_cohort(id, segment)
    activityLevel = pick_activityLevel(id, segment)
    proportionShareOfWallet = pick_proportionShareOfWallet(id, segment)

    file_to_filter.write("%5.2f;%10.2f;%6.2f;%d;%s;%s;%s;%s;" % (
        shareOfWallet, shareOfWalletHoldings, shareOfWalletSize, totalBankProducts, flagPFSP["name"],cohort["name"],activityLevel["name"],proportionShareOfWallet)
    )
    file_to_load.write("%5.2f;%10.2f;%6.2f;%d;%s;%s;%s;%s;" % (
        shareOfWallet, shareOfWalletHoldings, shareOfWalletSize, totalBankProducts, flagPFSP["name"],cohort["name"],activityLevel["name"],proportionShareOfWallet)
    )


def write_house_info(file_to_filter,file_to_load, id, segment):
    houseOwner = pick_houseOwner(id, segment)
    homeTenant = pick_homeTenant(id, segment, houseOwner)
    valueProperty = pick_valueProperty(id, segment)
    nbrPropertiesOwned = pick_nbrPropertiesOwned(id, segment, houseOwner)
    landLord = pick_landLord(id, segment, houseOwner)
    wealthyRegion = pick_wealthyRegion(id, segment)
    socialClassInd=pick_socialClassInd(id,segment)
    residenceType=pick_residenceType(id,segment)
    file_to_filter.write("%s;%s;%s;%s;%s;%s;%s;%s;" % (
        houseOwner["name"], homeTenant, valueProperty["name"], nbrPropertiesOwned, landLord, wealthyRegion["name"],socialClassInd["name"],residenceType["name"])
    )
    file_to_load.write("%s;%s;%s;%s;%s;%s;%s;%s;" % (
        houseOwner["name"], homeTenant, valueProperty["name"], nbrPropertiesOwned, landLord, wealthyRegion["name"],socialClassInd["name"],residenceType["name"])
    )


def write_crm_info(file_to_filter,file_to_load, id, segment):
    age_category = pick_age_category(id, segment)
    age = pick_age(id, age_category)
    occupation = pick_occupation(id, segment)
    lifestage = pick_lifestage(id, segment)
    isStudent = pick_isStudent(id, segment, age)
    isRetired = pick_isRetired(id, segment, age)
    education = pick_education(id, segment)
    maritalstatus = pick_maritalStatus(id, segment)
    monthlyincome = pick_monthlyIncome(id, segment)
    nbrChildren = pick_nbrChildren(id, segment)
    mainNationality = pick_mainNationality(id, segment)
    mainLanguage = pick_mainLanguage(id, segment)
    flagEmployed = pick_flagEmployed(id, segment,isStudent,isRetired)
    flagSelfEmployed = pick_flagSelfEmployed(id, segment,flagEmployed)


    file_to_filter.write("%s;%s;%s;%s;%d;%s;%s;%s;%s;%s;%s;%7.2f;%7.2f;%s;%s;%s;%s;%s;" % (
        id, segment["name"], segment["segnr"], age_category["name"], age, occupation["name"], lifestage["name"], isStudent,
        isRetired, education["name"], maritalstatus["name"], monthlyincome, monthlyincome, nbrChildren["name"], mainNationality["name"], mainLanguage["name"],flagEmployed,flagSelfEmployed)
    )
    file_to_load.write("%s;%s;%s;%s;%2.0f;%s;%s;%s;%s;%s;%s;%7.2f;%7.2f;%s;%s;%s;%s;%s;" % (
        id, segment["name"], segment["segnr"], age_category["name"], age, occupation["name"], lifestage["name"], isStudent,
        isRetired, education["name"], maritalstatus["name"], monthlyincome, monthlyincome, nbrChildren["name"], mainNationality["name"], mainLanguage["name"],flagEmployed,flagSelfEmployed)
    )

    return {'is_student' : isStudent, 'is_retired' : isRetired, 'age' : age}

def write_contact_ability(file_to_filter,file_to_load, id, segment):
    flagContactAbilityLandline=pick_flagContactAbilityLandline(id,segment)
    flagContactAbilityMobileCall=pick_flagContactAbilityMobileCall(id,segment)
    flagContactAbilityEmail=pick_flagContactAbilityEmail(id,segment)
    flagContactAbilityMobileTxt=pick_flagContactAbilityMobileTxt(id,segment,flagContactAbilityMobileCall)
    flagContactAbilityDirectMail=pick_flagContactAbilityDirectMail(id,segment)
    flagContactAbilityInternet=pick_flagContactAbilityInternet(id,segment)
    flagContactAbilityTwitter=pick_flagContactAbilityTwitter(id,segment,flagContactAbilityInternet)
    flagContactAbilityFaceBook=pick_flagContactAbilityFaceBook(id,segment,flagContactAbilityInternet)
    flagContactAbilityLinkedIn=pick_flagContactAbilityLinkedIn(id,segment,flagContactAbilityInternet)
    contactLandlineActive=pick_contactLandlineActive(id,segment,flagContactAbilityLandline)
    contactMobileActive=pick_contactMobileActive(id,segment,flagContactAbilityMobileCall)
    contactDirectMailActive=pick_contactDirectMailActive(id,segment,flagContactAbilityDirectMail)
    contactEmailActive=pick_contactEmailActive(id,segment,flagContactAbilityEmail)
    contactTwitterActive=pick_contactTwitterActive(id,segment,flagContactAbilityTwitter)
    contactFacebookActive=pick_contactFacebookActive(id,segment,flagContactAbilityFaceBook)
    contactLinkedinActive=pick_contactLinkedinActive(id,segment,flagContactAbilityLinkedIn)
    contactInternetChatActive=pick_contactInternetChatActive(id,segment,flagContactAbilityInternet)
    flagOptOut=pick_flagOptOut(id,segment)
    flagOptIn=pick_flagOptIn(id,segment,flagOptOut)
    flagDoNotCall=pick_flagDoNotCall(id,segment,flagContactAbilityLandline,flagContactAbilityMobileCall)
    flag3rdPartyOptOut=pick_flag3rdPartyOptOut(id,segment)
    flag3rdPartyOptIn=pick_flag3rdPartyOptIn(id,segment,flag3rdPartyOptOut)


    file_to_filter.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" % (
        flagContactAbilityLandline["name"],flagContactAbilityMobileCall["name"],flagContactAbilityEmail["name"],flagContactAbilityMobileTxt,
        flagContactAbilityDirectMail["name"],flagContactAbilityInternet["name"],flagContactAbilityTwitter,
        flagContactAbilityFaceBook,flagContactAbilityLinkedIn,contactLandlineActive,contactMobileActive,contactDirectMailActive,contactEmailActive,contactTwitterActive,contactFacebookActive,
        contactLinkedinActive,contactInternetChatActive,flagOptOut["name"],flagOptIn,flagDoNotCall,flag3rdPartyOptOut["name"],flag3rdPartyOptIn)
        )
    file_to_load.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" % (
        flagContactAbilityLandline["name"],flagContactAbilityMobileCall["name"],flagContactAbilityEmail["name"],flagContactAbilityMobileTxt,
        flagContactAbilityDirectMail["name"],flagContactAbilityInternet["name"],flagContactAbilityTwitter,
        flagContactAbilityFaceBook,flagContactAbilityLinkedIn,contactLandlineActive,contactMobileActive,contactDirectMailActive,contactEmailActive,contactTwitterActive,contactFacebookActive,
        contactLinkedinActive,contactInternetChatActive,flagOptOut["name"],flagOptIn,flagDoNotCall,flag3rdPartyOptOut["name"],flag3rdPartyOptIn)
        )

def write_preferredcommunication_info(file_to_filter,file_to_load, id, segment, is_student, is_retired):
    preferredChannel = pick_preferredchannel(id, segment)
    preferredChannelByLocation = pick_preferredchannellocation(id, segment, preferredChannel,is_student,is_retired)
    preferredChannelByTime = pick_preferredchanneltime(id, segment,preferredChannel)
    preferredCommunicationDevice = pick_preferredCommunicationDevice(id, segment)
    preferredCommunicationDeviceByLocation = pick_preferredcommunicationdevicelocation(id, segment,preferredCommunicationDevice,is_student,is_retired)
    preferredCommunicationDeviceByTime = pick_preferredcommunicationdevicetime(id, segment,preferredCommunicationDevice)
    preferredContactChannel = pick_preferredContactChannel(id, segment)
    preferredContactDevice = pick_preferredContactDevice(id, segment)
    preferredInboundChannel = pick_preferredInboundChannel(id, segment)
    preferredInboundChannelByLocation = pick_preferredinboundchannellocation(id, segment,preferredInboundChannel,is_student,is_retired)
    preferredInboundChannelByTime = pick_preferredinboundchanneltime(id, segment,preferredInboundChannel)
    locationWork=pick_locationWork(id, segment,is_student,is_retired)
    onlineBuyDevice=pick_onlineBuyDevice(id, segment)
    consumtionDevice=pick_consumptionDevice(id, segment)
    consumptionLocation=pick_consumptionLocation(id, segment,is_student,is_retired)
    onlineBuyLocation=pick_onlineBuyLocation(id, segment)
    jobSector=pick_jobSector(id, segment,is_student,is_retired)
    desContactFreq=pick_desContactFreq(id,segment)
    desContactTiming=pick_desContactTiming(id,segment)
    contactChannelVariety=pick_contactChannelVariety(id,segment)

    file_to_filter.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" % (
        preferredChannel["name"],preferredChannelByLocation,preferredChannelByTime,preferredCommunicationDevice["name"],preferredCommunicationDeviceByLocation,preferredCommunicationDeviceByTime,preferredContactChannel["name"],preferredContactDevice["name"],preferredInboundChannel["name"],preferredInboundChannelByLocation,preferredInboundChannelByTime,locationWork,onlineBuyDevice["name"],consumtionDevice["name"],consumptionLocation,onlineBuyLocation["name"],jobSector,desContactFreq["name"],desContactTiming["name"],contactChannelVariety["name"])
    )
    file_to_load.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" % (
        preferredChannel["name"],preferredChannelByLocation,preferredChannelByTime,preferredCommunicationDevice["name"],preferredCommunicationDeviceByLocation,preferredCommunicationDeviceByTime,preferredContactChannel["name"],preferredContactDevice["name"],preferredInboundChannel["name"],preferredInboundChannelByLocation,preferredInboundChannelByTime,locationWork,onlineBuyDevice["name"],consumtionDevice["name"],consumptionLocation,onlineBuyLocation["name"],jobSector,desContactFreq["name"],desContactTiming["name"],contactChannelVariety["name"])
    )

def write_brand_info(file_to_filter,file_to_load, id, segment):
    awareBrand = pick_isawareBrand(id, segment)
    interested = pick_isInterested(id, segment, awareBrand)
    considering = pick_isConsidering(id, segment,awareBrand,interested)
    purchased = pick_hasPurchased(id, segment,awareBrand)
    onlineBuyMoment= pick_onlineBuyMoment(id, segment)
    att2Competition= pick_att2Competition(id, segment)
    competitivePricing= pick_competitivePricing(id, segment)

    file_to_filter.write("%s;%s;%s;%s;%s;%s;%s;" % (
        awareBrand["name"],interested,considering,purchased,onlineBuyMoment["name"],att2Competition["name"],competitivePricing["name"])
    )
    file_to_load.write("%s;%s;%s;%s;%s;%s;%s;" % (
        awareBrand["name"],interested,considering,purchased,onlineBuyMoment["name"],att2Competition["name"],competitivePricing["name"])
    )

def write_lifemoments_info(file_to_filter,file_to_load, id, segment, is_student, is_retired, age):
    flagChairmanRoles=pick_hasChairmanRole(id, segment, is_student, is_retired, age)
    flagBoardRoles=pick_hasBoardRole(id, segment, is_student,is_retired, age)
    flagFirstProfJob=pick_firstProfJob(id, segment, is_student,age)
    flagJobHunting=pick_isJobHunting(id, segment, is_student, is_retired)
    flagLeavingNest=pick_isLeavingNest(id, segment, is_student, age)
    nrTimesMoved=pick_nbrTimesMoved(id, segment, flagLeavingNest)
    flagRecentRetirement=pick_isRecentRetirement(id, segment, is_retired, age)
    flagResidenceCountryBirth=pick_residenceCountryBirth(id, segment)
    file_to_filter.write("%s;%s;%s;%s;%s;%s;%s;%s;" % (
        flagChairmanRoles,flagBoardRoles,flagFirstProfJob,flagJobHunting,flagLeavingNest,nrTimesMoved,flagRecentRetirement,flagResidenceCountryBirth["name"])
    )
    file_to_load.write("%s;%s;%s;%s;%s;%s;%s;%s;" % (
        flagChairmanRoles,flagBoardRoles,flagFirstProfJob,flagJobHunting,flagLeavingNest,nrTimesMoved,flagRecentRetirement,flagResidenceCountryBirth["name"])
    )

def write_mobileapp_info(file_to_filter,file_to_load, id, segment):
    hasMobileApp = pick_hasMobileApp(id, segment)
    regMobileApp = pick_regMobileApp(id, segment,hasMobileApp)

    file_to_filter.write("%s;%s;" % (
        hasMobileApp["name"],regMobileApp)
                         )
def write_fakenames(file_to_filter,file_to_load, fakenames_df, id):
    if id<=50000 :
        gender = fakenames_df.ix[id-1,1]
        title = fakenames_df.ix[id-1,2]
        first_name = fakenames_df.ix[id-1,3]
        middle_name = fakenames_df.ix[id-1,4]
        last_name = fakenames_df.ix[id-1,5]
        street_address = fakenames_df.ix[id-1,6]
        res_city = fakenames_df.ix[id-1,7]
        state = fakenames_df.ix[id-1,8]
        zipcode = fakenames_df.ix[id-1,9]
        res_country = fakenames_df.ix[id-1,10]
        email_address = fakenames_df.ix[id-1,11]
        phone_number = fakenames_df.ix[id-1,12]
        city_population = fakenames_df.ix[id-1,13]
        city_density = fakenames_df.ix[id-1,14]

    else :
        T=int(id/50000)
        gender = fakenames_df.ix[id-(50000*T),1]
        title = fakenames_df.ix[id-(50000*T),2]
        first_name = fakenames_df.ix[id-(50000*T),3]
        middle_name = fakenames_df.ix[id-(50000*T),4]
        last_name = fakenames_df.ix[id-(50000*T),5]+str(T)
        street_address = fakenames_df.ix[id-(50000*T),6]
        res_city = fakenames_df.ix[id-(50000*T),7]
        state = fakenames_df.ix[id-(50000*T),8]
        zipcode = fakenames_df.ix[id-(50000*T),9]
        res_country = fakenames_df.ix[id-(50000*T),10]
        email_address = fakenames_df.ix[id-(50000*T),11]+str(T)
        phone_number = fakenames_df.ix[id-(50000*T),12]+str(T)
        city_population = fakenames_df.ix[id-1,13]
        city_density = fakenames_df.ix[id-1,14]
    file_to_filter.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" % (gender,title,first_name,middle_name,last_name,street_address,res_city,state,zipcode,res_country,email_address,phone_number,city_population,city_density))
#    file_to_load.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;" % (gender,title,first_name,middle_name,last_name,street_address,res_city,state,zipcode,res_country,email_address,phone_number,city_population,city_density))
    file_to_load.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (gender,title,first_name,middle_name,last_name,street_address,res_city,state,zipcode,res_country,email_address,phone_number,city_population,city_density))

def write_currentLocationTracking(file_to_filter, id, segment):
    currentLocationTracking=pick_currentLocationTracking(id, segment)
    file_to_filter.write("%s;" % (
        currentLocationTracking["name"]))

def write_model_info(file_to_filter,id, segment):
    oldmodel = pick_oldModelCategories(id, segment)
    oldmodel_prob = generate_oldModelProb_values(id, oldmodel)
    newmodel = pick_newModelCategories(id, segment)
    newmodel_prob = generate_newModelProb_values(id, newmodel)
    postCampaignBannerCat = pick_bannerCategories(id, segment)
    bannerClicks = pick_bannerClicks(id, postCampaignBannerCat)
    carLoanSale = pick_salesCarLoan(id, postCampaignBannerCat)
    carLoanSaleChannel = pick_salesChannel(id, postCampaignBannerCat,carLoanSale)
    carLoanSimulations = pick_carLoanSim(id, postCampaignBannerCat,carLoanSale)
    startdate_flagCarLoanpostCampaign=pick_startdate_flagCarLoanpostCampaign(id,segment,carLoanSale)

    file_to_filter.write("%s;%5.2f;%s;%5.2f;%s;%s;%s;%s;%s;%s;%s\n" % (oldmodel["name"],oldmodel_prob,newmodel["name"],newmodel_prob,postCampaignBannerCat["name"],postCampaignBannerCat["displays"],bannerClicks["name"],carLoanSale["name"],carLoanSaleChannel,carLoanSimulations,startdate_flagCarLoanpostCampaign))
#    file_to_load.write("%5.2f;%5.2f;%s\n" % (oldmodel_prob, newmodel_prob,postCampaignBannerCat["name"]))


def main_crm():
    segments = load(model_file('segments.json'))
    segment_crm_data = [
        load(model_file('segment_crm_1.json')),
        load(model_file('segment_crm_2.json')),
        load(model_file('segment_crm_3.json')),
        "",
        load(model_file('segment_crm_5.json')),
        load(model_file('segment_crm_6.json')),
        load(model_file('segment_crm_7.json'))
    ]

    fakenames_df = pd.read_csv(model_file('fakenames2.csv'), sep=',',header=None)
    with open(output_file('CrmDataToFilter.csv'), 'w') as file_out_to_filter, \
            open(output_file('CrmDataToLoad.csv'), 'w') as file_out_to_load, \
            open(output_file('CrmDataToLoad.hdr'), 'w') as file_hdr_to_load:
        write_header_to_filter(file_out_to_filter)
        write_header_to_load(file_hdr_to_load)

        pb = Bar('Generating', max=nr_records, fill='=', suffix='%(percent)d%%')
        for id in range(1, nr_records + 1):
            segment = pick_segment(id, segments, segment_crm_data)
#            print id,segment["segnr"]

            crm_info = write_crm_info(file_out_to_filter, file_out_to_load, id, segment)
            write_house_info(file_out_to_filter, file_out_to_load, id, segment)
            write_bank_portfolio_info(file_out_to_filter, file_out_to_load, id, segment)
            write_bank_accounts_info(file_out_to_filter, id, segment)
            write_bank_investments_info(file_out_to_filter, id, segment)
            write_bank_savings_info(file_out_to_filter, id, segment)
            write_bank_loan_info(file_out_to_filter, id, segment)
            write_bank_customer_info(file_out_to_filter, file_out_to_load, id, segment)
            write_bank_assets_info(file_out_to_filter, file_out_to_load, id, segment)
            write_affinities_info(file_out_to_filter, file_out_to_load, id, segment)
            write_affinities_info2(file_out_to_filter, file_out_to_load, id, segment)
            write_contact_ability(file_out_to_filter, file_out_to_load, id, segment)
            write_preferredcommunication_info(file_out_to_filter, file_out_to_load, id, segment,crm_info['is_student'],crm_info['is_retired'])
            write_brand_info(file_out_to_filter, file_out_to_load, id, segment)
            write_lifemoments_info(file_out_to_filter, file_out_to_load, id, segment,crm_info['is_student'],crm_info['is_retired'],crm_info['age'])
            write_mobileapp_info(file_out_to_filter, file_out_to_load, id,segment)
            write_fakenames(file_out_to_filter, file_out_to_load, fakenames_df, id)
            write_currentLocationTracking(file_out_to_filter, id,segment)
            write_model_info(file_out_to_filter, id,segment)
            pb.next()

if __name__ == "__main__":
    main_crm()