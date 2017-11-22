#!/usr/bin/python
import os
import argparse


# globals
source = '/disk1/current'

# Read command line args
parser = argparse.ArgumentParser(description='Generate DemoPersona CRM data for Lily demo environments.')
parser.add_argument('-o','--output', help='output folder',required=False, default='.data')
args = parser.parse_args()

o_folder = args.output

# functions
def output_file(file_name):
    return o_folder + "/" + file_name


for file in os.listdir(source):
#    print(file)
    if file.endswith(".hdr"):
        if file.find('ItxData_') != -1 and file.find('_DemoPersona') == -1:
            fullpath = os.path.join(source, file)
            filename=file[:-4]+"_DemoPersona.hdr"
            file_hdr=open(output_file(filename), 'w')
            header = open(fullpath, "r").readlines()[0]
            file_hdr.write(header)


    if file.endswith(".csv"):
        if file.find('ItxData_') != -1 and file.find('_DemoPersona') == -1:
            print(file)
            fullpath = os.path.join(source, file)
            filename=file[:-4]+"_DemoPersona.csv"
            file_out=open(output_file(filename), 'w')

            for i in range(1, 15):
                text_file = open(fullpath, "r")

                lines = text_file.readlines()
                for line in lines:
#                print(line)
                    parts = line.split(";")




            #3346 -> Krista Johnson
            #22639 -> Desmond Thomas

                    if i==1 and parts[0]=="22639" :    #Clone Desmond Thomas - Luc Burgelman
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==2 and parts[0]=="3346" : #Clone Krista Johnson - Luc Burgelman
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==3 and parts[0]=="22639" :    #Clone Desmond Thomas - Frank Hamerlinck
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==4 and parts[0]=="22639" :    #Clone Desmond Thomas - Aaron Rosenthal
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==5 and parts[0]=="3346" : #Clone Krista Johnson - Sara Tohey
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==6 and parts[0]=="22639" :    #Clone Desmond Thomas - Edwin Madou
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==7 and parts[0]=="22639" :    #Clone Desmond Thomas - Joe Pilkerton
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==8 and parts[0]=="3346" : #Clone Krista Johnson - Molly Galetto
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==9 and parts[0]=="22639" :    #Clone Desmond Thomas - Wim Driessens
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==10 and parts[0]=="22639" :    #Clone Desmond Thomas - Wim Driessens
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==11 and parts[0]=="22639" :    #Clone Desmond Thomas - Steven Noels
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==12 and parts[0]=="22639" :    #Clone Desmond Thomas - Ron Ranaldi
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==13 and parts[0]=="22639" :    #Clone Desmond Thomas - Stephanne Marlin
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")

                    if i==14 and parts[0]=="3346" : #Clone Krista Johnson - Roos Vogel
                        parts[0]=99950+i
                        for j in range(0,len(parts)-1) :
                            file_out.write("%s;" % (parts[j]))
                        file_out.write("%s" % (parts[len(parts)-1]))
#                file_out.write("\n")


                text_file.close()
            file_out.close()
