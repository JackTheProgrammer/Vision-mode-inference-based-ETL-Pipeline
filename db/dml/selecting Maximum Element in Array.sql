SELECT * 
FROM (
    SELECT video_inference_id, confidence,
	(SELECT max(conf) FROM unnest(confidence) conf) as max_conf 
	FROM public.video_inference_analytics 
) sub_query
WHERE max_conf BETWEEN 87 AND 100;