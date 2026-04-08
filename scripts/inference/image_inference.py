from ultralytics import YOLO

def image_inference(image_path: str) -> list[str]:
    """
    Runs inference on an image and returns a list of JSONified results.
    Each JSONified result contains the following keys:
    - 'boxes': a list of bounding boxes, where each bounding box is a list of
        [x_min, y_min, x_max, y_max] coordinates
    - 'scores': a list of confidence scores for each bounding box
    - 'class_ids': a list of class IDs for each bounding box
    """
    
    model_path = 'model/best.pt'
    model = YOLO(model_path)

    results = model.predict(
        source=image_path, 
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
    )

    json_results = [result.to_json() for result in results]
    return json_results

def image_inference_test_run():
    image_path = 'media/photos/20221120_165722_jpg.rf.730d6ef7f112828c75e429b714c633ff.jpg'
    json_results = image_inference(image_path=image_path)
    print("JSONified results: ", json_results)

image_inference_test_run()