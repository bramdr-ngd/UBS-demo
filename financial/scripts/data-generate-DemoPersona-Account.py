#!/usr/bin/python
import os
import argparse


# globals
source = 'C:/Projects/Lily/Lily-demo/financial/schemas/src/main/resources/scripts/.data'

# Read command line args
parser = argparse.ArgumentParser(description='Generate DemoPersona Entity Account data for Lily demo environments')
parser.add_argument('-o','--output', help='output folder',required=False, default='.data')
args = parser.parse_args()

o_folder = args.output

# functions
def output_file(file_name):
    return o_folder + "/" + file_name

# Outputfile
file_out=open(output_file("DemoPersonaAccountData.csv"), 'w')

# Create header
headers = open(output_file('AccountData.hdr'), "r").readlines()[0]
file_hdr=open(output_file("DemoPersonaAccountData.hdr"), 'w')
file_hdr.write(headers)

def main_crm():
    for i in range(1, 15):
        text_file = open(output_file('EntityDataToLoad.csv'), "r")
        #ENTITY_ID;ID;PRODUCT;WAARDE;START;END;TYPE;SUBTYPE;ACTIF;
        lines = text_file.readlines()

        for line in lines:
            parts = line.split(";")

            #3346 -> Krista Johnson
            #22639 -> Desmond Thomas

            if i==1 and parts[1]=="22639" :    #Clone Desmond Thomas - Luc Burgelman
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==2 and parts[1]=="3346" : #Clone Krista Johnson - Luc Burgelman
                parts[0]=(int(parts[0]) - 3346000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==3 and parts[1]=="22639" :    #Clone Desmond Thomas - Frank Hamerlinck
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==4 and parts[1]=="22639" :    #Clone Desmond Thomas - Aaron Rosenthal
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==5 and parts[1]=="3346" : #Clone Krista Johnson - Sara Tohey
                parts[0]=(int(parts[0]) - 3346000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==6 and parts[1]=="22639" :    #Clone Desmond Thomas - Edwin Madou
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==7 and parts[1]=="22639" :    #Clone Desmond Thomas - Joe Pilkerton
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==8 and parts[1]=="3346" : #Clone Krista Johnson - Molly Galetto
                parts[0]=(int(parts[0]) - 3346000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==9 and parts[1]=="22639" :    #Clone Desmond Thomas - Wim Driessens
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==10 and parts[1]=="22639" :    #Clone Desmond Thomas - Wim Driessens
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==11 and parts[1]=="22639" :    #Clone Desmond Thomas - Steven Noels
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==12 and parts[1]=="22639" :    #Clone Desmond Thomas - Ron Ranaldi
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==13 and parts[1]=="22639" :    #Clone Desmond Thomas - Stephanne Marlin
                parts[0]=(int(parts[0]) - 22639000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))

            if i==14 and parts[1]=="3346" : #Clone Krista Johnson - Roos Vogel
                parts[0]=(int(parts[0]) - 3346000) + ((99950+i)*1000)
                file_out.write('%s;%s;%s;%s;%s\n' %(parts[0],parts[2],parts[7],parts[3],parts[8]))


if __name__ == "__main__":
    main_crm()

#            text_file.close()
