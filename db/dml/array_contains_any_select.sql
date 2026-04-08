SELECT video_inference_id, inference_id, class_name, confidence
FROM public.video_inference_analytics
WHERE class_name && ARRAY['left-red', 'red']
ORDER BY video_inference_id ASC 