from Detector import *
import os

def main():
    videoPath = "test_videos/street2.mp4" # For webcam, replace this with 0

    configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("model_data", "coco.names")

    detector = Detector(videoPath, configPath, modelPath, classesPath)
    a = detector.onVideo(showVideo = True, writeVideo=True)
    print(a)
if __name__ == '__main__':
    main()