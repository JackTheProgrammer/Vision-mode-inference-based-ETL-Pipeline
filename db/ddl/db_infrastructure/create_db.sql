-- Database: yolo_inference_analytics

-- DROP DATABASE IF EXISTS yolo_inference_analytics;

CREATE DATABASE yolo_inference_analytics
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE yolo_inference_analytics
    IS 'Analytics of the my fine-tuned YOLOv11 model';