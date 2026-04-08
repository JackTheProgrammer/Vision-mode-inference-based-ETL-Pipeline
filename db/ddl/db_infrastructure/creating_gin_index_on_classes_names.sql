CREATE INDEX idx_classes_names 
ON video_inference_analytics
USING GIN (class_name);
