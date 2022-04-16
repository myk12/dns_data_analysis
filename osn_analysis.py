import os
import json
import pandas as pd
import matplotlib.pyplot as plt

class osn_analysis:
    def __init__(self, conf_filename):
        """
        init class
        """
        self.osn_resfile_dict = {}
        self.osn_stat_df = pd.DataFrame()

        with open(conf_filename, "r", encoding = 'utf8') as file_json:
            config_json = json.load(file_json)

            self.res_data_dir = config_json["res_data_dir"]
            self.osn_websites = config_json["websites"]
            self.stat_filename = config_json["res_data_dir"] + config_json["stat_res_filename"]

            for website, website_info in self.osn_websites.items():
                # result file data path
                self.osn_resfile_dict[website] = self.res_data_dir + website_info["res_filename"]
    
    def osn_statistic_day_sum(self):
        
        for website, res_file in self.osn_resfile_dict.items():
            osn_stat_se = pd.read_csv(res_file)["date"].value_counts().sort_index()
            osn_stat_se.name = website
            
            #print(osn_stat_se)
            self.osn_stat_df = pd.concat([self.osn_stat_df, osn_stat_se], axis = 1)
        
        # print(self.osn_stat_df)
        self.osn_stat_df.to_csv(self.stat_filename, index=True)
    
    def show_statistic_graph(self):
        self.osn_statistic_day_sum()
        stat_df = pd.read_csv(self.stat_filename)

        stat_df.to_string(columns={'Unnamed: 0'})
        stat_df.rename(columns={'Unnamed: 0':'time'}, inplace=True)
        stat_df["time"] = pd.to_datetime(stat_df["time"], format="%Y%m%d%H")

        print(stat_df)
        
        plt.close("all")
        stat_df.plot(x = 'time')
        plt.show()

if __name__ == '__main__':
    analysis = osn_analysis("config.json")
    analysis.show_statistic_graph()