SELECT detected_obj_class_name, 
max(detected_obj_confidence) as max_conf
FROM public.video_inferenced_analytics_flattened
GROUP BY detected_obj_class_name, detected_obj_confidence
ORDER BY detected_obj_confidence DESC
LIMIT 5;