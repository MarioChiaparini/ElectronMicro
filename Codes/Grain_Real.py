import cv2 
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io, color, measure

image = cv2.imread('../LFP_PÓ_TIFF/10k.tiff', 0)

pixels_to = 0.05

plt.hist(image.flat, bins= 100, range=(0,255))
ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#cv2.imshow("Threshold Image", thresh)
#cv2.waitKey(0)


kernel = np.ones((3,3), np.uint8)
eroded = cv2.erode(thresh, kernel, iterations = 1)
dilated = cv2.dilate(eroded, kernel, iterations = 1)
#cv2.imshow("Dilated Image", dilated)
#cv2

mask = dilated == 255
io.imshow(mask)
io.imshow(image)
s = [[1,1,1], [1,1,1], [1,1,1]]
label_mask, num_labels = ndimage.label(mask, structure=s)
imagem = color.label2rgb(label_mask, bg_label=0)
io.imshow(imagem)
clusters = measure.regionprops(label_mask, image)
clusters[0].perimeter

#for prop in clusters:
#    print("Label: {} Area {}".format(prop.label, prop.area))

proplist = [
    'Area',
    'equivalent_diameter',
    'orientation',
    'MajorAxisLength',
    'MinorAxisLength',
    'Perimeter',
    'MinIntensity',
    'MeanIntensity',
    'MaxIntensity'
]
output_file = open('mev_measurements.csv', 'w')
output_file.write(',' + ','.join(proplist) + '\n')

for clusters_props in clusters:
    output_file.write(str(clusters_props['Label']))
    for i,prop in enumerate(proplist):
        if(prop == 'Area'):
            to_print = clusters_props[prop] * pixels_to**2
        elif(prop == 'orientation'):
            #degrees for radians
            to_print = clusters_props[prop] * 52.2958
        elif(prop.find('Intensity') < 0):
            to_print = clusters_props[prop] * pixels_to
        else:
            to_print = clusters_props[prop]
        output_file.write(',' + str(to_print))
    output_file.write('\n')