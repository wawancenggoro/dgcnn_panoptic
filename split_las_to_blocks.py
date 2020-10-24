import laspy
import numpy as np
import gdal
from osgeo import osr
import os
import h5py

hf = h5py.File('ahn3_blocks.h5', 'w')

for filename in ['C_38FN1.las']:
# for filename in ['C_38FN1.las', 'C_37EN2.las', 'C_32CN1.las', 'C_37FZ1.las', 'C_31HZ2.las']:
    print("membuka file "+filename)

    inFile = laspy.file.File("../"+filename, mode = "r")
    #mengambil nilai fitur
    print("mengambil nilai x")
    points_x = inFile.x
    print("mengambil nilai y")
    points_y = inFile.y
    print("mengambil nilai z")
    points_z = inFile.z
    print("mengambil nilai intensity")
    points_intensity = inFile.intensity
    print("mengambil nilai return number")
    points_return_num = inFile.return_num
    print("mengambil nilai number of returns")
    points_num_returns = inFile.num_returns
    print("mengambil nilai classification")
    points_classification = inFile.classification

    x_min = int(np.floor(points_x.min()))
    x_max = int(np.floor(points_x.max()))
    y_min = int(np.floor(points_y.min()))
    y_max = int(np.floor(points_y.max()))        
    range_x_min = x_min - 1000
    range_x_max = x_max + 1001
    range_y_min = y_min - 1000
    range_y_max = y_max + 1001
    range_x = int((range_x_max - range_x_min) / 10)
    range_y = int((range_y_max - range_y_min) / 10)
    dist_x = int((range_x_max - range_x_min)/range_x)
    dist_y = int((range_y_max - range_y_min)/range_y)
    num_points = points_x.shape[0]

    # buat dataset hdf5
    print("Membuat dataset")
    for i in range(dist_y):
        for j in range(dist_x):
        	hf.create_dataset(filename+"_block_"+str(j)+"_"+str(i), (0,7), maxshape=(num_points, 7))        	

    #looping setiap titik
    for y in range(num_points):
        print('menyimpan point ke-{} dari {} point'.format(y,num_points))
        range_y_min_full = range_y_min
        #looping block sepanjang axis y
        for i in range(dist_y):
            print(i)
            range_y_min_range = range_y_min_full
            range_y_min_full = range_y_min_range + range_y
            range_x_min_full = range_x_min
            #looping block sepanjang axis x
            for j in range(dist_x):
                print(j)
                range_x_min_range = range_x_min_full
                range_x_min_full = range_x_min_range + range_x
                if points_x[y] <= range_x_min_full and points_x[y] > range_x_min_range and points_y[y] <= range_y_min_full and points_y[y] > range_y_min_range:
                    allx, ally, allz, allintensity, allreturnnum, allnumreturns, allclass = [], [], [], [], [], [], []
                    
                    dset = hf[filename+"_block_"+str(j)+"_"+str(i)]
                    dset.resize((dset.shape[0]+1,dset.shape[1]))
                    dset[-1] = np.array([points_x[y], points_y[y], points_z[y], points_intensity[y], points_return_num[y], points_num_returns[y], points_classification[y]])