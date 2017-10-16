#!/usr/bin/python
import argparse
from progress.bar import Bar
import json
from numpy.random import seed
from numpy.random import RandomState
import pandas as pd
import random
import datetime
import radar

#TODO remove blank spaces when writing float values e.g. %10.2f
#TODO generate folder structure for target file if not exists

# globals
seedValue = 1234
seed(seed=seedValue)
r = RandomState(seedValue)

# Read command line args
parser = argparse.ArgumentParser(description='Generate customer randomisation CRM data for Lily demo environments.')
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

def pick_shareOfWallet(i, segment):
    return int(random.uniform(segment["Random_shareOfWallet"][0],segment["Random_shareOfWallet"][1]))

def pick_shareOfWalletHoldings(i, segment):
    return int(random.uniform(segment["Random_shareOfWalletHoldings"][0],segment["Random_shareOfWalletHoldings"][1]))

def pick_shareOfWalletSize(i, segment):
    return int(random.uniform(segment["Random_shareOfWalletSize"][0],segment["Random_shareOfWalletSize"][1]))

def pick_satisfaction(i, segment):
    return random.uniform(segment["Random_satisfaction"][0],segment["Random_satisfaction"][1])

def pick_churnScore(i, segment):
    return random.uniform(segment["Random_churnScore"][0], segment["Random_churnScore"][1])

def pick_totalAssets(i, segment):
    return int(random.uniform(segment["Random_totalAssets"][0],segment["Random_totalAssets"][1]))

def pick_affNightLife(i, segment):
    return int(random.uniform(segment["Random_affNightLife"][0],segment["Random_affNightLife"][1]))

def pick_affSport(i, segment):
    return int(random.uniform(segment["Random_affSport"][0],segment["Random_affSport"][1]))

def pick_affHealthFitness(i, segment):
    return int(random.uniform(segment["Random_affHealthFitness"][0],segment["Random_affHealthFitness"][1]))

def pick_affOutdoor(i, segment):
    return int(random.uniform(segment["Random_affOutdoor"][0],segment["Random_affOutdoor"][1]))

def pick_affLuxuryShopper(i, segment):
    return int(random.uniform(segment["Random_affLuxuryShopper"][0],segment["Random_affLuxuryShopper"][1]))

def pick_affMovie(i, segment):
    return int(random.uniform(segment["Random_affMovie"][0],segment["Random_affMovie"][1]))

def pick_affPetLovers(i, segment):
    return int(random.uniform(segment["Random_affPetLovers"][0],segment["Random_affPetLovers"][1]))

def pick_affFastFood(i, segment):
    return int(random.uniform(segment["Random_affFastFood"][0],segment["Random_affFastFood"][1]))

def pick_affValueShopper(i, segment):
    return int(random.uniform(segment["Random_affValueShopper"][0],segment["Random_affValueShopper"][1]))

def pick_affTechnophiles(i, segment):
    return int(random.uniform(segment["Random_affTechnophiles"][0],segment["Random_affTechnophiles"][1]))

def pick_affGreenLiving(i, segment):
    return int(random.uniform(segment["Random_affGreenLiving"][0],segment["Random_affGreenLiving"][1]))

def pick_affMusic(i, segment):
    return int(random.uniform(segment["Random_affMusic"][0],segment["Random_affMusic"][1]))

def pick_affFoodies(i, segment):
    return int(random.uniform(segment["Random_affFoodies"][0],segment["Random_affFoodies"][1]))

def pick_affCooking(i, segment):
    return int(random.uniform(segment["Random_affCooking"][0],segment["Random_affCooking"][1]))

def pick_affShutterbugs(i, segment):
    return int(random.uniform(segment["Random_affShutterbugs"][0],segment["Random_affShutterbugs"][1]))

def pick_affSavvyParents(i, segment):
    return int(random.uniform(segment["Random_affSavvyParents"][0],segment["Random_affSavvyParents"][1]))

def pick_affDIY(i, segment):
    return int(random.uniform(segment["Random_affDIY"][0],segment["Random_affDIY"][1]))

def pick_affAuto(i, segment):
    return int(random.uniform(segment["Random_affAuto"][0],segment["Random_affAuto"][1]))

def pick_affFashionistas(i, segment):
    return int(random.uniform(segment["Random_affFashionistas"][0],segment["Random_affFashionistas"][1]))

def pick_affBeautyMavens(i, segment):
    return int(random.uniform(segment["Random_affBeautyMavens"][0],segment["Random_affBeautyMavens"][1]))

def pick_affHomeDecor(i, segment):
    return int(random.uniform(segment["Random_affHomeDecor"][0],segment["Random_affHomeDecor"][1]))

def pick_affPolitical(i, segment):
    return int(random.uniform(segment["Random_affPolitical"][0],segment["Random_affPolitical"][1]))

def pick_affAvidInvestor(i, segment):
    return int(random.uniform(segment["Random_affAvidInvestor"][0],segment["Random_affAvidInvestor"][1]))

def pick_affThrillSeeker(i, segment):
    return int(random.uniform(segment["Random_affThrillSeeker"][0],segment["Random_affThrillSeeker"][1]))

def pick_affBargainHunter(i, segment):
    return int(random.uniform(segment["Random_affBargainHunter"][0],segment["Random_affBargainHunter"][1]))

def pick_affTravelBuff(i, segment):
    return int(random.uniform(segment["Random_affTravelBuff"][0],segment["Random_affTravelBuff"][1]))

def pick_affLuxuryTravel(i, segment):
    return int(random.uniform(segment["Random_affLuxuryTravel"][0],segment["Random_affLuxuryTravel"][1]))

def pick_affFamilyVacation(i, segment):
    return int(random.uniform(segment["Random_affFamilyVacation"][0],segment["Random_affFamilyVacation"][1]))

def pick_affBeachTravel(i, segment):
    return int(random.uniform(segment["Random_affBeachTravel"][0],segment["Random_affBeachTravel"][1]))

def pick_affWinterTravel(i, segment):
    return int(random.uniform(segment["Random_affWinterTravel"][0],segment["Random_affWinterTravel"][1]))

def pick_affNewsJunky(i, segment):
    return int(random.uniform(segment["Random_affNewsJunky"][0],segment["Random_affNewsJunky"][1]))

def pick_affArtTheater(i, segment):
    return int(random.uniform(segment["Random_affArtTheater"][0],segment["Random_affArtTheater"][1]))

def pick_affGamer(i, segment):
    return int(random.uniform(segment["Random_affGamer"][0],segment["Random_affGamer"][1]))

def pick_affTV(i, segment):
    return int(random.uniform(segment["Random_affTV"][0],segment["Random_affTV"][1]))

def pick_proportionShareOfWallet(i, segment):
    propShareOfWallet=pick_random_pct_min_max(segment["proportionShareOfWallet_categories"])
    if propShareOfWallet["name"]=="0-25" :
        proportionShareOfWallet=int(random.uniform(0,25))
    elif propShareOfWallet["name"]=="26-50" :
        proportionShareOfWallet=int(random.uniform(26,50))
    elif propShareOfWallet["name"]=="51-75" :
        proportionShareOfWallet=int(random.uniform(51,75))
    else :
        proportionShareOfWallet=int(random.uniform(75,100))

    return proportionShareOfWallet

def pick_random_pct_min_max(array):
    #    random= r.rand()
    random1= r.uniform(size=1)

    for i in range(len(array)):
        if random1 > array[i]["pct_min"] and random1 <= array[i]["pct_max"]:
            return array[i]


def write_bank_customer_info(file_to_load, id, segment):
    satisfaction = pick_satisfaction(id, segment)
    churnScore = pick_churnScore(id, segment)
#    file_to_load.write("%5.2f;%5.2f;" % (satisfaction, churnScore))
    file_to_load.write("%5.2f;" % (satisfaction)

def write_bank_portfolio_info(file_to_load, id, segment):
    shareOfWallet = pick_shareOfWallet(id, segment)
    shareOfWalletHoldings = pick_shareOfWalletHoldings(id, segment)
    shareOfWalletSize = pick_shareOfWalletSize(id, segment)
    proportionShareOfWallet = pick_proportionShareOfWallet(id, segment)
    file_to_load.write("%5.2f;%10.2f;%6.2f;%s;" % (
        shareOfWallet, shareOfWalletHoldings, shareOfWalletSize,proportionShareOfWallet))

def write_bank_assets_info(file_to_load, id, segment):
    totalAssets = pick_totalAssets(id, segment)
    file_to_load.write("%7.0f;" % (totalAssets))

def write_affinities_info(file_to_load,id, segment):
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
    file_to_load.write("%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;" % (
        affNightLife, affSport, affHealthFitness, affOutdoor, affLuxuryShopper, affMovie, affPetLovers, affFastFood,
        affValueShopper, affTechnophiles, affGreenLiving, affMusic))

def write_affinities_info2(file_to_load,id, segment):
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
    file_to_load.write("%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f;%3.0f" % (
        affFoodies,affCooking,affShutterbugs,affSavvyParents,affDIY,affAuto,affFashionistas,affBeautyMavens,
        affHomeDecor,affPolitical,affAvidInvestor,affThrillSeeker,affBargainHunter,affTravelBuff,affLuxuryTravel,
        affFamilyVacation,affBeachTravel,affWinterTravel,affNewsJunky,affArtTheater,affGamer,affTV))


# Import customer data
crm_df = pd.read_csv(c_file, sep=';')
#print crm_df

def main_crm():
    segment_crm_data = [
        load(model_file('segment_crm_1.json')),
        load(model_file('segment_crm_2.json')),
        load(model_file('segment_crm_3.json')),
        "",
        load(model_file('segment_crm_5.json')),
        load(model_file('segment_crm_6.json')),
        load(model_file('segment_crm_7.json'))
    ]


    file_hdr_to_load =open(output_file("RandomCrmDataToLoad.hdr"), 'w')
    file_hdr_to_load.write('id;segnr;')
    file_hdr_to_load.write('share_Of_Wallet;share_Of_Wallet_Holdings;share_Of_Wallet_Size;proportion_Share_Of_Wallet;')
    file_hdr_to_load.write('satisfaction;score_Churn;')
    file_hdr_to_load.write('total_Assets;')
    file_hdr_to_load.write('aff_Night_Life;aff_Sport;aff_Health_Fitness;aff_Outdoor;aff_Luxury_Shopper;aff_Movie;aff_Pet_Lovers;aff_Fast_Food;aff_Value_Shopper;aff_Technophiles;aff_Green_Living;aff_Music;')
    file_hdr_to_load.write('aff_Foodies;aff_Cooking;aff_Shutterbugs;aff_Savvy_Parents;aff_DIY;aff_Auto;aff_Fashionistas;aff_Beauty_Mavens;aff_Home_Decor;aff_Political;aff_Avid_Investor;aff_Thrill_Seeker;')
    file_hdr_to_load.write('aff_Bargain_Hunter;aff_Travel_Buff;aff_Luxury_Travel;aff_Family_Vacation;aff_Beach_Travel;aff_Winter_Travel;aff_News_Junky;aff_Art_Theater;aff_Gamer;aff_TV\n;')

    file_out_to_load =open(output_file("RandomCrmDataToLoad.csv"), 'w')



    pb = Bar('Generating', max=len(crm_df), fill='=', suffix='%(percent)d%%')
    for id in range(1, len(crm_df) + 1):
        segnr = crm_df.ix[id-1,'segnr']
        segment=load_profile(segnr,segment_crm_data)
        file_out_to_load.write("%s;%s;" % (id, segnr))

        write_bank_portfolio_info(file_out_to_load, id, segment)
        write_bank_customer_info(file_out_to_load, id, segment)
        write_bank_assets_info(file_out_to_load, id, segment)
        write_affinities_info(file_out_to_load, id, segment)
        write_affinities_info2(file_out_to_load, id, segment)
        file_out_to_load.write("\n")

        pb.next()

if __name__ == "__main__":
    main_crm()