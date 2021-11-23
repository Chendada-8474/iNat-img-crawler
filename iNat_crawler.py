from urllib.request import urlretrieve
from easygui import fileopenbox, multchoicebox, ccbox, msgbox
from os import mkdir, listdir
from numpy import NaN
from tqdm import tqdm
import pandas as pd
from time import sleep
from random import uniform
import sys


# get file path and read csv
while True:

    print("Please select the csv file downloaded from iNat.")
    path = fileopenbox()

    if path == None:
        sys.exit(0)
    elif path[-4:] == '.csv':
        break
    else:
        msgbox('Please select "CSV" file\nselect again')

path = path.replace('\\', '/')
inat = pd.read_csv(path)

needed_col = ('id', 'user_login', 'license', 'image_url', 'scientific_name', 'common_name')

# check the columns are right
lack_col = [i for i in needed_col if i not in inat.columns]
if len(lack_col) > 0:
    msgbox("Your file lacks columns:\n%s," % ',\n'.join(lack_col))
    sys.exit(0)

# CC selector
while True:
    print('Please select the cc license via the "CC selector window"')
    msg = 'Please select the CC license\n\nCC license explanation:\nBY: Attribution\nNC: Noncommercial\nSA: ShareAlike\nND: No Derivative\n\nPLEASE NOTE the legal issue of the "All right reserved"'
    title = "CC selector"
    choices = ('CC0', 'CC-BY', 'CC-BY-NC', 'CC-BY-NC-SA', 'CC-BY-NC-ND', 'CC-BY-ND', 'CC-BY-SA', 'All rights reserved')
    cc = multchoicebox(msg, title, choices, preselect=None)

    if cc == None:
        none_check = ccbox("You selected nothing or clicked the cancel botton.\nCancel or Continue?")

        if none_check == False:
            sys.exit(0)
    else:
        break

for i,j in enumerate(cc):
    if j == 'All rights reserved':
        cc[i] = NaN


# caculating the number of images will be downloaded
checked_sp = []
ids = []

print("Caculating number of img...")
for index, row in inat.iterrows():
    if row['scientific_name'] in checked_sp or row['image_url'] == '' or row['common_name'] == '' or row['license'] not in cc:
        continue
    checked_sp.append(row['scientific_name'])
    ids.append(row['id'])

image_num_check = ccbox('Total %i images will be downloaded\nContinue?' % len(ids))

if image_num_check == False:
    sys.exit(0)

# download start
print("downloading images... It may take a while")
print("Total_row:", len(ids))

# make a dir under same diraction. if dir exist, it make a new one.
dir_index = 1
if "iNat-img" in listdir('./'):
    while True:
        if "iNat-img-%s" % dir_index in listdir('./'):
            dir_index = dir_index + 1
        else:
            dir_name = 'iNat-img-%s' % dir_index
            mkdir('./%s' % dir_name)
            break

else:
    dir_name = 'iNat-img'
    mkdir('./%s' % dir_name)

for index, row in tqdm(inat[inat['id'].isin(ids)].iterrows()):

#file name rules: 'iNat id'_'common name'_by-'iNat user id'.jpg
    urlretrieve('%s' % row['image_url'], "./%s/%s_%s_by-%s.jpg" % (dir_name, row['id'],row['common_name'], row['user_login']))

    checked_sp.append(row['scientific_name'])
    sleep(uniform(0,1))

print("All the images have been downloaded. Program will exit in 3s.\nBYE BYE!")
sleep(3)
