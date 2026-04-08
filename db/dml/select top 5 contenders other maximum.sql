SELECT detected_obj_class_name, detected_obj_confidence
FROM public.video_inferenced_analytics_flattened viaf
WHERE viaf.detected_obj_confidence <> (
	SELECT max(detected_obj_confidence)
	FROM public.video_inferenced_analytics_flattened
)
ORDER BY detected_obj_confidence DESC
LIMIT 5;