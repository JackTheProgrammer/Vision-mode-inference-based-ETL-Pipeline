-- SEQUENCE: public.inference_inferenced_id_seq

-- DROP SEQUENCE IF EXISTS public.inference_inferenced_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.inference_inferenced_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.inference_inferenced_id_seq
    OWNED BY public.inference.inferenced_id;

ALTER SEQUENCE public.inference_inferenced_id_seq
    OWNER TO postgres;