import os
import json
import pandas as pd

class osn_analysis:
    def __init__(self, conf_filename):
        """
        init class
        """
        self.osn_resfile_dict = {}
        self.osn_stat_df = pd.DataFrame();

        with open(conf_filename, "r", encoding = 'utf8') as file_json:
            config_json = json.load(file_json)

            self.res_data_dir = config_json["res_data_dir"]
            self.osn_websites = config_json["websites"]

            for website, website_info in self.osn_websites.items():
                # result file data path
                self.osn_resfile_dict[website] = self.res_data_dir + website_info["res_filename"]
    
    def osn_statistic_day_sum(self):
        
        for website, res_file in self.osn_resfile_dict.items():
            osn_stat_se = pd.read_csv(res_file)["date"].value_counts().sort_index()
            osn_stat_se.name = website
            
            #print(osn_stat_se)
            self.osn_stat_df = pd.concat([self.osn_stat_df, osn_stat_se], axis = 1)
        
        print(self.osn_stat_df)

if __name__ == '__main__':
    analysis = osn_analysis("config.json")
    analysis.osn_statistic_day_sum()


