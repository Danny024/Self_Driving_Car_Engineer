# Mid Project Report
## 3D Object Detection Project
### Section 1 :Compute Lidar Point Cloud from Range 
1.1 (ID_S1_EX1):
We visualize the range image below as seen below:
![Range Image](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/range_image.png)

1.2 ID_S1_EX2
The example of vehicles as seen from the point cloud can be seen below
The below are images of vehicles as seeen in the point cloud
![Point Cloud with images](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/sequence3_with_pcl.png)

![Point Cloud with Images2](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/image_and_pcl.png)

- The stable vehicle features as see in the point cloud above are :
   
- **Shape of Vehicles** : As seen in the image above the vehicles's front and behind can be seen in the point cloud. The hood and bumper are clearly visible. The shape of the truck can also be seen in the image below. The geometric outline of the cars can be visibly seen from the point cloud.From the features like the roofline and the sides up to the windows and doors, you can  tell the overall shape of the vehicle. This shape is key for distinguishing various vehicle types; it’s  good for telling whether it’s a truck, sedan, or SUV.
 
- **Car Wheels and Tyres**:  The circular features at the base of each vehicle are the wheels. Depending on the LiDAR's angle from where it is positioned, the tyres and wheels pf vehicles can be seen to appear as circles or segments in point cloud data. Wheel is a reliable indicator  for vehicle identification as they are of consistent shape and are positioned predictably across vehicle categories such as the cars and the trucks.

- **Alignment and Wheel Spacing of Vehicles**: The spacing and arrangement of the wheels provide size additional and information type. regarding For the example, vehicle’s a  greater distance between the front and rear wheels is often a characteristic  of longer vehicles such as seen in the sedans or the SUVs.


### Section 2: Create Birds-Eye View from LiDAR Point Cloud 
The BEV image height and intensity can be seen in the image below
The Bird Eye View Point cloud 

The image height result of the BEV

![Image height bev](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/image_height_bev.png)

The image intensity map of the BEV

![Intensity Map](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/intensity_map.png)


### Section 3: Model-Based Object Detection Bird's Eye View Image
The BEV Point Cloud and the detected objects can be seen below
The Image label as seen below:

![Image Label](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/image_results/frame_0.png)

The label and the detected objects can be seen in the figure below

![labels and dtetected objects](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/labelsvsobjects.png)

### Section 4: Performance Evaluation for object Detection
The performance of the model for the sequence for the sequence `training_segment-1005081002024129653_5313_150_5333_150_with_camera_labels.tfrecord` and frames [0,200] is 
precision = 0.9539473684210527, recall = 0.9477124183006536
![Metrics](https://github.com/Danny024/Self_Driving_Car_Engineer/blob/main/P2_3D_Object_Detection/nd013-c2-fusion-starter/image_results/mid_project/metrics.png)
