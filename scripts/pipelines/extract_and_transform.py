# from dotenv import load_dotenv
# from pandas import DataFrame
# import os, sys, psycopg2, json, datetime

# # Allow running as a script from any CWD (not only as a package module).
# # This makes `python scripts/pipelines/inference_etl.py` work.
# repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# if repo_root not in sys.path:
#     sys.path.insert(0, repo_root)

# from scripts.inference.image_inference import image_inference
# from scripts.inference.video_inference import video_inference

# def media_type(media_path: str) -> str:
#     # example name: 20221120_165837_jpg.rf.da94dd0a7d8cd7e083d97b2e356dba4a.jpg,
#     # has length of 4 when split by '.', and the 4th element is 'jpg' or 'jpeg' -> image
#     if len(media_path.split('.')) == 4:
#         if media_path.split('.')[3] == 'jpg' or media_path.split('.')[3] == 'jpeg':
#             return 'image'
#         else:
#             return 'not an image'
#     elif media_path.split('.')[1] == 'mp4' or media_path.split('.')[1] == 'avi':
#         return 'video'
#     else:
#         return 'unknown'

# def extract_media_inference_to_db():
#     """
#     Extract media inference results and save to database.
#     """
#     photos_dir = 'media/photos'
#     videos_dir = 'media/videos'
    
#     photos_inferenced_json_list = []
#     videos_inferenced_json_list = []
    
#     load_dotenv('config/.env')
#     host = os.getenv('DB_HOST')
#     port = os.getenv('DB_PORT')
#     database = os.getenv('DB_DATABASE')
#     user = os.getenv('DB_USER')
#     password = os.getenv('DB_PASSWORD')

#     try:
#         connection = psycopg2.connect(
#             host=host,
#             port=port,
#             database=database,
#             user=user,
#             password=password
#         )
        
#         # If we reach this line, the connection is alive
#         print("Connection to database successful")
        
#         # Optional: double check with a real ping
#         cursor = connection.cursor()
#         # cursor.execute('SELECT 1')
        
#     except Exception as e:
#         # This runs if the host is wrong, password fails, etc.
#         print(f"Connection to database failed due to error: {e}")
    
#     for photo in os.listdir(photos_dir):
#         print(f"Processing photo: {photo}")
#         photo_path = os.path.join(photos_dir, photo)
#         # I am double checking the media type because there 
#         # may be some non-image files in the photos directory,
#         # and I want to avoid errors from trying to run 
#         # inference on non-image files
#         if media_type(photo_path) != 'image':
#             print(f"Skipping non-image file: {photo_path}")
#         else:
#             image_inference_json_list = image_inference(photo_path)
#             insert_to_inference_query = """
#             INSERT INTO inference
#                 (media_path, media_type, image_inference)
#             VALUES
#                 (%s, %s, %s)
#             RETURNING inference.inferenced_id;
#             """
#             # Why the 0th element? Because image_inference 
#             # returns a list of JSON strings, but for images 
#             # we only have one JSON string in the list, so 
#             # we take the 0th element to get the JSON string, and then
#             # parse it into a JSON object before inserting into the database.
#             image_inference_json = json.loads(image_inference_json_list[0])
#             cursor.execute(
#                 insert_to_inference_query,
#                 (photo_path, 'image', json.dumps(image_inference_json))
#             )
            
#             inference_id = cursor.fetchone()[0]
            
#             # Insert each detection into image_inference_analytics
#             insert_to_analytics_query = """
#             INSERT INTO image_inference_analytics
#                 (inference_id, class_name, class_id, confidence, x1, y1, x2, y2)
#             VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s);
#             """
            
#             # The structure of the parsed JSON at 0th index is acquired via an example run 
#             # of the image_inference function on a sample image, and is as follows:
#             # [
#                 # {
#                     # "name":"green",
#                     # "class":0,
#                     # "confidence":0.81741,
#                     # "box":{
#                         # "x1":134.97356,
#                         # "y1":129.00793,
#                         # "x2":148.42818,
#                         # "y2":174.41165
#                     # }
#                 # },
#                 # {
#                     # "name":"left-red",
#                     # "class":2,
#                     # "confidence":0.77638,
#                     # "box":{
#                         # "x1":298.35782,
#                         # "y1":189.50417,
#                         # "x2":317.5578,
#                         # "y2":247.40361
#                     # }
#                 # }
#             # ]
            
#             class_names = [detection['name'] for detection in image_inference_json]
#             class_ids = [detection['class'] for detection in image_inference_json]
#             confidences = [detection['confidence'] for detection in image_inference_json]
#             x1_values = [detection['box']['x1'] for detection in image_inference_json]
#             y1_values = [detection['box']['y1'] for detection in image_inference_json]
#             x2_values = [detection['box']['x2'] for detection in image_inference_json]
#             y2_values = [detection['box']['y2'] for detection in image_inference_json]
#             cursor.execute(
#                 insert_to_analytics_query,
#                 (
#                     inference_id,
#                     class_names,
#                     class_ids,
#                     confidences,
#                     x1_values,
#                     y1_values,
#                     x2_values,
#                     y2_values
#                 )
#             )
#             connection.commit()
            
#             image_inference_collection = {
#                 photo_path: {
#                     "class_name": class_names,
#                     "class_id": class_ids,
#                     "confidence": confidences,
#                     "x1": x1_values,
#                     "y1": y1_values,
#                     "x2": x2_values,
#                     "y2": y2_values
#                 }
#             }
#             photos_inferenced_json_list.append(image_inference_collection)

#     for video in os.listdir(videos_dir):
#         print(f"Processing video: {video}")
#         video_path = os.path.join(videos_dir, video)
#         # Same logic as above - double checking media type 
#         # to avoid errors from non-video files in the 
#         # videos directory
#         if media_type(video_path) != 'video':
#             print(f"Skipping non-video file: {video_path}")
#         else:
#             video_inference_json_list = video_inference(video_path)
            
#             # I got the structure of the video inference 
#             # JSON list from an example run of the video_inference 
#             # function on a sample video. 
            
#             # The reason for the json list be that long is that video inference results 
#             # are stored as a list of frames, and each frame has its own inference result.
#             # So for a video with many frames, the resulting JSON list can be quite long.
                
#             # Filter out empty frame outputs (e.g., '[]') from the returned model JSON list.
#             non_empty_video_inference_json_list = [item for item in video_inference_json_list if item and item != '[]']
#             parsed_video_inference_json_list = []
#             for inference_json in non_empty_video_inference_json_list:
#                 try:
#                     parsed_frame = json.loads(inference_json)
#                 except json.JSONDecodeError as exc:
#                     print(f"Warning: skipping invalid JSON frame for {video_path}: {exc}")
#                     continue
#                 if isinstance(parsed_frame, list) and parsed_frame:
#                     parsed_video_inference_json_list.append(parsed_frame)

#             # Build flatten arrays for one matching dimension across all frames, required by Pg array columns.
#             class_names = [detection['name'] for frame_inference in parsed_video_inference_json_list for detection in frame_inference]
#             class_ids = [detection['class'] for frame_inference in parsed_video_inference_json_list for detection in frame_inference]
#             confidences = [detection['confidence'] for frame_inference in parsed_video_inference_json_list for detection in frame_inference]
#             x1_values = [detection['box']['x1'] for frame_inference in parsed_video_inference_json_list for detection in frame_inference]
#             y1_values = [detection['box']['y1'] for frame_inference in parsed_video_inference_json_list for detection in frame_inference]
#             x2_values = [detection['box']['x2'] for frame_inference in parsed_video_inference_json_list for detection in frame_inference]
#             y2_values = [detection['box']['y2'] for frame_inference in parsed_video_inference_json_list for detection in frame_inference]

#             # inserting into the `inference` table first to get the 
#             # `inference_id` for the video, which is a foreign key in the 
#             # `video_inference_analytics` table
            
#             insert_to_inference_query = """
#             INSERT INTO inference
#                 (media_path, media_type, video_inference)
#             VALUES
#                 (%s, %s, %s)
#             RETURNING inference.inferenced_id;
#             """
#             cursor.execute(
#                 insert_to_inference_query,
#                 (video_path, 'video', json.dumps(video_inference_json_list))
#             )
#             inference_id = cursor.fetchone()[0]

#             insert_to_video_analytics_query = """
#             INSERT INTO video_inference_analytics
#                 (inference_id, class_name, class_id, confidence, x1, y1, x2, y2)
#             VALUES
#                 (%s, %s, %s, %s, %s, %s, %s, %s);
#             """
#             cursor.execute(
#                 insert_to_video_analytics_query,
#                 (
#                     inference_id,
#                     class_names,
#                     class_ids,
#                     confidences,
#                     x1_values,
#                     y1_values,
#                     x2_values,
#                     y2_values
#                 )
#             )
#             connection.commit()
            
#             video_inference_collection = {
#                 video_path: {
#                     "class_name": class_names,
#                     "class_id": class_ids,
#                     "confidence": confidences,
#                     "x1": x1_values,
#                     "y1": y1_values,
#                     "x2": x2_values,
#                     "y2": y2_values,
#                 }
#             }
#             videos_inferenced_json_list.append(video_inference_collection)

#     cursor.close()
#     connection.close()

#     return photos_inferenced_json_list, videos_inferenced_json_list

# def transform_results_to_json():
#     photos_inferenced_json_list, videos_inferenced_json_list = extract_media_inference_to_db()
#     print("Photos inferenced JSON list length:", len(photos_inferenced_json_list))
#     print("Videos inferenced JSON list length:", len(videos_inferenced_json_list))

#     # Generate a filesystem-safe timestamp for filenames (no ':' characters)
#     safe_ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#     photo_file = f'JSONs/photos/{safe_ts}_photo_inference_dumps.json'
#     video_file = f'JSONs/videos/{safe_ts}_video_inference_dumps.json'

#     # Write the results to separate files
#     with open(photo_file, 'w') as f:
#         json.dump(photos_inferenced_json_list, f, indent=4)

#     with open(video_file, 'w') as f:
#         json.dump(videos_inferenced_json_list, f, indent=4)

#     print(f"Results saved to {photo_file} and {video_file}")

# def transform_results_to_csv():
#     # This function can be implemented in the future if we want to save results in CSV format instead of JSON.
#     try:
#         load_dotenv('config/.env')
#         host = os.getenv('DB_HOST')
#         port = os.getenv('DB_PORT')
#         dbname = os.getenv('DB_DATABASE')
#         user = os.getenv('DB_USER')
#         password = os.getenv('DB_PASSWORD')

#         conn = psycopg2.connect(
#             host=host,
#             port=port,
#             dbname=dbname,
#             user=user,
#             password=password
#         )
        
#         if conn:
#             print("Successfully connected to PostgreSQL")
        
#         cursor = conn.cursor()
#         print("The PostgreSQL cursor status: ", cursor.statusmessage)
#     except psycopg2.Error as e:
#         print(f"Error connecting to PostgreSQL: {e.pgerror} with error code: {e.pgcode}")
    
#     image_analytics_table = 'public.image_inference_analytics'
#     video_analytics_table = 'public.video_inference_analytics'
    
#     image_analytics_select_query = f"""
#     SELECT image_inference_id, class_name, confidence, 
#     x1, y1, x2, y2 
#     FROM {image_analytics_table};
#     """
    
#     video_analytics_select_query = f"""
#     SELECT video_inference_id, class_name, confidence, 
#     x1, y1, x2, y2 
#     FROM {video_analytics_table};
#     """
    
#     image_analytics_results = {
#         'image_inference_id': [],
#         'class_name': [],
#         'confidence': [],
#         'x1': [],
#         'y1': [],
#         'x2': [],
#         'y2': []
#     }
#     video_analytics_results = {
#         'video_inference_id': [],
#         'class_name': [],
#         'confidence': [],
#         'x1': [],
#         'y1': [],
#         'x2': [],
#         'y2': []
#     }
    
#     try:
#         cursor.execute(image_analytics_select_query)
#         image_rows = cursor.fetchall()

#         for image_analytics in image_rows:
#             print("Image inference id: ", image_analytics[0])
#             image_analytics_results['image_inference_id'].append(image_analytics[0])
            
#             print("Class name: ", image_analytics[1])
#             image_analytics_results['class_name'].append(image_analytics[1])
            
#             print("Confidence: ", image_analytics[2])
#             image_analytics_results['confidence'].append(image_analytics[2])

#             print("X1: ", image_analytics[3])
#             image_analytics_results['x1'].append(image_analytics[3])
            
#             print("Y1: ", image_analytics[4])
#             image_analytics_results['y1'].append(image_analytics[4])
            
#             print("X2: ", image_analytics[5])
#             image_analytics_results['x2'].append(image_analytics[5])

#             print("Y2: ", image_analytics[6])
#             image_analytics_results['y2'].append(image_analytics[6])
            
#             print("Length of image_analytics: ", len(image_analytics))
        
#         cursor.execute(video_analytics_select_query)
#         video_rows = cursor.fetchall()

#         for video_analytics in video_rows:
#             print("Video inference id: ", (video_analytics[0]))
#             video_analytics_results['video_inference_id'].append(video_analytics[0])
            
#             print("Class name: ", video_analytics[1])
#             video_analytics_results['class_name'].append(video_analytics[1])
            
#             print("Confidence: ", video_analytics[2])
#             video_analytics_results['confidence'].append(video_analytics[2])
            
#             print("X1: ", video_analytics[3])
#             video_analytics_results['x1'].append(video_analytics[3])
            
#             print("Y1: ", video_analytics[4])
#             video_analytics_results['y1'].append(video_analytics[4])
            
#             print("X2: ", video_analytics[5])
#             video_analytics_results['x2'].append(video_analytics[5])
            
#             print("Y2: ", video_analytics[6])
#             video_analytics_results['y2'].append(video_analytics[6])
            
#             print("Length of video_analytics: ", len(video_analytics))

#     except psycopg2.Error as e:
#         print(f"Error executing query: {e.pgerror} with error code: {e.pgcode}")

#     finally:
#         if cursor and conn:
#             cursor.close()
#             conn.close()
    
#     image_analytics_df = DataFrame(image_analytics_results)
#     video_analytics_df = DataFrame(video_analytics_results)
    
#     # Generate a filesystem-safe timestamp for filenames (no ':' characters)
#     safe_ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#     photo_file = f'CSVs/photos/{safe_ts}_photo_inference_analytics.csv'
#     video_file = f'CSVs/videos/{safe_ts}_video_inference_analytics.csv'

#     image_analytics_df.to_csv(photo_file, index=False)
#     video_analytics_df.to_csv(video_file, index=False)

# transform_results_to_json()
# transform_results_to_csv()

import os
import sys
import json
import logging
import datetime
import psycopg2
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# --- 1. SETUP & PATHING ---
# Using Pathlib for robust cross-platform path handling
BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.inference.image_inference import image_inference
from scripts.inference.video_inference import video_inference

# Initialize Logging (Better than print statements)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
load_dotenv(BASE_DIR / 'config/.env')

# --- 2. UTILITY FUNCTIONS ---

def get_db_connection():
    """Centralized connection logic (Cloud-ready for NeonDB)."""
    try:
        # This is done for on-prem setups where .env might be used, 
        # but in production with NeonDB, the NEON_DATABASE_URL env var 
        # should be retrieved from the GitHub secrets.
        env_file_path = Path('config/.env')
        if env_file_path.exists():
            load_dotenv(env_file_path)
            conn = psycopg2.connect(os.getenv('ON_PREMISE_DB'))
        
        # Use the DSN string logic we discussed for NeonDB/Production
        # on GitHub Actions, where the .env file won't be present, 
        # and the connection string is provided via env vars.
        elif env_file_path.exists() == False:
            conn = psycopg2.connect(os.getenv('NEON_DATABASE_URL'))
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        sys.exit(1)

def get_media_type(file_path: Path) -> str:
    """Robust extension checking using Pathlib."""
    ext = file_path.suffix.lower()
    if ext in ['.jpg', '.jpeg']: return 'image'
    if ext in ['.mp4', '.avi']: return 'video'
    return 'unknown'

def flatten_detections(detections):
    """Refactor: One pass to extract all lists from detections."""
    data = {
        'names': [], 'ids': [], 'confs': [],
        'x1': [], 'y1': [], 'x2': [], 'y2': []
    }
    for d in detections:
        data['names'].append(d['name'])
        data['ids'].append(d['class'])
        data['confs'].append(d['confidence'])
        data['x1'].append(d['box']['x1'])
        data['y1'].append(d['box']['y1'])
        data['x2'].append(d['box']['x2'])
        data['y2'].append(d['box']['y2'])
    return data

# --- 3. THE ETL CORE ---

def process_inference():
    """The 'Resolute' ETL: Extracts, Infers, and Loads."""
    photos_dir = Path('media/photos')
    videos_dir = Path('media/videos')
    results = {'photos': [], 'videos': []}

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            # --- Process Photos ---
            for photo_path in photos_dir.glob('*'):
                if get_media_type(photo_path) != 'image': continue
                
                logging.info(f"Inferencing Photo: {photo_path.name}")
                raw_json = image_inference(str(photo_path))
                parsed_data = json.loads(raw_json[0])
                flat = flatten_detections(parsed_data)

                # Insert to Main Table
                cursor.execute(
                    "INSERT INTO inference (media_path, media_type, image_inference) VALUES (%s, %s, %s) RETURNING inferenced_id",
                    (str(photo_path), 'image', json.dumps(parsed_data))
                )
                inf_id = cursor.fetchone()[0]

                # Insert to Analytics Table
                cursor.execute(
                    "INSERT INTO image_inference_analytics (inference_id, class_name, class_id, confidence, x1, y1, x2, y2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (inf_id, flat['names'], flat['ids'], flat['confs'], flat['x1'], flat['y1'], flat['x2'], flat['y2'])
                )
                results['photos'].append({str(photo_path): flat})

            # --- Process Videos ---
            for video_path in videos_dir.glob('*'):
                if get_media_type(video_path) != 'video': continue
                
                logging.info(f"Inferencing Video: {video_path.name}")
                raw_list = video_inference(str(video_path))
                
                # Filter & Flatten (Using the logic we discussed earlier)
                frames = [json.loads(f) for f in raw_list if f and f != '[]']
                all_detections = [det for frame in frames for det in frame]
                flat = flatten_detections(all_detections)

                cursor.execute(
                    "INSERT INTO inference (media_path, media_type, video_inference) VALUES (%s, %s, %s) RETURNING inferenced_id",
                    (str(video_path), 'video', json.dumps(raw_list))
                )
                inf_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO video_inference_analytics (inference_id, class_name, class_id, confidence, x1, y1, x2, y2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (inf_id, flat['names'], flat['ids'], flat['confs'], flat['x1'], flat['y1'], flat['x2'], flat['y2'])
                )
                results['videos'].append({str(video_path): flat})
                
            conn.commit()
    return results

# --- 4. EXPORT LOGIC ---

def export_results(data):
    """Saves findings to JSON and CSV."""
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # JSON Export
    for m_type in ['photos', 'videos']:
        path = Path(f'JSONs/{m_type}/{ts}_{m_type}_dump.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data[m_type], f, indent=4)

    # CSV Export (The Data Engineer Way)
    with get_db_connection() as conn:
        for table in ['image_inference_analytics', 'video_inference_analytics']:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            csv_path = Path(f"CSVs/{table.split('_')[0]}s/{ts}_{table}.csv")
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(csv_path, index=False)
            logging.info(f"Exported {table} to CSV.")

if __name__ == "__main__":
    inference_data = process_inference()
    export_results(inference_data)