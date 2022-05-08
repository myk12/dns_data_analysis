!/bin/sh

data_dir="new-sample"
res_dir="result"

douyin="ixigua.com.w.kunlunle.com|ixigua.com.v4.tcdnvod.com|pstatp.com.w.alikunlun.com|gslb.ksyuncdn.com|douyin.com.w.kunluncan.com|snssdk.com.w.kunluncan.com|bytecdn.cn.w.kunlunpi.com|bytecdn.cn.w.kunlunhuf.com|v.qingcdn.com|v6-dy.ixigua.com"

processfile(){
    fullname=$1
    filename=$2
    cp $fullname $filename

    #unzip file
    gunzip $filename
    file=${filename%.*}

    awk -F '|' '/'${douyin}'/{print $2,$3}' $file >> ./data.dat

    #clean
    rm -rf ${file}
}

init_env(){

}

main(){
    init_env
    echo "===================== start ====================="
    date
    for dir in `ls ${data_dir}`
    do
        echo "process datadir [${dir}]"
        for file in `ls ${data_dir}/${dir}`
        do
            processfile "${data_dir}/${dir}/${file}" "${file}"
        done
    done
    echo "===================== end  ====================="
    date
}

main
