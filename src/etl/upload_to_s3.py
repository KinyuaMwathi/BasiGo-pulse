import boto3
import os

# Config
BUCKET_NAME = "basigopulse-raw-charlesmwathi"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")

# Initialize S3 client
s3 = boto3.client("s3")

def delete_file(s3_key):
    """
    Delete a file from S3
    """
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        print(f"🗑️ Deleted s3://{BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"❌ Error deleting {s3_key}: {str(e)}")

def upload_file(local_path, s3_key):
    """
    Upload a file to S3
    """
    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
        print(f"✅ Uploaded {local_path} to s3://{BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"❌ Error uploading {local_path}: {str(e)}")

def main():
    files = {
        "routes/routes.csv": os.path.join(DATA_DIR, "routes.csv"),
        "trips/trips.csv": os.path.join(DATA_DIR, "trips.csv"),
        "telematics/telematics.csv": os.path.join(DATA_DIR, "telematics.csv"),
        "financials/financials.csv": os.path.join(DATA_DIR, "financials.csv"),
        "maintenance/maintenance.csv": os.path.join(DATA_DIR, "maintenance.csv"),
    }

    for s3_key, local_path in files.items():
        # Delete existing file in S3 first
        delete_file(s3_key)
        # Upload fresh file
        upload_file(local_path, s3_key)

if __name__ == "__main__":
    main()