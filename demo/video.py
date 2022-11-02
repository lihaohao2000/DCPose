#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import os.path as osp
import sys

sys.path.insert(0, osp.abspath('../'))

from tqdm import tqdm
import logging

from datasets.process.keypoints_ord import coco2posetrack_ord_infer
from tools.inference import inference_PE
from object_detector.YOLOv3.detector_yolov3 import inference_yolov3
from utils.utils_folder import list_immediate_childfile_paths
from utils.utils_video import video2images


zero_fill = 8

logger = logging.getLogger(__name__)


def main():
    video()


def video():
    logger.info("Start")
    base_video_path = "./input"
    image_save_base = "./image"
    train_video_path = osp.join(base_video_path,"train")
    validate_video_path = osp.join(base_video_path,"validate")
    train_video_list = [list_immediate_childfile_paths(osp.join(train_video_path,temp), ext=['mp4']) for temp in os.listdir(train_video_path)]
    train_video_list = [i for item in train_video_list for i in item]
    validate_video_list = list_immediate_childfile_paths(validate_video_path, ext=['mp4'])
    train_image_save_dirs = []
    validate_image_save_dirs = []
    dic_images2video = {}
    # 1.Split the video into images
    print("1.Split the video into images")
    for video_path in tqdm(train_video_list):
        video_name = osp.basename(video_path)
        temp = video_name.split(".")[0]
        image_save_path = os.path.join(image_save_base, temp)
        train_image_save_dirs.append(image_save_path)
        dic_images2video[image_save_path] = video_path
        if osp.exists(image_save_path):
            continue
        video2images(video_path, image_save_path)  # jpg

    for video_path in tqdm(validate_video_list):
        video_name = osp.basename(video_path)
        temp = video_name.split(".")[0]
        image_save_path = os.path.join(image_save_base, temp)
        validate_image_save_dirs.append(image_save_path)
        dic_images2video[image_save_path] = video_path
        if osp.exists(image_save_path):
            continue
        video2images(video_path, image_save_path)  # jpg

    # 2. Person Instance detection
    print("2. Person Instance detection")
    logger.info("Person Instance detection in progress ...")
    video_candidates = {}
    for index, images_dir in tqdm(enumerate(train_image_save_dirs)):
        video_name = osp.basename(images_dir)
        image_list = list_immediate_childfile_paths(images_dir, ext='jpg')
        video_candidates_list = []
        for image_path in tqdm(image_list):
            candidate_bbox = inference_yolov3(image_path)
            for bbox in candidate_bbox:
                # bbox  - x, y, w, h
                video_candidates_list.append({"image_path": image_path,
                                              "bbox": bbox,
                                              "keypoints": None})
                break   #just take one bbox
        video_candidates[video_name] = {"candidates_list": video_candidates_list,
                                        "length": len(image_list)}

    for index, images_dir in tqdm(enumerate(validate_image_save_dirs)):
        video_name = osp.basename(images_dir)
        image_list = list_immediate_childfile_paths(images_dir, ext='jpg')
        video_candidates_list = []
        for image_path in tqdm(image_list):
            candidate_bbox = inference_yolov3(image_path)
            for bbox in candidate_bbox:
                # bbox  - x, y, w, h
                video_candidates_list.append({"image_path": image_path,
                                              "bbox": bbox,
                                              "keypoints": None})
                break   #just take one bbox
        video_candidates[video_name] = {"candidates_list": video_candidates_list,
                                        "length": len(image_list)}                                  
    logger.info("Person Instance detection finish")


    # 3. Singe Person Pose Estimation
    dic_video2TF = {}
    with open("train.txt") as f:
        lines = f.read().splitlines()
        logging.info("VideoIter:: found {} videos in `{}'".format(len(lines), "train.txt"))
        for i, line in enumerate(lines):
            v_id, label, video_subpath = line.split()
            video_path = os.path.join(train_video_path, video_subpath)
            if not os.path.exists(video_path):
                logging.warning("VideoIter:: >> cannot locate `{}'".format(video_path))
                continue
            dic_video2TF[video_path] = label
    with open("validate.txt") as f:
        lines = f.read().splitlines()
        logging.info("VideoIter:: found {} videos in `{}'".format(len(lines), "validate.txt"))
        for i, line in enumerate(lines):
            v_id, label, video_subpath = line.split()
            video_path = os.path.join(train_video_path, video_subpath)
            if not os.path.exists(video_path):
                logging.warning("VideoIter:: >> cannot locate `{}'".format(video_path))
                continue
            dic_video2TF[video_path] = label

    print("3. Singe Person Pose Estimation")
    logger.info("Single person pose estimation in progress ...")
    pose_estimatated_list = []
    HAR_label_list = []
    for video_name, video_info in video_candidates.items():
        pose_estimatated_seq = []
        video_candidates_list = video_info["candidates_list"]
        video_length = video_info["length"]
        for person_info in tqdm(video_candidates_list):
            image_path = person_info["image_path"]
            xywh_box = person_info["bbox"]
            image_idx = int(os.path.basename(image_path).replace(".jpg", ""))
            prev_idx, next_id = image_idx - 1, image_idx + 1
            if prev_idx < 0:
                prev_idx = 0
            if image_idx >= video_length - 1:
                next_id = video_length - 1
            prev_image_path = os.path.join(os.path.dirname(image_path), "{}.jpg".format(str(prev_idx).zfill(zero_fill)))
            next_image_path = os.path.join(os.path.dirname(image_path), "{}.jpg".format(str(next_id).zfill(zero_fill)))


            bbox = xywh_box
            keypoints = inference_PE(image_path, prev_image_path, next_image_path, bbox)
            # person_info["keypoints"] = keypoints.tolist()[0]

            #posetrack points
            mid_coord = coco2posetrack_ord_infer(keypoints[0])
            print (mid_coord)
            exit()
            #coord change
            # new_coord = changeCoord(mid_coord)
            
            pose_estimatated_seq.append(new_coord)
        pose_estimatated_list.append(pose_estimatated_seq)
        HAR_label_list.append(dic_video2TF[dic_images2video[osp.join(image_save_base,video_name)]])




# def changeCoord(old_corrd):
#     new_coord = []
#     new_coord.append(old_corrd[0])

            
                    

        

     
            

        


if __name__ == '__main__':
    main()
