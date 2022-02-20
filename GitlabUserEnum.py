#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# @Version : 0.1
# @Time    : 2022/2/12 14:19
# @Author  : houdini
# @File    : GitlabUserEnum.py

import requests
import prettytable
import argparse
import csv

def banner():
    print("""
 ██████╗ ██╗████████╗██╗      █████╗ ██████╗       ███████╗███╗   ██╗██╗   ██╗███╗   ███╗
██╔════╝ ██║╚══██╔══╝██║     ██╔══██╗██╔══██╗      ██╔════╝████╗  ██║██║   ██║████╗ ████║
██║  ███╗██║   ██║   ██║     ███████║██████╔╝█████╗█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║
██║   ██║██║   ██║   ██║     ██╔══██║██╔══██╗╚════╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║
╚██████╔╝██║   ██║   ███████╗██║  ██║██████╔╝      ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
 ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝       ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
                                                                                         
[author: houdini]
[version: 0.1]                                                                                                                       
""")

table_header = ['id', 'name', 'username', 'project_path']

def args():
    parse = argparse.ArgumentParser(prog='GitlabUserEnum.py')
    parse.add_argument('-u', '--url', help='enum target', type=str, required=True)
    parse.add_argument('-r', '--range', help='enum range', type=int, default=100)
    parse.add_argument('-o', '--output', help='output to csv file')
    args = parse.parse_args()
    return args,parse


def show_enum_user():
    table = prettytable.PrettyTable(table_header)
    return table

def user_enum(url, enum_range):
    table = show_enum_user()
    user_number = 0
    enum_data = []
    for user_id in range(1, enum_range+1):
        try:
            enum_url = "{}/api/v4/users/{}".format(url, user_id)
            r = requests.get(enum_url)
            if r.status_code != 404 and r.json()['id']:
                user_number += 1
                user_data = r.json()
                project_path = '{}/{}'.format(url, user_data['username'])
                enum_data.append([user_data['id'], user_data['name'], user_data['username'], project_path])
                table.add_row([user_data['id'], user_data['name'], user_data['username'], project_path])
        except Exception as e:
            print(e)
            break
    print(table)
    print("A total of {} users were found".format(user_number))
    return enum_data


def save_to_csv(export_data, filename):
    with open(filename, 'w', newline='') as file:
        f_csv = csv.writer(file)
        f_csv.writerow(table_header)
        f_csv.writerows(export_data)

if __name__=='__main__':
    banner()
    args = args()
    url = str(args[0].url).strip("/")
    enum_range = args[0].range
    if args[0].url:
        table_data = user_enum(url, enum_range)
        if args[0].output:
            save_to_csv(table_data, args[0].output)

