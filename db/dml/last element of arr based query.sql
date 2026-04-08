SELECT * 
FROM public.video_inference_analytics 
WHERE confidence[array_upper(confidence, 1)] <= 0.95;