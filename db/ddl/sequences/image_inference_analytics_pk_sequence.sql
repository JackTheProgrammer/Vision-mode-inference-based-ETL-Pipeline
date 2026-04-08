-- SEQUENCE: public.image_inference_analytics_image_inference_id_seq

-- DROP SEQUENCE IF EXISTS public.image_inference_analytics_image_inference_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.image_inference_analytics_image_inference_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.image_inference_analytics_image_inference_id_seq
    OWNED BY public.image_inference_analytics.image_inference_id;

ALTER SEQUENCE public.image_inference_analytics_image_inference_id_seq
    OWNER TO postgres;