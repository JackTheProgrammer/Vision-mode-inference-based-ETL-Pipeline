# 👁️ Vision-to-Analytics ETL Pipeline

A production-ready system designed to bridge the gap between **Computer Vision inference** and **Relational Data Analytics**. This project orchestrates the end-to-end lifecycle of raw media processing: from YOLO-based object detection to a structured Medallion-style database architecture.

-----

## 🚀 System Overview

This pipeline automates the extraction of spatial and confidence-based metadata from video/image streams and transforms it into high-performance SQL relations. It is designed for engineers and recruiters who value **data integrity**, **optimized schema design**, and **deployment-ready automation**.

### **Core Capabilities (Implemented)**

* **Automated Inference:** High-accuracy object detection using Ultralytics YOLO (`best.pt`), processing both static images and video streams.
* **Medallion Data Architecture:**
  * **Bronze:** Raw JSON/CSV dumps preserving original model output.
  * **Silver/Gold:** Structured PostgreSQL tables with dedicated sequences and GIN indexes for high-speed retrieval.
* **Production ETL Pipelines:**
  * `extract_and_transform`: Cleans and structures raw inference metadata.
  * `extract_and_flatten`: Decouples nested inference objects into analytical rows.
* **Infrastructure as Code (SQL):** Comprehensive DDL/DML suite including ranked confidence queries, unnesting logic, and array-based filtering.
* **Containerized Portability:** Fully Dockerized environment ensuring parity between local development and production.
* **CI/CD Orchestration:** Scheduled execution via GitHub Actions with secure secret management.

-----

## 🏗️ Technical Architecture

### **1. Database & Analytics Layer**

The database is not just a storage bin; it is a dedicated analytical engine.

* **Performance:** Implemented **GIN Indexes** on class names for lightning-fast multi-value searches.
* **Complex SQL Logic:** Includes unnesting demo queries, array-element selection, and ranked confidence analytics to extract top-5 contenders from detection frames.
* **Integrity:** Managed via custom SQL sequences for primary key governance across Video and Image inference tables.

### **2. The Pipeline Logic**

The scripts follow a strict separation of concerns:

* `inference/`: Pure Computer Vision logic.
* `pipelines/`: Multi-stage ETL (Extract, Transform, Load) that bridges the model to the NeonDB production/dev branches.
* `app/`: Streamlit dashboard for real-time visualization of database-resident analytics.

-----

## 📂 Project Structure

```text
Directory structure:
└── jacktheprogrammer-vision-mode-inference-based-etl-pipeline/
    ├── README.md
    ├── Dockerfile
    ├── LICENSE
    ├── requirements.txt
    ├── .dockerignore
    ├── config/
    │   └── dev.env
    ├── CSVs/
    │   └── images/
    │       ├── 20260405_002004_photo_inference_analytics.csv
    │       ├── 20260405_030950_photo_inference_analytics.csv
    │       ├── 20260408_213102_image_inference_analytics.csv
    │       └── 20260409_015202_image_inference_analytics.csv
    ├── db/
    │   ├── ddl/
    │   │   ├── db_infrastructure/
    │   │   │   ├── analytics_db_relations.sql
    │   │   │   ├── create_db.sql
    │   │   │   └── creating_gin_index_on_classes_names.sql
    │   │   └── sequences/
    │   │       ├── image_inference_analytics_pk_sequence.sql
    │   │       ├── inference_pk_sequence.sql
    │   │       └── video_inference_analytics_pk.sql
    │   └── dml/
    │       ├── array_contains_any_select.sql
    │       ├── each_class_avg_confidence_video_inference.sql
    │       ├── last element of arr based query.sql
    │       ├── ranked_confidence.sql
    │       ├── select top 5 contenders other maximum.sql
    │       ├── select_arr_specific_element.sql
    │       ├── select_containg_all_from_arr.sql
    │       ├── selecting Maximum Element in Array.sql
    │       ├── selecting minimum element in arr.sql
    │       ├── top 5 classes with max_conf in video_inference.sql
    │       └── unnesting demo select query on videos.sql
    ├── JSONs/
    │   └── photos/
    │       ├── 20260401_194925_photo_inference_dumps.json
    │       ├── 20260401_200131_photo_inference_dumps.json
    │       ├── 20260405_002003_photo_inference_dumps.json
    │       ├── 20260405_030950_photo_inference_dumps.json
    │       ├── 20260408_213102_photos_dump.json
    │       └── 20260409_015202_photos_dump.json
    ├── scripts/
    │   ├── __init__.py
    │   ├── app/
    │   │   ├── __init__.py
    │   │   ├── app.py
    │   │   └── dev_app.py
    │   ├── inference/
    │   │   ├── __init__.py
    │   │   ├── image_inference.py
    │   │   └── video_inference.py
    │   └── pipelines/
    │       ├── __init__.py
    │       ├── extract_and_flatten.py
    │       ├── extract_and_transform.py
    │       ├── load_analytics.py
    │       └── load_dev_branch_analytics.py
    └── .github/
        └── workflows/
            └── actions.yml
```

-----

## 🛠️ Tech Stack & Tooling

* **Language:** Python (optimized for 3.11/3.13)
* **Vision Engine:** Ultralytics YOLOv10/v11
* **Database:** PostgreSQL (NeonDB)
* **Analytics:** Pandas, Plotly, Seaborn
* **Deployment:** Docker, GitHub Actions

-----

## 🛡️ Engineering Excellence

* **Security:** Zero-leak policy for credentials using `.env` masking and GitHub Secret injection.
* **Scalability:** The pipeline is designed to be branch-aware, allowing seamless loading into `dev` or `production` database environments.
* **Optimized SQL:** Custom DML scripts allow for deep-dive analytics directly in the database layer, reducing overhead on the application layer.

**Constructed with resolute focus on system stability and data accuracy.** 🦋🛡️⚖️
