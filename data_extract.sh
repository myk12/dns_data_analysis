#!/bin/sh

# init variable
top_dir=`pwd`
data_dir=$top_dir/$1
res_dir=$top_dir"/output/"
conf_file=$top_dir"/config"

# create workdir and path
rm -rf $res_dir
mkdir -p $res_dir

# read osn from config file
osn_arr=(`awk -F '=' '{print $1}' $conf_file`)
key_arr=(`awk -F '=' '{print $2}' $conf_file`)
osn_num=${#osn_arr[*]}

processfiledir(){
    echo "--- processing datadir : [$2]"
    src_dir=$1
    name_dir=$2

    cp -r $src_dir $res_dir
    cd $res_dir/$name_dir

    for file in `ls`
    do
        gunzip $file
        filename=${file%.*}

        # pattern match
        for ((i=0; i<osn_num; i++))
        do
            awk -F '|' '/'${key_arr[i]}'/{print $2, $3}' $filename >> ${osn_arr[i]}
        done

        # clean
        rm -rf $filename
    done
}


main(){
    # start log
    echo "--------------------- data processing start ---------------------"
    echo "- start time  : "`date`
    echo "- top dir     : "$top_dir
    echo "- data dir    : "$data_dir
    echo "- output dir  : "$res_dir
    echo "-----------------------------------------------------------------"
    echo

    # start process data
    start_time=`date '+%x %T'`
    for dir in `ls ${data_dir}`
    do
        processfiledir "${data_dir}/${dir}" "${dir}"
    done
    end_time=`date '+%x %T'`

    # compress result data
    cd $top_dir
    tar -zcf result.tar.gz output

    # result log
    echo
    echo "--------------------- data processing complete! ---------------------"
    echo "- start at : "$start_time
    echo "- end at   : "$end_time
    echo "- result data compressed to file : <result.tar.gz>"
    echo "---------------------------------------------------------------------"
}

# start data processing
main
