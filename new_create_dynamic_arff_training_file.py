import sys
import os
import utilities
from tqdm import tqdm


def already_processed_hashes_and_urls(url_index_mapping, dynamic_1K_addr):
    all_dynamic_features_data = utilities.read_file_newline_stripped(
        dynamic_1K_addr)
    all_urls = utilities.read_file_newline_stripped(url_index_mapping)

    hashes = []
    urls = []
    seen = False

    for row in all_dynamic_features_data:
        if row.strip() == '@data':
            seen = True
            continue

        if seen:
            if row.strip() == '':
                continue
            else:
                splitted_row = row.split(',', 3)
                if splitted_row[1].strip() != '' and splitted_row[1].strip() != '?':
                    hashes.append(splitted_row[1].strip())
                elif splitted_row[0].strip() != '' and splitted_row[0].strip() != '?' and splitted_row[0].strip() != 'URL_N':
                    actual_url = all_urls[int(
                        splitted_row[0].strip().split('_')[1])]
                    urls.append(actual_url.strip())

    return hashes, urls


def create_arff(top_dynamic_features_addr, all_dynamic_features_csv_addr, file_to_write, url_index_mapping_all_data, seen_hashes, seen_urls):
    top_dynamic_features = utilities.read_file_newline_stripped(
        top_dynamic_features_addr)
    all_dynamic_features_csv = utilities.read_file_newline_stripped(
        all_dynamic_features_csv_addr)
    all_urls = utilities.read_file_newline_stripped(url_index_mapping_all_data)
    print(all_urls)

    feature_mapping_json = {}
    header = all_dynamic_features_csv[0].split(',')

    for item in top_dynamic_features:
        feature_mapping_json[item] = header.index(item)
    # print(top_dynamic_features)
    all_rows = []

    seen_hashes_count = 0
    seen_urls_count = 0

    all_hashes = set()
    all_urls_unseen = set()

    pbar = tqdm(total=len(all_dynamic_features_csv[1:]))
    # print(all_dynamic_features_csv[0])
    # print("===================================")
    # print(all_dynamic_features_csv[1])
    for row in all_dynamic_features_csv[1:]:
        pbar.update(1)
        splitted_row = row.split(',')
        if splitted_row[0].strip() != '' and splitted_row[0].strip() != '?':
            # print("====")
            # print(splitted_row[0].strip())
            # print("====")
            if splitted_row[0].strip() in seen_hashes:
                seen_hashes_count += 1
                continue
            else:
                all_hashes.add(splitted_row[0].strip())

        elif splitted_row[1].strip() != '' and splitted_row[1].strip() != '?' and splitted_row[1].strip() != 'URL_N':
            print("===================================")
            print(splitted_row[1].strip().split('_'))
            actual_url = all_urls[int(splitted_row[1].strip().split('_')[1])]
            if actual_url in seen_urls:
                seen_urls_count += 1
                continue
            else:
                all_urls_unseen.add(splitted_row[1].strip())

        row_to_add = ''
        for item in top_dynamic_features:
            current_item = splitted_row[feature_mapping_json[item]]
            if current_item.strip() == '':
                current_item = '?'
            row_to_add += current_item + ','

        all_rows.append(row_to_add[:-1])

    arff_header = []
    arff_header.append('@relation dynamic_all_data')
    arff_header.append('')

    print("Seen url: " + ','.join(all_urls_unseen))

    for item in top_dynamic_features:
        if item == 'hash':
            arff_header.append('@attribute ' + item +
                               ' {' + ','.join(all_hashes) + '}')
        elif item == 'url_id':
            if len(all_urls_unseen) == 0:
                arff_header.append('@attribute ' + item +'{URL_N}')
            else:
                #arff_header.append('@attribute ' + item +'{URL_N}')
                arff_header.append('@attribute ' + item +
                                ' {' + ','.join(all_urls_unseen) + ', URL_N}')
        elif item == 'class':
            arff_header.append('@attribute ' + item + ' {FP,NONFP}')
        else:
            arff_header.append('@attribute ' + item + ' numeric')
    arff_header.append('')
    arff_header.append('@data')
    arff_header.append('')

    utilities.write_list_simple(file_to_write, arff_header + all_rows)
    print('seen hash count, seen url count',
          seen_hashes_count, seen_urls_count)

def main(data_directory,extra_directory):
    # example: python3 new_create_dynamic_arff_training_file.py /Users/luoyisang/FP/fp-inspector-classification/output/data /Users/luoyisang/FP/fp-inspector-classification/extra_data
    # data_directory = sys.argv[1]
    # extra_directory = sys.argv[2]

    top_dynamic_features_addr = os.path.join(extra_directory,'dynamic_top_1K_features.txt')
    dynamic_1K_addr = os.path.join(data_directory,'features_with_encoding.arff')
    all_dynamic_features_csv_addr = os.path.join(data_directory,'features_with_encoding.csv')
    file_to_write = os.path.join(data_directory,'correct_dynamic_features_all_data2.arff')
    url_index_mapping = os.path.join(data_directory,'url_index_mapping.txt')
    url_index_mapping_all_data = os.path.join(data_directory,'url_index_mapping.txt')


    seen_hashes, seen_urls = already_processed_hashes_and_urls(
        url_index_mapping, dynamic_1K_addr)

    create_arff(top_dynamic_features_addr, all_dynamic_features_csv_addr,
                file_to_write, url_index_mapping_all_data, seen_hashes, seen_urls)

if __name__ == '__main__':
    # main()
    main(arg1, arg2)
