SELECT *
FROM public.video_inference_analytics
WHERE class_name @> ARRAY['red', 'green', 'left-red']
ORDER BY video_inference_id ASC
LIMIT 10;