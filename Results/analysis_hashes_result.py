import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
folderNames = ["beautifyTools", "clos_comp/simple", "clos_comp/advanced", "draftlogic", "jfogs",
        "js_obfus", "obfus_io/default", "obfus_io/high", "obfus_io/low", "obfus_io/medium", "original"]








# Filter by majority
# f = open("non_filter.json")
# non_filter_list =json.load(f)
# for folder in folderNames:
#         f = open(folder+"/fp_hashes.json")
#         fp_list = json.load(f)
#         new_fp_list = []
#         fp_num = 0
#         for x in fp_list:
#                 if (x in non_filter_list):
#                         new_fp_list.append(x)
                        
#                 else:
#                         fp_num += 1
#                         continue
#         f = open(folder+"/nfp_hashes.json")
#         nfp_list = json.load(f)
#         new_nfp_list = []
#         nfp_num = 0
#         for x in nfp_list:
#                 if (x in non_filter_list):
#                         new_nfp_list.append(x)
                        
#                 else:
#                         nfp_num  += 1
#                         continue

#         print("Filtered", fp_num, "fp hashes in", folder)
#         print("Filtered", nfp_num, "nfp hashes in", folder)
#         move_folder = folder + '/new_fp_hashes.json'
#         with open(move_folder,'w') as outfile:
#                 json.dump(new_fp_list, outfile, indent=4)
#         move_folder = folder + '/new_nfp_hashes.json'
#         with open(move_folder,'w') as outfile:
#                 json.dump(new_nfp_list, outfile, indent=4)




# for folder in folderNames:
#         f = open(folder+"/fp_hashes.json")
#         fp_list = json.load(f)
#         new_fp_list = []
#         fp_num = 0
#         for x in fp_list:
#                 new_fp_list.append(x)
#                 fp_num += 1

#         f = open(folder+"/nfp_hashes.json")
#         nfp_list = json.load(f)
#         new_nfp_list = []
#         nfp_num = 0
#         for x in nfp_list:
#                 new_nfp_list.append(x)
#                 nfp_num += 1

#         print( fp_num, "fp hashes in", folder)
#         print( nfp_num, "nfp hashes in", folder)

# Filter by replaced scripts
# f = open("new_fingerprinting_domains.json")
# fp_domain = json.load(f)
# replaced_hashes= []
# for x in fp_domain:
#         replaced_hashes.append(x)
# print(len(replaced_hashes))

# for folder in folderNames:
#         f = open(folder+"/fp_hashes.json")
#         fp_list = json.load(f)
#         new_fp_list = []
#         fp_num = 0
#         for x in fp_list:
#                 if (x in replaced_hashes):
#                         new_fp_list.append(x)
#                         fp_num += 1
#                 else:
#                         continue

#         f = open(folder+"/nfp_hashes.json")
#         nfp_list = json.load(f)
#         new_nfp_list = []
#         nfp_num = 0
#         for x in nfp_list:
#                 if (x in replaced_hashes):
#                         new_nfp_list.append(x)
#                         nfp_num  += 1
#                 else:
#                         continue
                        

#         print( fp_num, "fp hashes in", folder)
#         print(nfp_num, "nfp hashes in", folder)

#         move_folder = folder + '/filtered_fp_hashes.json'
#         with open(move_folder,'w') as outfile:
#                 json.dump(new_fp_list, outfile, indent=4)
#         move_folder = folder + '/filtered_nfp_hashes.json'
#         with open(move_folder,'w') as outfile:
#                 json.dump(new_nfp_list, outfile, indent=4)




# clean up to set - remove repeated hashes

# for folder in folderNames:
#         s = set()
#         fp_set =[]
#         nfp_set = []
#         f = open(folder+"/filtered_fp_hashes.json")
#         fp_domain = json.load(f)
#         for x in fp_domain:
#                 s.add(x)
#         for x in s:
#                 fp_set.append(x)
#         print(len(fp_domain) - len(fp_set), "repeated fp hashes in ", folder)
#         f = open(folder+"/filtered_nfp_hashes.json")
#         nfp_domain = json.load(f)
#         s = set()
#         for x in nfp_domain:
#                 s.add(x)
#         for x in s:
#                 nfp_set.append(x)
#         print(len(nfp_domain) - len(nfp_set), "repeated nfp hashes in",folder)
#         move_folder = folder + '/fully_filtered_fp_hashes.json'
#         with open(move_folder,'w') as outfile:
#                 json.dump(fp_set, outfile, indent=4)
#         move_folder = folder + '/fully_filtered_nfp_hashes.json'
#         with open(move_folder,'w') as outfile:
#                 json.dump(nfp_set, outfile, indent=4)











# get the set of all hashes in all folders + get results of each hash
s = set()
hashes = []
for folder in folderNames:
        f = open(folder+"/fp_hashes.json")
        fp_domain = json.load(f)
        for x in fp_domain:
                s.add(x)
        f = open(folder+"/nfp_hashes.json")
        nfp_domain = json.load(f)
        for x in nfp_domain:
                s.add(x)
        
num = 0
for x in s:
        hashes.append(x)
        num += 1
print(len(s))

hash_dict = {}
num = 0 
fp_domain = {}
nfp_domain = {}
f = open(folder+"/fp_hashes.json")
l = json.load(f)
for x in l:
        fp_domain[x] = 1 
f = open(folder+"/nfp_hashes.json")
l = json.load(f)
for x in l:
        nfp_domain[x] = 1 
for x in hashes:
        l = []
        d ={}
        
        for folder in folderNames:
                if(x in fp_domain):
                        d[folder] = 1
                elif x in nfp_domain:
                        d[folder] = 0
                else:
                        d[folder] = -1
        num += 1
        l.append(d)
        hash_dict[x] = l
        print(num)
        


with open('./results_test.json','w') as outfile:
                json.dump(hash_dict, outfile, indent=4)


#plotting
# with open("results.json") as test:
#     dictionary = json.load(test)

# hashes = []


# num = 0
# for x in dictionary:
#         l = []
#         count_1 = 0
        
#         for obfuscator in dictionary[x][0]:
#                 if dictionary[x][0][obfuscator] == -1:
#                     count_1 += 1
#                 l.append(dictionary[x][0][obfuscator])
#         if num == 0:
#             arr = np.array([l])
#         else:
#             if count_1 >6:
#                 continue
#             arr = np.append(arr, [l], axis =0)
#         arr = np.append(arr, [l], axis =0)
#         num += 1
#         hashes.append(x)
#         if num == 100:
#                 break

# fig, ax = plt.subplots(figsize=(50,300))
# im = ax.imshow(arr)

# # We want to show all ticks...
# ax.set_xticks(np.arange(len(folderNames)))
# ax.set_yticks(np.arange(len(hashes)))
# # ... and label them with the respective list entries
# ax.set_xticklabels(folderNames)
# ax.set_yticklabels(hashes)

# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
#          rotation_mode="anchor")

# # Loop over data dimensions and create text annotations.
# for i in range(len(hashes)):
#     for j in range(len(folderNames)):
#         text = ax.text(j, i, arr[i, j],
#                        ha="center", va="center", color="w")

# ax.set_title("Hashes Results")
# fig.tight_layout()
# # plt.show()
# plt.savefig('results.png')