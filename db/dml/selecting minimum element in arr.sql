SELECT * 
FROM (
    SELECT video_inference_id, confidence, (SELECT min(conf) FROM unnest(confidence) conf) as min_conf
    FROM public.video_inference_results
) sub_query
WHERE min_conf < 10;