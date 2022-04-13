import os
import gzip
from pydoc import resolve
import pandas as pd
import json
import re

class preprocessing:
    def __init__(self, datadir = "./data/", outputdir = "./result/"):
        """
        init context
        """
        self.datadir = datadir
        self.outputdir = outputdir
        self.dataframes_dict = {}
        self.keywords_dict = {}
        self.filenames_dict = {}

        # load config json
        with open("config.json", "r", encoding="utf-8") as load_conf:
            self.websites_conf = json.load(load_conf)["websites"]

            for website, website_info in self.websites_conf.items():
                self.keywords_dict[website] = website_info["keywords"]
                self.dataframes_dict[website] = pd.DataFrame(columns=['date', 'domain_name'])
                
                file_name = self.outputdir + '/' + website_info["res_filename"]
                self.filenames_dict[website] = file_name

                #create file to save data
                with open(file_name, "w") as csv_fd:
                    csv_fd.write("date,domain_name\n")


    def process_items(self, item):
        item_components = item.decode().split("|")

        domain_name = item_components[1]
        resolve_time = item_components[2]

        for website, name in self.keywords_dict.items():
            if name in domain_name:
                it = {}
                it["date"] = resolve_time[0:10]
                it["domain_name"] = domain_name
                
                self.dataframes_dict[website] = self.dataframes_dict[website].append(pd.Series(it), ignore_index=True)


    def get_compressed_data(self, filename):
        #unzip file and read
        un_file = gzip.GzipFile(filename)
        file_lines = un_file.readlines()

        for line in file_lines:
            self.process_items(line)

    def save_data(self):
        for website, dataframe in self.dataframes_dict.items():
            dataframe.to_csv(self.filenames_dict[website], mode = 'a', index = False, header = False)

            # empty the dataframe
            dataframe.drop(dataframe.index, inplace=True)
            #print("data saved.")

    def readData(self):
        dir_list = os.listdir(self.datadir)

        print(self.datadir)

        # Walk through all folders in the data_dir directory
        for filedir in dir_list:
            # process data of days
            file_path = self.datadir + '/' + filedir
            file_list = os.listdir(file_path)

            print("+++ processing datadir :", filedir)
            for file in file_list:
                #print("+++ processing file", file)
                file_lines = self.get_compressed_data(file_path + '/' +  file)
                self.save_data()
                #print("--- saved data")

    def run(self):
        self.readData()

if __name__ == "__main__":
    date_process = preprocessing()
    date_process.run()