#! /usr/bin/python3
"""
author : lw
date :2020-03-29
description: update all pip package
"""
import os
import subprocess

if __name__ == '__main__':
    update_list_gen = subprocess.Popen(r"./pip3.7 list --format=columns  | awk '{if(NR>2){print $1}}'", shell=True ,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
    for i in update_list_gen.stdout.readlines():
        i = str(i.strip(),'utf-8')
        print(i)
        os.system('./pip3.7 install --index-url https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade {}'.format(i))
