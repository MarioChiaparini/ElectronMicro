import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io, color, measure
import sys

# Check if correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python Grain_Real.py <image_path> <output_csv_path>")
    sys.exit(1)

# Read the image file from the first argument
image_path = sys.argv[1]
image = cv2.imread(image_path, 0)

# Output CSV path from the second argument
output_csv_path = sys.argv[2]

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

with open(output_csv_path, 'w') as output_file:
    output_file.write(',' + ','.join(proplist) + '\n')
    
    for clusters_props in clusters:
        output_file.write(str(clusters_props.label))
        for i, prop in enumerate(proplist):
            #to_print = getattr(clusters_props, prop.replace('Intensity', 'intensity'))  # Adjusting to correct attribute names
            if prop == 'Area':
                to_print *= pixels_to**2
            elif prop == 'orientation':
                # degrees from radians
                to_print *= 57.2958  # Correcting the conversion factor for radians to degrees
            elif 'Intensity' in prop:
                to_print *= pixels_to
            output_file.write(',' + str(to_print))
        output_file.write('\n')
