import os
import pandas as pd
import json

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
            config_json = json.load(load_conf)

            self.websites_conf = config_json["websites"]
            self.data_compress_type = config_json["data_compress_type"]
            self.data_columns_name = config_json["data_columns_name"]
            self.data_delimiter = config_json["data_delimiter"]

            for website, website_info in self.websites_conf.items():

                self.keywords_dict[website] = website_info["keywords"]
                self.dataframes_dict[website] = pd.DataFrame(columns=['time', 'domain_name'])
                
                file_name = self.outputdir + '/' + website_info["res_filename"]
                self.filenames_dict[website] = file_name

                #create file to save data
                with open(file_name, "w") as csv_fd:
                    csv_fd.write("time,domain_name\n")

    def save_data(self):
        for website, dataframe in self.dataframes_dict.items():
            dataframe.to_csv(self.filenames_dict[website], mode = 'a', index = False, header = False)

            # empty the dataframe
            dataframe.drop(dataframe.index, inplace=True)
            print("data saved.")

    def process_dataframe(self, df_data):
        for website, keywords in self.keywords_dict.items():
            osn_dataframe = df_data[df_data["domain_name"].str.contains(keywords, na = False)]

            # concat
            self.dataframes_dict[website] = pd.concat([self.dataframes_dict[website], osn_dataframe], ignore_index = True)

    def process_data(self):
        dir_list = os.listdir(self.datadir)
        dir_list.sort()
    
        # Walk through all folders in the data_dir directory
        for filedir in dir_list:
            # process data of days
            file_path = self.datadir + '/' + filedir
            file_list = os.listdir(file_path)

            print("+++ processing datadir :", filedir)
            dataframe = pd.DataFrame()

            for file in file_list:
                # read data from gzip file
                df = pd.read_csv(file_path + '/' +  file, \
                                compression = self.data_compress_type, \
                                delimiter = self.data_delimiter, \
                                names = self.data_columns_name)[["time","domain_name"]]
                
                self.process_dataframe(df)
            
            #save data to file
            self.save_data()

if __name__ == "__main__":
    date_process = preprocessing()
    date_process.process_data()