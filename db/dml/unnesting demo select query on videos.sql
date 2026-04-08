SELECT flattened_video_inference.class_name, flattened_video_inference.confidence 
FROM (
	SELECT
		video_inference_id,
	    inference_id, 
	    unnest(class_name) as class_name, -- This "unrolls" the array into rows
		unnest(class_id) as class_id,
	    unnest(confidence) as confidence,
		unnest(x1) as x1,
		unnest(y1) as y1,
		unnest(x2) as x2,
		unnest(y2) as y2
	FROM public.video_inference_analytics
	WHERE video_inference_id = 4
) flattened_video_inference
ORDER BY flattened_video_inference.confidence DESC