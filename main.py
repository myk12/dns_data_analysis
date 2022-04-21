import os
import json
import time
import threading
import argparse
import dataprocess
import osn_analysis

class thread_handler(threading.Thread):
    def __init__(self, id, name, dirlist):
        threading.Thread.__init__(self)
        self.threadID = id
        self.name = name
        self.data_dir_list = dirlist

    def run(self):
        print("+++ start thread %d +++" %self.threadID)

        processor = dataprocess.preprocessing("./result_%d" %self.threadID)
        processor.process_data(self.data_dir_list)

        print("--- exit thread %d ---" %self.threadID)

def main(thread_num = 1):
    #laod  json format config file
    with open("config.json", "r", encoding = "utf-8") as load_conf:
        config_json = json.load(load_conf)

    #get data dir path
    data_source_path = config_json["raw_data_dir"]
    data_file_list = [os.path.join(data_source_path, d) for d in os.listdir(data_source_path)]
    data_file_list.sort()

    #start multi-thread processing
    threads_list = []
    step_len = len(data_file_list) // thread_num
    start, end = 0, step_len

    # create threads
    for i in range(thread_num + 1):
        thread_i = thread_handler(i, "thread %d" %i, data_file_list[start:end])
        threads_list.append(thread_i)

        start, end = end, end + step_len
    
    # start thread
    [thread.start() for thread in threads_list]
    [thread.join() for thread in threads_list]

if __name__ == '__main__':
    # get cmdline params
    parser = argparse.ArgumentParser(description = "main process")
    parser.add_argument("-j", help = "thread numbers", type = int)

    # record process start time
    start_time = time.strftime('%H:%M:%S',time.localtime(time.time()))

    # start process
    if parser.parse_args().j:
        main(parser.parse_args().j)
    else:
        main()

    # record process end time
    end_time = time.strftime('%H:%M:%S',time.localtime(time.time()))

    # brief prompt
    print("\n=============== complete ===============\ndata process\nstart : %s\n  end : %s\n=========================================" %(start_time, end_time))