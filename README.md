# Self-Driving Car NanoDegree-Capstone Project

## Description

This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree-Capstone Project: Programming a Real Self-Driving Car. 

## Team Members

This repo is maintained by the following:
* [Team Leader] Mohammed Abdou  (Mohammed.Abdou@valeo.com)
* [Team Member] Bishoy Samy (Bishoy.Zaky@valeo.com) 
* [Team Member] Sandra George (Sandra.George@valeo.com)
* [Team Member] Mohammed Essam (Mohammed.Essam@valeo.com)

## Introduction

For this project, our team designed a fully autonomous vehicle system, initially to be tested out on a simulator, and then on Udacity’s real self-driving car. The project can be broken up into three parts: (1) Waypoint Following techniques, (2) Control, and (3) Traffic Light Detection and Classification as shown in the following figure. The Waypoint Following technique would take information from the traffic light detection and classification with the current waypoints in order to update the target velocities for each waypoint based on this information. For Control part, we designed a drive-by-wire (dbw) node that could take the target linear and angular velocities and publish commands for the throttle, brake, and steering of the car. Finally, Traffic Light Detection and classification, we designed a classification node that would take the current waypoints of the car and an image taken from the car and determine if the closest traffic light was red or green.
 
![alt text](imgs/final-project-ros-graph-v2.png "Capstone Project ROS Graph")

### Waypoint Following

This is considered as a ROS Node that listens or subscribes to (/base_waypoint), (/current_pose), and (/traffic_waypoint) topics in order to generate or publishes (/final_waypoint).

![alt text](imgs/waypoint-updater-ros-graph.png "Waypoint Updater Node")

This part is updated on two phases. The first phase is responsible for generating the final waypoints to make the vehicle moves on straight lines, then depends on the Control part in order to control throttle, steering and brake actions of the Autonomous Vehicle. The Second phase integrates the traffic light detection and classification, so this node subscribes to (/traffic_waypoint) topic. The (/final_waypoint) is updated based on the traffic light color: if RED, the velocity of the vehicle decelerates through the future waypoints, while if GREEN, the velocity accelerates till the Maximum allowable speed through future waypoints.

### Control

This is considered as a ROS Node that subscribes to (/twist_cmd), (/current_velocity), and (/dbw_enabled) topics in order to publishes (/vehicle/steering_cmd), (/vehicle/throttle_cmd), and (/vehicle/brake_cmd).

![alt text](imgs/dbw-node-ros-graph.png "DBW Node")

It is responsible to control the vehicles (throttle, steering, and brake) action commands. We have built a PID controller whose parameters (KP = 0.3, KI = 0.1, KD = 0). This part is called Drive by Wire (dbw) which can be defined as having electric control signal for the main control actions of the vehicle. The brake value is functional of the vehicle mass and the wheel radius calculating the vehcile Torque.

### Traffic Light Detection and Classification

This is considered as a ROS Node that subscribes to (/base_waypoints), (/image_color), and (/current_pose) in order to publishes (/traffic_waypoints).

![alt text](imgs/tl-detector-ros-graph.png "Traffic Light Detection Node")

In this part, our aim is to build a deep learning model to detect the position of the traffic light in the image sent by Carla Simulator, then classify its color if it is RED or GREEN. First of all, we have integrated pre-trained model for Mask RCNN, but when we run the whole pipeline, the waypoints were delayed so much. We calculated the Mask RCNN inference time after freezing its graph, it was approximately = 15 sec on our i5-T520 machine.

This allows us to think about different way instead of a Detection Network, as the detection network takes much time than any other problem in deep learning. Based on our big aim is to classify the color of the traffic light, we thought about searching for traffic light data in order to train simple classification Network  based on its color. We found Bosch traffic light data (https://hci.iwr.uni-heidelberg.de/node/6132) which is labeled on yaml files. Here are an example for the dataset:

![alt text](imgs/TL_example.png "Traffic Light Example")

Now we have the traffic light data, and we need to train a simple classification network (less inference time) that takes the image and output the traffic light color. We know that it will not give the best results, but we have tested it on many frames from the testing data of Bosch and it was working well. In addition to that, we have tested it on some external data and it was working well too.


A fine-tuned MobileNet (https://arxiv.org/pdf/1704.04861.pdf) is offered a good balance between efficiency and accuracy. We depended on the information of stop line locations, so we decided not to use an object detection detection, and instead classify entire images as conraining very simply: RED, YELLOW, or GREEN traffic light. We felt that if we go through object detection task, it will waste our resources especially we don't have powerful machine. We followed in the path of freezing the graph in order to ensure having less inference than detection task. Actually, the inference time = 0.349 sec on our i5-T520 machine which is better than Mask RCNN by 43x enhancement.

![alt text](imgs/MobileNet.png "MobileNet Architecture")

### Vehicle Performance on Unity Simulator

The vehicle is oving Normally on the Simulator:

![alt text](imgs/move.png  "Move Normally")

The vehicle is able to decelerate if the traffic light is RED:

![alt text](imgs/Decelerate.png  "Deceleration")

The vehicle stops while the traffic light is RED: 

![alt text](imgs/stop.png  "Stop")

The vehicle is able to accelerate if the traffic light is GREEN:

![alt text](imgs/Accelerate.png  "Accelerate")


## Conclusion

Autonomous Vehicle System Integration project combines what we have learned in the Self-Driving Car NanoDegree together like: Advanced Deep Learning, path planning, and Control. In addition to that, it allows us to interact with a powerful framework like ROS knowing the concepts of subscribe, and publish. The most interesting part was designing traffic light detection and clasification as it is considered as a realistic problem needed nowadays especially its interaction with the vehicle control actions. Finally, we are so happy to complete this course and very thankful to Udacity for providing us with these information.

## Acknowledgments

We would like to thank Valeo which allows us to enter Self-Driving Car NanoDegree program ang gain all of its information.


## Installation

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND_Term3_Project3_Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone 
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND_Term3_Project3_Capstone.git
```

2. Install python dependencies
```bash
cd CarND_Term3_Project3_Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND_Term3_Project3_Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images
