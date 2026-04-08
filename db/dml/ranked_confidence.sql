SELECT detected_obj_class_name, detected_obj_confidence
FROM (
	SELECT *, DENSE_RANK() OVER 
	(ORDER BY detected_obj_confidence DESC)
	AS ranked_confidence
	FROM public.video_inferenced_analytics_flattened
) AS ranked_viaf
WHERE ranked_confidence = 2;