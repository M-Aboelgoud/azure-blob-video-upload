# Azure Blob Video Uploader (Python)

This project provides a Python script to **upload a large video file to Azure Blob Storage** using chunked uploads and retry logic for slow or unstable internet connections.

---

## 🚀 Features

- Uploads any video file in chunks to Azure Blob Storage
- Automatic container creation
- Public access support (generates public video URL)
- Retry logic for reliable uploads
- Logs detailed progress for each chunk

---

## 🧰 Prerequisites

- Python 3.8+
- Azure Storage Account (with account name and access key)

---

## 📦 Installation & Setup (Recommended via `venv`)

1. Open terminal or PowerShell and navigate to the project folder:

```bash
cd /path/to/your/project
```


2.  Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

* On **Windows**:

  ```bash
  venv\Scripts\activate
  ```

* On **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

4. Install the required Python package:

```bash
pip install azure-storage-blob
```

5. Run the upload script:

```bash
python upload_video.py
```

---

## ⚙️ Configuration

Edit these values in `upload_video.py`:

```python
STORAGE_ACCOUNT_NAME = "your_account_name"
STORAGE_ACCOUNT_KEY = "your_account_key"
CONTAINER_NAME = "your_container_name"
LOCAL_VIDEO_FILE = "./your_video.mp4"
```

---

## 📂 File Structure

```
upload_video.py     # Main upload script
nancy_ai_video.mp4  # Sample video file
README.md           # This file
```

---

## 📤 Example Output

```
✅ Uploaded 'nancy_ai_video.mp4' successfully.
🌐 Public URL: https://youraccount.blob.core.windows.net/your-container/nancy_ai_video.mp4
```

---

## 🔐 Notes

* The container is made **publicly accessible**. Anyone with the link can view the video.
* For private or time-limited access, consider using a **SAS token**.

---

## 📃 License

MIT License. Free to use, modify, and distribute.

---

## 🙋 Support

For issues or feature requests (e.g. batch uploads, SAS access, CLI support), feel free to reach out or fork the project!

```

---

Let me know if you also want:
- A `requirements.txt` to include with the project
- Dockerfile support
- Auto-renaming of videos on upload
```
