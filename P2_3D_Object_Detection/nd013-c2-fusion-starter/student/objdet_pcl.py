# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Process the point-cloud and prepare it for object detection
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# general package imports
import cv2
import numpy as np
import torch
import zlib
import open3d as o3d

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# waymo open dataset reader
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils
from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2

# object detection tools and helper functions
import misc.objdet_tools as tools


# visualize lidar point-cloud
def show_pcl(pcl):

    ####### ID_S1_EX2 START #######     
    #######
    print("student task ID_S1_EX2")

    # step 1 : initialize open3d with key callback and create window
    visualizer = o3d.visualization.VisualizerWithKeyCallback()
    visualizer.create_window()

    
    # step 2 : create instance of open3d point-cloud class
    point_cloud = o3d.geometry.PointCloud()

    # step 3 : set points in pcd instance by converting the point-cloud into 3d vectors (using open3d function Vector3dVector)
    point_cloud.points = o3d.utility.Vector3dVector(pcl[:, :3])

    # step 4 : for the first frame, add the pcd instance to visualization using add_geometry; for all other frames, use update_geometry instead
    visualizer.add_geometry(point_cloud)
    # step 5 : visualize point cloud and keep window open until right-arrow is pressed (key-code 262)
    def on_key_press(visualizer_instance):
        #update the visualization with the current geometry and refresh the window
        visualizer_instance.update_geometry(point_cloud)
        visualizer_instance.poll_events()
        visualizer_instance.update_renderer()

   # Register the callback function for the right-arrow key 
    visualizer.register_key_callback(262, on_key_press)

    # step 5: Start the visualization loop
    visualizer.run()
    visualizer.destroy_window()

    #######
    ####### ID_S1_EX2 END #######     
       

# visualize range image
def show_range_image(frame, lidar_name):

    ####### ID_S1_EX1 START #######     
    #######
    print("student task ID_S1_EX1")

    # step 1 : extract lidar data and range image for the roof-mounted lidar
    lidar_data = next((laser for laser in frame.lasers if laser.name == lidar_name), None)
    if lidar_data and len(lidar_data.ri_return1.range_image_compressed) > 0:
        compressed_data = lidar_data.ri_return1.range_image_compressed
        decompressed_data = zlib.decompress(compressed_data)
        range_image = dataset_pb2.MatrixFloat()
        range_image.ParseFromString(decompressed_data)
        range_image = np.array(range_image.data).reshape(range_image.shape.dims)
    else:
        raise ValueError ("No valid range image is found for the lidar sensor")


    
    # step 2 : extract the range and the intensity channel from the range image
    range_channel = range_image[:, :, 0]
    intensity_channel = range_image [:, :, 1]
    
    # step 3 : set values <0 to zero
    range_channel[range_channel < 0] = 0.0
    
    # step 4 : map the range channel onto an 8-bit scale and make sure that the full range of values is appropriately considered
    range_min , range_max = np.amin(range_channel), np.amax(range_channel)
    scaled_range = (range_channel - range_min) * 255 / (range_max - range_min)
    range_image_8bit = scaled_range.astype(np.uint8)

    # step 5 : map the intensity channel onto an 8-bit scale and normalize with the difference between the 1- and 99-percentile to mitigate the influence of outliers
    intensity_min, intensity_max = np.percentile(intensity_channel, [1, 99])
    intensity_channel = np.clip(intensity_channel, intensity_min, intensity_max)
    scaled_intensity = (intensity_channel - intensity_min) * 255 / (intensity_max - intensity_min)
    intensity_image_8bit = scaled_intensity.astype(np.uint8)
    
    # step 6 : stack the range and intensity image vertically using np.vstack and convert the result to an unsigned 8-bit integer
    stacked_image = np.vstack((range_image_8bit, intensity_image_8bit))
    
    #center region 
    center = stacked_image.shape[1] // 2
    half_width = stacked_image.shape[1] // 4
    img_range_intensity = stacked_image[:, center - half_width:center + half_width]
    #######
    ####### ID_S1_EX1 END #######     
    
    return img_range_intensity


# create birds-eye view of lidar data
def bev_from_pcl(lidar_pcl, configs):

    # remove lidar points outside detection area and with too low reflectivity
    mask = np.where((lidar_pcl[:, 0] >= configs.lim_x[0]) & (lidar_pcl[:, 0] <= configs.lim_x[1]) &
                    (lidar_pcl[:, 1] >= configs.lim_y[0]) & (lidar_pcl[:, 1] <= configs.lim_y[1]) &
                    (lidar_pcl[:, 2] >= configs.lim_z[0]) & (lidar_pcl[:, 2] <= configs.lim_z[1]))
    lidar_pcl = lidar_pcl[mask]
    
    # shift level of ground plane to avoid flipping from 0 to 255 for neighboring pixels
    lidar_pcl[:, 2] = lidar_pcl[:, 2] - configs.lim_z[0]  

    # convert sensor coordinates to bev-map coordinates (center is bottom-middle)
    ####### ID_S2_EX1 START #######     
    #######
    print("student task ID_S2_EX1")

    ## step 1 :  compute bev-map discretization by dividing x-range by the bev-image height (see configs)
    bev_resolution = (configs.lim_x[1] - configs.lim_x[0]) / configs.bev_height


    ## step 2 : create a copy of the lidar pcl and transform all metrix x-coordinates into bev-image coordinates   
    lidar_pcl_cpy= np.copy(lidar_pcl) 
    lidar_pcl_cpy[:,0] = np.int_(np.floor(lidar_pcl_cpy[:, 0] / bev_resolution))


    # step 3 : perform the same operation as in step 2 for the y-coordinates but make sure that no negative bev-coordinates occur
    lidar_pcl_cpy[:, 1] = np.int_(np.floor((lidar_pcl_cpy[:,1] - configs.lim_y[0]) / bev_resolution))

    # step 4 : visualize point-cloud using the function show_pcl from a previous task
    #show_pcl(lidar_pcl_cpy)
    
    #######
    ####### ID_S2_EX1 END #######     
    
    
    # Compute intensity layer of the BEV map
    ####### ID_S2_EX2 START #######     
    #######
    print("student task ID_S2_EX2")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    intensity_map = np.zeros ((configs.bev_height + 1, configs.bev_height + 1))

    # step 2 : re-arrange elements in lidar_pcl_cpy by sorting first by x, then y, then -z (use numpy.lexsort)
    lidar_pcl_cpy[lidar_pcl_cpy[:, 3] > 1.0, 3] = 1.0
    sorted_indices = np.lexsort((-lidar_pcl_cpy[:,3], lidar_pcl_cpy[:,1], lidar_pcl_cpy[:,0]))
    sorted_lidar_pcl = lidar_pcl_cpy[sorted_indices]
    ## step 3 : extract all points with identical x and y such that only the top-most z-coordinate is kept (use numpy.unique)
    ##          also, store the number of points per x,y-cell in a variable named "counts" for use in the next task
    _, unique_indices, point_counts = np.unique(sorted_lidar_pcl[:, 0:2], axis=0, return_index=True, return_counts=True)
    lidar_pcl_top = sorted_lidar_pcl[unique_indices]

    ## step 4 : assign the intensity value of each unique entry in lidar_top_pcl to the intensity map 
    ##          make sure that the intensity is scaled in such a way that objects of interest (e.g. vehicles) are clearly visible    
    ##          also, make sure that the influence of outliers is mitigated by normalizing intensity on the difference between the max. and min. value within the point cloud
    normalized_intensity = (
        lidar_pcl_top[:,3] / (np.max(lidar_pcl_top[:,3]) - np.amin(lidar_pcl_top[:, 3]))

    )
    intensity_map[np.int_(lidar_pcl_top[:, 0]), np.int_(lidar_pcl_top[:,1])] = normalized_intensity


    ## step 5 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    intensity_image = (intensity_map * 256).astype(np.uint8)

    # while True:
    #     cv2.imshow('Intensity Map', intensity_image)
    #     if cv2.waitKey(10) & 0xFF == 27: #Press 'Esc' to exit
    #         break
    # cv2.destroyAllWindows()
    #######
    ####### ID_S2_EX2 END ####### 


    # Compute height layer of the BEV map
    ####### ID_S2_EX3 START #######     
    #######
    print("student task ID_S2_EX3")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    height_map = np.zeros((configs.bev_height + 1, configs.bev_width + 1))

    ## step 2 : assign the height value of each unique entry in lidar_top_pcl to the height map 
    ##          make sure that each entry is normalized on the difference between the upper and lower height defined in the config file
    ##          use the lidar_pcl_top data structure from the previous task to access the pixels of the height_map
    height_map[np.int_(lidar_pcl_top[:,0]), np.int_(lidar_pcl_top[:,1])] = lidar_pcl_top[:,2] / float (np.abs(configs.lim_z[1] - configs.lim_z[0]))

    ## step 3 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    image_height = height_map * 256
    image_height = image_height.astype(np.uint8)

    #######
    ####### ID_S2_EX3 END #######       

    # TODO remove after implementing all of the above steps
    # while True:
    #     cv2.imshow('Image height', image_height)
    #     if cv2.waitKey(10) & 0xFF == 27:
    #         break
    # cv2.destroyAllWindows()

    # Compute density layer of the BEV map
    density_map = np.zeros((configs.bev_height + 1, configs.bev_width + 1))
    _, _, counts = np.unique(lidar_pcl_cpy[:, 0:2], axis=0, return_index=True, return_counts=True)
    normalizedCounts = np.minimum(1.0, np.log(counts + 1) / np.log(64)) 
    density_map[np.int_(lidar_pcl_top[:, 0]), np.int_(lidar_pcl_top[:, 1])] = normalizedCounts
        
    # assemble 3-channel bev-map from individual maps
    bev_map = np.zeros((3, configs.bev_height, configs.bev_width))
    bev_map[2, :, :] = density_map[:configs.bev_height, :configs.bev_width]  # r_map
    bev_map[1, :, :] = height_map[:configs.bev_height, :configs.bev_width]  # g_map
    bev_map[0, :, :] = intensity_map[:configs.bev_height, :configs.bev_width]  # b_map

    # expand dimension of bev_map before converting into a tensor
    s1, s2, s3 = bev_map.shape
    bev_maps = np.zeros((1, s1, s2, s3))
    bev_maps[0] = bev_map

    bev_maps = torch.from_numpy(bev_maps)  # create tensor from birds-eye view
    input_bev_maps = bev_maps.to(configs.device, non_blocking=True).float()
    return input_bev_maps


