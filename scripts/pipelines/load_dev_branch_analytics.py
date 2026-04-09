import psycopg2
from dotenv import load_dotenv
from os import getenv
from typing import Any
from pandas import DataFrame

def get_db_connection():
    """Handles secure database connection."""
    try:
        load_dotenv('config/dev.env')
        conn = psycopg2.connect(getenv('DEV_BRANCH_NEONDB_URL'), connect_timeout=10)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        return None

def get_flattened_analytics(
    media_type: str,
    analytics = 'inferenced_analytics_flattened'
) -> list[tuple[Any, ...]] | None:
    conn = get_db_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            query = f"""
            SELECT detected_obj_class_name,
            max(detected_obj_confidence)
            AS max_confidence
            FROM {media_type}_{analytics}
            GROUP BY detected_obj_class_name, detected_obj_confidence
            ORDER BY detected_obj_confidence DESC
            LIMIT 5
            """
            cursor.execute(query, (media_type,))
            results = cursor.fetchall()
            return results
    except psycopg2.Error as e:
        print(f"Query execution failed: {e}")
        return None
    finally:
        conn.close()
        
def get_image_video_max_confidence() -> tuple[DataFrame | None, DataFrame | None]:
    """
    Fetches top 5 detected object classes with max confidence for both images and videos.
    Returns:
        Tuple of DataFrames containing top 5 classes and their confidences for images and videos.
        
        `top5_image_classes` and `top5_video_classes` are DataFrames with columns 
        'top5_classes' and 'top5_confidences'.
            - 'top5_classes': List of top 5 detected object class names.
            - 'top5_confidences': List of corresponding confidence scores for the 
            top 5 classes.
        
        In case of failure to retrieve data, returns `(None, None)`.
    """
    image_results = get_flattened_analytics('image')
    video_results = get_flattened_analytics('video')
    
    if image_results is None or video_results is None:
        print("Failed to retrieve analytics data.")
        return None, None

    top5_image_classes = {
        'top5_classes': [],
        'top5_confidences': [],
    }
    top5_video_classes = {
        'top5_classes': [],
        'top5_confidences': [],
    }
    
    for obj_class, confidence in image_results:
        top5_image_classes['top5_classes'].append(obj_class)
        top5_image_classes['top5_confidences'].append(confidence)

    for obj_class, confidence in video_results:
        top5_video_classes['top5_classes'].append(obj_class)
        top5_video_classes['top5_confidences'].append(confidence)

    return DataFrame(top5_image_classes), DataFrame(top5_video_classes)