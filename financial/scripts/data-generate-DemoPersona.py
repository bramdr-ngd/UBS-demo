#!/usr/bin/python
import argparse

# globals

# Read command line args
parser = argparse.ArgumentParser(description='Generate DemoPersona CRM data for Lily demo environments.')
parser.add_argument('-o','--output', help='output folder',required=False, default='.data')
args = parser.parse_args()

o_folder = args.output

# functions
def output_file(file_name):
    return o_folder + "/" + file_name

# Outputfile
file_out=open(output_file("DemoPersonaDataToLoad.csv"), 'w')

# Retrieve indeces
headers = open(output_file('CrmDataToLoad.hdr'), "r").readlines()[0].split(';')
firstname = headers.index('first_name')
lastname = headers.index('last_name')
phone = headers.index('phone_number')
mail = headers.index('email_address')

# Create header
headers2 = open(output_file('CrmDataToLoad.hdr'), "r").readlines()[0]
file_hdr=open(output_file("DemoPersonaDataToLoad.hdr"), 'w')
file_hdr.write(headers2)



def main_crm():
    for i in range(1, 15):
        text_file = open(output_file('CrmDataToLoad.csv'), "r")
        lines = text_file.readlines()

        for line in lines:
            parts = line.split(";")

            #3346 -> Krista Johnson
            #22639 -> Desmond Thomas

            if i==1 and parts[0]=="22639" :    #Clone Desmond Thomas - Luc Burgelman
                parts[0]=99950+i
                parts[firstname]="Desmond"
                parts[lastname]="Thomaz"
                parts[phone]="+1 4156039217"
                parts[mail]="lucb@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==2 and parts[0]=="3346" : #Clone Krista Johnson - Luc Burgelman
                parts[0]=99950+i
                parts[firstname]="Kristi"
                parts[lastname]="Johnson"
                parts[phone]="+1 4156039217"
                parts[mail]="lucb@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==3 and parts[0]=="22639" :    #Clone Desmond Thomas - Frank Hamerlinck

                parts[0]=99950+i
                parts[firstname]="Peter"
                parts[lastname]="Lance"
                parts[phone]="+32 475826140"
                parts[mail]="frankh@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==4 and parts[0]=="22639" :    #Clone Desmond Thomas - Aaron Rosenthal
                parts[0]=99950+i
                parts[firstname]="Kevin"
                parts[lastname]="Adamo"
                parts[phone]="+1 9172091299"
                parts[mail]="aaronr@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==5 and parts[0]=="3346" : #Clone Krista Johnson - Sara Tohey
                parts[0]=99950+i
                parts[firstname]="Jennifer"
                parts[lastname]="Frost"
                parts[phone]="+1 4044449455"
                parts[mail]="sarat@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==6 and parts[0]=="22639" :    #Clone Desmond Thomas - Edwin Madou
                parts[0]=99950+i
                parts[firstname]="Steve"
                parts[lastname]="Becker"
                parts[phone]="+32 475878623"
                parts[mail]="edwinm@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==7 and parts[0]=="22639" :    #Clone Desmond Thomas - Joe Pilkerton
                parts[0]=99950+i
                parts[firstname]="Brent"
                parts[lastname]="Slater"
                parts[phone]=" "
                parts[mail]="joep@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==8 and parts[0]=="3346" : #Clone Krista Johnson - Molly Galetto
                parts[0]=99950+i
                parts[firstname]="Kristin"
                parts[lastname]="Clark"
                parts[phone]=" "
                parts[mail]="mollyg@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==9 and parts[0]=="22639" :    #Clone Desmond Thomas - Wim Driessens
                parts[0]=99950+i
                parts[firstname]="RobertEU"
                parts[lastname]="Nolan"
                parts[phone]="+32 493250326"
                parts[mail]="wimd@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==10 and parts[0]=="22639" :    #Clone Desmond Thomas - Wim Driessens
                parts[0]=99950+i
                parts[firstname]="RobertUS"
                parts[lastname]="Nolan"
                parts[phone]="+1 3478025937"
                parts[mail]="wimd@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==11 and parts[0]=="22639" :    #Clone Desmond Thomas - Steven Noels
                parts[0]=99950+i
                parts[firstname]="Jordan"
                parts[lastname]="Davis"
                parts[phone]="+32 478292900"
                parts[mail]="stevenn@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==12 and parts[0]=="22639" :    #Clone Desmond Thomas - Ron Ranaldi
                parts[0]=99950+i
                parts[firstname]="Michael"
                parts[lastname]="Turner"
                parts[phone]="+1 6466613970"
                parts[mail]="ronr@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==13 and parts[0]=="22639" :    #Clone Desmond Thomas - Stephanne Marlin
                parts[0]=99950+i
                parts[firstname]="Chris"
                parts[lastname]="Thompson"
                parts[phone]="+33 622927384"
                parts[mail]="stephanem@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

            if i==14 and parts[0]=="3346" : #Clone Krista Johnson - Roos Vogel
                parts[0]=99950+i
                parts[firstname]="Diana"
                parts[lastname]="Fields"
                parts[phone]="+31 620968820"
                parts[mail]="roosv@ngdata.com"

                for j in range(0,len(parts)-1) :
                    file_out.write("%s;" % (parts[j]))
                file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

if __name__ == "__main__":
    main_crm()