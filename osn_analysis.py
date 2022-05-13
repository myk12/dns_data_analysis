import os
import re
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
    
    def read_data(self):
        # get all result dir
        result_list = []
        [re.match("result_", dir) and result_list.append(dir) for dir in os.listdir("./")]


class shell_result_analysis:
    def __init__(self):
        # data check
        if not os.path.exists("./result.tar.gz") or not os.path.exists("./config"):
            raise Exception("data not exists!")
        
        # compress data
        os.system("tar -zxf result.tar.gz -C /tmp/")

        # variable define
        self.src_dir = "/tmp/output/"
        self.osn_list = []
        with open("./config", "r+") as conf:
            conf_lines = conf.readlines()
            [self.osn_list.append(osn.split('=')[0]) for osn in conf_lines]
    
    def get_day(self, day):
        day_dict = {}

        day_dict["date"] = day
        src_path = self.src_dir + day
        osn_list = os.listdir(src_path)
        for osn in osn_list:
            with open(src_path + '/' + osn, 'r') as osn_fd:
                day_dict[osn] = len(osn_fd.readlines())
        
        return day_dict
        

    def analyze_timeline(self):
        days_list = os.listdir(self.src_dir)

        # extract data to dataframe
        df = pd.DataFrame()
        for day in days_list:
            dic = self.get_day(day)

            if 'df' not in dir():
                df = pd.DataFrame([dic])
                print(type(df))
            else:
                df = pd.concat([df, pd.DataFrame([dic])], ignore_index=True)
        #print(df)
        
        # trans data
        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
        df.set_index("date", inplace=True)
        df = df.sort_index(ascending=True)

        #plot
        df.plot()
        #plt.show()
        plt.savefig("osn_timeline_req.png")

        return df

    def analyze_daytime(self, osn_name):
        days_list = os.listdir(self.src_dir)
        req_time_count_dic = {}
        
        d = 0
        for days in days_list:
            df = pd.read_csv(self.src_dir + days + '/' + osn_name,delimiter = ' ', names = ['domain', str(d)])
            df[str(d)] = df[str(d)].apply(lambda t: str(t)[8:-2])
            se_count = df[str(d)].value_counts().to_frame()

            if 'df_total' not in dir():
                df_total = se_count
            else:
                df_total = pd.concat([df_total, se_count], axis=1)
            d += 1

        df_day_req_stat = df_total.apply(lambda x:x.sum(), axis=1)

        #plot
        df_day_req_stat.index = pd.to_datetime(df_day_req_stat.index, format="%H%M")
        df_day_req_stat.plot()
        plt.savefig(osn_name + "_day_req.png")



if __name__ == '__main__':
    try:
        analysis_obj = shell_result_analysis()
    except Exception as err_msg:
        print("error : %s" %(err_msg))

    analysis_obj.analyze_timeline()
    analysis_obj.analyze_daytime("douyin")