from ultralytics import YOLO

def video_inference(vid_path: str) -> list[str]:
    model_path = 'model/best.pt'
    model = YOLO(model_path)

    results = model.predict(
        source=vid_path, # Video path or directory of the image to be predicted
        conf=0.75, 
        save=False, 
        save_txt=False, 
        save_crop=False,
        save_frames=False,
        save_conf=False,
        show=False, 
        device=0,
        visualize=False,
        augment=False, # I am setting it to False because when it's True it's robust, YET at the cost of speed.
        show_labels=False,
        show_conf=False,
        show_boxes=True,
        stream=True, # This is the only difference between video and image inference. Setting stream to True allows the model to process video frames in a streaming manner, which is more efficient for video inference.
    )

    json_dataset = [result.to_json() for result in results]
    return json_dataset

def video_inference_test_run():
    vid_path = 'media/videos/Traffic lights sequence theory test UK part 1.mp4'
    json_dataset = video_inference(vid_path)
    print("JSONified data: ", json_dataset)

video_inference_test_run()