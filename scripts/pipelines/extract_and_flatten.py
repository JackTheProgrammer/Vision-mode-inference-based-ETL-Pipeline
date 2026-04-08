import psycopg2
import logging
from os import getenv
from dotenv import load_dotenv

# 1. Setup Professional Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Handles secure database connection."""
    try:
        load_dotenv('config/.env')
        conn = psycopg2.connect(
            host=getenv('DB_HOST'),
            port=getenv('DB_PORT', 5432),
            dbname=getenv('DB_DATABASE'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASSWORD'),
            connect_timeout=10
        )
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None

def run_sync_query(cursor, source_table, target_table, id_column):
    """
    Executes a high-performance 'Set-Based' sync.
    It identifies missing IDs using a LEFT JOIN and inserts them in one batch.
    """
    sync_sql = f"""
    INSERT INTO {target_table} (
        {id_column},
        detected_obj_class_name,
        detected_obj_class_id,
        detected_obj_confidence,
        detected_obj_x1,
        detected_obj_y1,
        detected_obj_x2,
        detected_obj_y2
    )
    SELECT 
        src.{id_column},
        -- Using ROWS FROM to ensure array parity (safety first!)
        unnested.*
    FROM {source_table} src
    LEFT JOIN {target_table} target 
        ON src.{id_column} = target.{id_column}
    CROSS JOIN LATERAL UNNEST(
        src.class_name, 
        src.class_id, 
        src.confidence, 
        src.x1, src.y1, src.x2, src.y2
    ) AS unnested(class_name, class_id, confidence, x1, y1, x2, y2)
    WHERE target.{id_column} IS NULL;
    """
    cursor.execute(sync_sql)
    return cursor.rowcount

def extract_to_flattened_tables():
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            # Sync Images
            logger.info("Starting Image table sync...")
            img_count = run_sync_query(
                cursor, 
                'public.image_inference_analytics', 
                'public.image_inferenced_analytics_flattened', 
                'image_inference_id'
            )
            logger.info(f"Successfully synced {img_count} new image detections.")

            # Sync Videos
            logger.info("Starting Video table sync...")
            vid_count = run_sync_query(
                cursor, 
                'public.video_inference_analytics', 
                'public.video_inferenced_analytics_flattened', 
                'video_inference_id'
            )
            logger.info(f"Successfully synced {vid_count} new video detections.")

            # Commit both as one transaction
            conn.commit()
            logger.info("ETL Job Completed Successfully.")

    except Exception as e:
        conn.rollback()
        logger.error(f"ETL Job Failed. Transaction rolled back. Error: {e}")
    finally:
        conn.close()
        cursor.close()

if __name__ == "__main__":
    extract_to_flattened_tables()