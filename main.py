import glob
import random
import os
import datetime
import csv
from PIL import Image

'Variables'
# region Change This

my_order = ['background', 'skincolor', 'mouth', 'eyes', 'hat', 'outfit']
files_path = '/Users/anwhae/PycharmProjects/NFT_CoolFire/output'
nft_names = 'Fire'
number_of_images = 10000
description = 'Make it burn! Cool Fire is a NFT collection of cute fire based on Ethereum blockchain. All NFTs are hand drawn and rare artworks inspired by fire. Hope you like this collection!'
collection = 'Cool_Fire_Official'
duration = ["02-09-2022 14:00", "08-05-2022 14:00"]

# endregion
# region Merging Image Data
prop_list = [f for f in glob.glob('data/*')]
total_time = 0
data = []
my_number = []
# Get only folder names and add to data list
for i in range(len(prop_list)):
    data.append(prop_list[i].split('/')[-1])

# Reorder data list into my order list
for i in range(len(prop_list)):
    my_number.append(data.index(my_order[i]))
data = [data[i] for i in my_number]

# Image path of all possible png files
image_path_data = []
for i in range(len(prop_list)):
    image_path_data.append([f for f in glob.glob('data/'+data[i]+'/*.png')])
# endregion
# region Metadata
metadata = [['file_path', 'nft_name', 'external_link', 'description', 'collection',
             'properties', 'levels', 'stats', 'unlockable_content',
             'explicit_and_sensitive_content', 'supply', 'blockchain', 'sale_type',
             'price', 'method', 'duration', 'specific_buyer', 'quantity']]
ex_link = 'https://opensea.io/Cornelius_Y'
unlockable_content = [False]
explicit_and_sensitive_content = False
supply = 1
blockchain = 'Ethereum'
sale_type = 'Fixed Price'
method = ["Sell to highest bidder", 0.1]
specific_buyer = [False]
quantity = 1
# Open metadata.csv
f = open("metadata.csv", "w")
writer = csv.writer(f, delimiter=';')
# endregion

'Loop'
for j in range(number_of_images):
    start_time = datetime.datetime.now()  # Starting Time Record
    chosen_list = []  # Random Choose
    chosen_metadata = []
    for i in range(len(prop_list)):
        chosen_filename = random.choice(image_path_data[i])
        chosen_list.append(chosen_filename)
        chosen_metadata.append(os.path.splitext(chosen_filename)[0].split('/')[-1])
    im0 = Image.open(chosen_list[0])  # Composite Images
    im1 = Image.open(chosen_list[1])
    final_image = [Image.alpha_composite(im0, im1)]
    for k in range(1, len(prop_list)):
        result = Image.alpha_composite(final_image[0], Image.open(chosen_list[k]))
        final_image = [result]
    final_image[0].save(f'./output/{j}.png')  # Save Image

    '''Make Metadata (file_path, nft_name, properties, levels, stats, price)'''
    file_path = files_path+'/%d.png' % j
    nft_name = nft_names+"_(%d)" % j
    properties = []
    for i in range(len(data)):
        properties.append([data[i], chosen_metadata[i]])
    levels = ['Temperature', random.randint(100, 200), 200]
    stats = ' '
    price = 0.0001 * random.randint(800, 3000)

    '''Add all data to metadata'''
    metadata.append([file_path, nft_name, ex_link, description, collection, properties,
                     levels, stats, unlockable_content, explicit_and_sensitive_content,
                     supply, blockchain, sale_type, price, method, duration, specific_buyer, quantity])
    end_time = datetime.datetime.now()  # End Time Record
    elapsed_time = end_time.minute*60 - start_time.minute*60 + \
        end_time.second + (end_time.microsecond/1000000) - \
        start_time.second - (start_time.microsecond/1000000)
    if elapsed_time < 0:
        pass
    else:
        total_time += elapsed_time  # Total Time Record
    print(f'Processing run id : {j}'+'/' + str(number_of_images)+',',
          'Elapsed time : ' + str(round(elapsed_time, 6)) + ',',
          'Total Time : ' + str(int(total_time//3600))+'h ' + str(int(total_time//60))+'m ' + str(round(total_time % 60, 6)) + 's')

for row in metadata:  # Write metadata
    writer.writerow(row)  # To metadata.csv
f.close()
