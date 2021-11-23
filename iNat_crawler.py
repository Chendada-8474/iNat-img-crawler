from urllib.request import urlretrieve
from easygui import fileopenbox
from os import mkdir, listdir
from tqdm import tqdm
import pandas as pd
from time import sleep
from random import uniform

print("Please select the csv file downloaded from iNat.")
path = fileopenbox()
path = path.replace('\\', '/')
print(path)

inat = pd.read_csv(path)

dir_index = 1

if "iNat-img" in listdir('./'):
    while True:
        if "iNat-img-%s" % dir_index in listdir('./'):
            dir_index = dir_index + 1
        else:
            dir_name = 'iNat-img-%s' % dir_index
            break

else:
   dir_name = 'iNat-img'

mkdir('./%s' % dir_name)

checked_sp = []

print("downloading images... It may take a while")
print("Total_row:", len(list(inat['scientific_name'])))

img_id = 1
for i in tqdm(zip(inat['scientific_name'], inat['image_url'], inat['common_name'])):
    if i[0] in checked_sp or i[1] == '' or i[2] == '':
        continue

    if img_id < 10:
        urlretrieve('%s' % i[1], "./%s/dada000%s_%s.jpg" % (dir_name, img_id,i[2]))
    elif img_id > 9 and img_id < 100:
        urlretrieve('%s' % i[1], "./%s/dada00%s_%s.jpg" % (dir_name, img_id,i[2]))
    elif img_id > 99 and img_id < 1000:
        urlretrieve('%s' % i[1], "./%s/dada0%s_%s.jpg" % (dir_name, img_id,i[2]))
    if img_id > 999 and img_id < 10000:
        urlretrieve('%s' % i[1], "./%s/dada%s_%s.jpg" % (dir_name, img_id,i[2]))
    img_id = img_id +1

    checked_sp.append(i[0])
    sleep(uniform(0,1))

input("All the images have been downloaded. input any key to end this program:")



