-- SEQUENCE: public.video_inference_analytics_video_inference_id_seq

-- DROP SEQUENCE IF EXISTS public.video_inference_analytics_video_inference_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.video_inference_analytics_video_inference_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.video_inference_analytics_video_inference_id_seq
    OWNED BY public.video_inference_analytics.video_inference_id;

ALTER SEQUENCE public.video_inference_analytics_video_inference_id_seq
    OWNER TO postgres;