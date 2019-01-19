# BEng Project - Autonomous vehicle movement with sensor fusion and probabilistic methods

This is a project that uses multiple sensors on a robot chassis to make an autonomous vehicle through sensor fusion.

The sensors are:
 - IMU (Inertial Measurement Unit) -> Accelerometer, gyroscope and magnetometer providing various outputs including linear acceleration, quaterions and more
 - Encoders -> Hall effect encoders fitted to DC motors. Provide relative motion of each motor, allowing relative position to be determined
 - Camera -> Camera positioned above the 'map' providing absolute position of the robot through image processing. Connected to a secondary raspberry pi
 - Lidar -> An inexpensive 360-degree Lidar module (RPLidar A1M8) that provides obstacle detection data to be used for autonomous vehicle movement. Also, potentially will be used as a fourth sensor to be included in a Kalman filter

In the project, I will be using a Kalman filter to provide sensor fusion of multiple imperfect sensors. The filter will have a prediction (a priori) step which is determined through development of two state space models for position from the IMU and encoders. Next, the filter performs a correction (a posteriori) step which is formed from an absolute measurement of the robot position, which is achieved by the camera (and possible the Lidar).

The main challenges are:
 - development of the state space models for the dynamic motion of the robot
 - implementing computer vision with computational efficiency and achieving a high enough sensor frequency (initially targeting 30Hz, since 30fps camera)
 - using linear algebra to develop the Kalman filter equations with data from multiple asynchronous sensors and implementing this in code
 - accurately obtaining optimal estimates of position by reducing uncertainty of sensors through sensor fusion
 - using the acquired position estimates combined with obstacle detection and avoidance algorithms with the Lidar to achieve autonomous vehicle movement

