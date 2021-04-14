import csv
import sqlite3
import json
import subprocess
import os
import sys


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
                        
        #                 num = num+1
                        
        # if(num == 0):
        #         quit()
        # print("Number of hashes: "+str(num))

def get_fp_hashes(fp_list, fp_hash):
        
        with open("./output/data/dynamic_features_with_mappings.csv", newline = '') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                        
                        line_count += 1
                        if str(line_count) in fp_list and f'{row[0]}' != "":
                                print("FP:",f'{row[0]}')
                        elif str(line_count) not in fp_list:
                                print("NONFP:",f'{row[0]}')
                                # fp_hash.append(f'{row[0]}')
                                


        
def get_scripts_top_sqlite(sql,fp_hash,hash_dict):
        try:    
                sqliteConnection = sqlite3.connect(sql)
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")
                cursor.execute("SELECT * FROM http_responses")
                rows = cursor.fetchall()
                print("Fetched All Rows for http_responses")
        
                for row in rows:
                        if row[13] in fp_hash:
                                if hash_dict.get(row[13]) == None:
                                        hash_dict1 = {row[13]:[row[3],row[5]]}
                                        hash_dict.update(hash_dict1)
                                else:
                                        hash_dict[row[13]].append([row[3],row[5]])
                
        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("sqlite connection is closed")

def to_json(hash_dict, json_name):
        with open(json_name,'w') as outfile:
                json.dump(hash_dict, outfile, indent=4)
                
        hashes = 0
        num = 0
        for x in hash_dict:
                hashes = hashes + 1
                for y in x:
                        num = num +1
        print("Number of Scripts: " + str(num))
        print("Number of Hashes: " + str(hashes))



def main():
        #change this
        folderNames = ["beautifyTools", "clos_comp/simple", "clos_comp/advanced", "draftlogic", "jfogs",
        "js_obfus", "obfus_io/default", "obfus_io/high", "obfus_io/low", "obfus_io/medium", "original"]
        analysis_folder  = "../Scripts-Replacing-Crawler/openWPM_data/" + folderNames[0] + "/all_sqlite/"
        analysis_name = "b394030e12a553646e5fc2b9f1523960.sqlite"    
        sql = os.path.join(analysis_folder, analysis_name)
        results_file = "./prediction_results.txt"
        json_name = 'non_fingerprinting_domains_orig.json'
        fp_list = []
        fp_hash = []
        hash_dict = {}
        

        try:
                open(results_file)
        except IOError:
                run_weka(results_file)
        get_fp_inst_num(results_file, fp_list)
        get_fp_hashes(fp_list,fp_hash)
        # get_scripts_top_sqlite(sql,fp_hash,hash_dict)
        # to_json(hash_dict,json_name)
        


main()
