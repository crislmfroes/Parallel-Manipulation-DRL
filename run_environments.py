import argparse
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument('--parallel_environments', default=2, type=int)
parser.add_argument('--ros_environment', default='turtlebot3_stage_1.launch', type=str)
args = parser.parse_args()


# Opening gazebo environments
for i in range(args.parallel_environments):
    os.system('gnome-terminal --tab --working-directory=WORK_DIR -- zsh -c "export '
              'ROS_MASTER_URI=http://localhost:{}; export GAZEBO_MASTER_URI=http://localhost:{}; roslaunch '
              'turtlebot3_gazebo {}"'.format(11310 + i, 11340 + i, args.ros_environment))
    time.sleep(2)
