SELECT *
FROM public.video_inference_analytics
WHERE 0.81 >= ANY(confidence)
AND 'green' = ANY(class_name)
ORDER BY video_inference_id;

-- SELECT class_name
-- FROM public.video_inference_analytics
-- GROUP BY class_name;