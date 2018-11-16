import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
from random import randint

ascii_img = Image.open("ascii.png");
ascii_img = ascii_img.convert(mode='L')

chars = ['!','"','#','$','%','&','\'','(',')','*','+',',','-','.','/',
         '0','1','2','3','4','5','6','7','8','9',':',';','<','=','>',
         '?','@','A','B','C','D','E','F','G','H','I','J','K','L','M',
         'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[','\\',
         ']','^','_','`','a','b','c','d','e','f','g','h','i','j','k',
         'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
         '{',':','}','~']
values = []
crops = []
for i in range(len(chars)):  
    white = 0
    crop = ascii_img.crop((i*8, 0, i*8+8, ascii_img.height))
    crops.append(crop)
    crop_array = np.array(crop)
    for row in crop_array:
        for pixel in row:
            if (pixel != 0):
                white += 1
    values.append((chars[i], round(white/45,5)))
values.append((' ', 0))

from operator import itemgetter
values.sort(key=itemgetter(1),reverse=False)

values_map = []
value_indexes = []
for tup in values:
    if tup[1] not in value_indexes:
        values_map.append((tup[1], [tup[0]]))
        value_indexes.append(tup[1])
    else:
        index = value_indexes.index(tup[1])
        values_map[index][1].append(tup[0])

org_img = Image.open("panda.jpg")
org_img = org_img.convert(mode='L')
org_img_mat = np.array(org_img)

def find_nearest(val_map, value):
    value = value/255
    result = (val_map[0][0], 0)
    i = 0
    for tup in val_map:
        if (np.abs(value - tup[0]) < np.abs(value - result[0])):
            result = (tup[0], i)
        i += 1
    return result[1]

def naive_ascii(org_img, step_size_rows, step_size_cols):
    org_img_mat = np.array(org_img)
    org_img_ascii_mat = np.zeros([int(org_img.height/step_size_rows), int(org_img.width/step_size_cols)])
    height = org_img.height
    width = org_img.width
    
    for i in range(0,height,step_size_rows):
        for j in range(0,width,step_size_cols):
            nearest_index = find_nearest(values_map,org_img_mat[i][j])
            rand_char_index = randint(0,len(values_map[nearest_index][1])-1)
            org_img_ascii_mat[int(i/step_size_rows)][int(j/step_size_cols)] = ord(values_map[nearest_index][1][rand_char_index])

    for row in org_img_ascii_mat:
        row_string = ""
        for pixel in row:
            row_string += chr(int(pixel))
        print(row_string)

def avg_ascii(org_img, step_size_rows, step_size_cols):
    org_img_mat = np.array(org_img)
    org_img_ascii_mat = np.zeros([int(org_img.height/step_size_rows), int(org_img.width/step_size_cols)])
    height = org_img.height
    width = org_img.width
    
    for i in range(0,height-1,step_size_rows):
        for j in range(0,width-1,step_size_cols):
            sum = int(org_img_mat[i][j]) + int(org_img_mat[i+1][j]) + int(org_img_mat[i][j+1]) + int(org_img_mat[i+1][j+1])
            nearest_index = find_nearest(values_map,sum/4)
            rand_char_index = randint(0,len(values_map[nearest_index][1])-1)
            org_img_ascii_mat[int(i/step_size_rows)][int(j/step_size_cols)] = ord(values_map[nearest_index][1][rand_char_index])

    for row in org_img_ascii_mat:
        row_string = ""
        for pixel in row:
            row_string += chr(int(pixel))
        print(row_string)

naive_ascii(org_img, 5, 2)