#!/bin/bash
if [[ $# -le 0 ]]; then
    echo "Please indicate the Python or C program"
    exit
fi

if [[ $# -ge 2 ]]; then
    g++ ${1}.cpp -o ${1}
    for i in {0..6}; do
        start=$((i * 3))
        end=$(((i + 1) * 3 - 1))
        #echo ${start} ${end}
        ./${1} ${start} ${end} &
    done
else
    for i in {0..6}; do
        start=$((i * 5))
        end=$(((i + 1) * 5 - 1))
        #echo ${start} ${end}
        #python3 getfeatures.py ${start} ${end} &
        #python3 stdfeatures.py ${start} ${end} &
        python3 ${1} ${start} ${end} &
    done
fi
