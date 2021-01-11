# MBotFollower

This repository contains the code for a line following robot designed as a final project for UCF's EEL4660 Robotic Systems.

For more information, see the brief [writeup submitted with our project](https://github.com/c-bujari/MBotFollower/blob/main/project-writeup.pdf) or [demo video](https://youtu.be/2XrjXeWvylg).

The robot is built from a variety of different parts (including the chassis and motors from an old [MBot](https://www.makeblock.com/mbot/) kit, hence the name). The robot is controlled by a Raspberry Pi 4, which uses CV2 to analyze video feed from its camera, determining the required motor output to remain on-track.

This code should, in theory, work with any Raspberry Pi and camera with Python 3 and CV2 installed. You may need to do a bit of extra work to install CV2; the default packages in Raspbian have issues and largely seem to not work.
