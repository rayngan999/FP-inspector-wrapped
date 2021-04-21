import sys
import os
from os import listdir
from os.path import isfile, join
import convert_sql_tables_to_json
import extract_features_from_properties_training
import new_create_dynamic_arff_training_file
import csv
import sqlite3
import json
import subprocess
import arff
import shutil

def run_weka(results_file):
        model = "./dynamic_1K_iteration_4.model"
        input_file = "./output/data/correct_dynamic_features_all_data2.arff"
        cmd = "java -cp ./weka.jar weka.classifiers.misc.InputMappedClassifier -L " + model + " -t " + input_file + " -T " + input_file + " -classifications weka.classifiers.evaluation.output.prediction.PlainText > prediction_results.txt"
        os.system(cmd)



def get_fp_inst_num(results_file, fp_list):
        
        num =0

        f = open(results_file, "r")

        for lines in f:
                start = 0
                started = False
                end = 0
                #change this for :NONFP or :FP
                if lines.find(":FP") != -1:
                        
                        for x in lines:
                                if x != " ":
                                        started = True
                                if x == " " and started:
                                        break;
                                if(started == False):
                                        start = start + 1
                                end = end + 1

                        fp_list.append(lines[start:end])
                        #print(lines[start:end])
                        
        #                 num = num+1
                        
        # if(num == 0):
        #         quit()
        # print("Number of hashes: "+str(num))

def get_fp_hashes(fp_list, fp_hash,nfp_hash):
        
        with open("./output/data/dynamic_features_with_mappings.csv", newline = '') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                next(csv_reader)
                for row in csv_reader:
                        
                        line_count += 1
                        if str(line_count) in fp_list and f'{row[0]}' != "" :
                                print("FP:",f'{row[0]}')
                                fp_hash.append(f'{row[0]}')
                        elif str(line_count) not in fp_list:
                                print("NONFP:",f'{row[0]}')
                                nfp_hash.append(f'{row[0]}')


def main():
    for i in range(3,11):
      #  if i == 0:
       #         continue
     
        fp_hash = []
        nfp_hash= []
        err_list =[]
        folderNames = ["beautifyTools", "clos_comp/simple", "clos_comp/advanced", "draftlogic", "jfogs",
        "js_obfus", "obfus_io/default", "obfus_io/high", "obfus_io/low", "obfus_io/medium", "original"]
        analysis_folder  = "../Results/" + folderNames[i] + "/all_sqlite/"


        directory = "./"
        onlyfiles = [f for f in listdir(analysis_folder ) if isfile(join(analysis_folder , f))]

        # print(analysis_name)

        for analysis_name in onlyfiles:
       # for x in range(1):
           # analysis_name = '83d7c6c27f7aae46379d401c0189cbf1.sqlite' 
            data_folder = "output/data"
            for filename in os.listdir( data_folder):
                filepath = os.path.join( data_folder, filename)
                os.remove(filepath)
            analysis_directory = os.path.join(analysis_folder, analysis_name)
        
            if analysis_name.find('.sqlite') == -1:
                continue
            convert_sql_tables_to_json.main(analysis_directory)
            extract_features_from_properties_training.main("./output/data", os.path.join(directory, "extra_data"))
            new_create_dynamic_arff_training_file.main("./output/data", os.path.join(directory, "extra_data"))
            results_file = "./prediction_results.txt"

            hash_name = analysis_name[:analysis_name.find(".sqlite")]
            print(hash_name)
            # get hash_name top url
            # loop thru json to get all hashes from top url 

            cur_fp_hash =[]
            cur_nfp_hash =[]
            fp_list = []
            run_weka(results_file)
            get_fp_inst_num(results_file, fp_list)
            get_fp_hashes(fp_list,fp_hash,nfp_hash)

            with open('new_fingerprinting_domains.json') as f:
                fp_domains = json.load(f)
            for x in fp_domains:
                if x in cur_fp_hash:
                    fp_hash.append(x)
                    print("FP-",x)
                if x in cur_nfp_hash:
                    nfp_hash.append(x)
                    print("NFP-",x)

            #     if x == hash_name:
            #         cur_top_url = fp_domains[x][1]

            # for x in fp_domains:
            #     if fp_domains[x][1] == cur_top_url:
            #         # print(fp_domains[x][0])
            #         print(x)

    #        with open('nfp_hashes.json') as outfile:
    #            data = json.load(outfile)
    #        for x in cur_nfp_hash:
    #            data.append(x)

            with open('nfp_hashes.json','w') as outfile:
                json.dump(nfp_hash, outfile, indent=4)

    #        with open('fp_hashes.json') as outfile:
    #            data = json.load(outfile)
    #        for x in cur_fp_hash:
    #            data.append(x)
            with open('fp_hashes.json','w') as outfile:
                json.dump(fp_hash, outfile, indent=4)
                
            with open('err_list.json','w') as outfile:
                json.dump(err_list, outfile, indent=4)
     
        shutil.move('nfp_hashes.json', "../Results/" + folderNames[i])
        shutil.move('fp_hashes.json', "../Results/" + folderNames[i])
        shutil.move('err_list.json', "../Results/" + folderNames[i])



if __name__ == '__main__':
    main()

    

    #python3 dynamic_analysis.py "./" "./crawl-data_part3.sqlite" "./output" "./data" 5000 
