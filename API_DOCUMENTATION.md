# Insurance Claim Validation API - Documentation

## Overview
FastAPI application that accepts JSON file uploads for insurance claim validation. Files are stored locally and validated against the ClaimForm (Source of Truth).

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python main.py
```

The API will be available at: `http://localhost:8000`

### 3. Access Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📡 API Endpoints

### 1. **Root Endpoint**
```http
GET /
```

**Response:**
```json
{
  "message": "Insurance Claim Validation API",
  "version": "1.0.0",
  "endpoints": {
    "upload_and_validate": "/validate",
    "upload_single": "/upload/single",
    "upload_multiple": "/upload/multiple",
    "validate_existing": "/validate/{folder_name}",
    "health": "/health"
  }
}
```

---

### 2. **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-01T13:30:00.000000"
}
```

---

### 3. **Upload and Validate** ⭐ (Main Endpoint)
```http
POST /validate
```

**Description:** Upload multiple JSON files, store them locally, and perform validation.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Multiple files (at least `01_ClaimForm.json` required)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/validate" \
  -F "files=@01_ClaimForm.json" \
  -F "files=@02_DischargeSummary.json" \
  -F "files=@03_FinalHospitalBill.json" \
  -F "files=@04_PaymentReceipts.json"
```

**Example using Python:**
```python
import requests

files = [
    ('files', ('01_ClaimForm.json', open('claim_folder_001/01_ClaimForm.json', 'rb'))),
    ('files', ('02_DischargeSummary.json', open('claim_folder_001/02_DischargeSummary.json', 'rb'))),
    # ... add more files
]

response = requests.post('http://localhost:8000/validate', files=files)
print(response.json())
```

**Response (Success - Clean):**
```json
{
  "claim_id": "claim_a1b2c3d4_20251101_133000",
  "folder_path": "uploads/claim_a1b2c3d4_20251101_133000",
  "uploaded_files": [
    "01_ClaimForm.json",
    "02_DischargeSummary.json",
    "03_FinalHospitalBill.json",
    "04_PaymentReceipts.json",
    "05_BillBreakup.json",
    "06_DoctorNotes.json",
    "07_LabReports.json",
    "08_PolicyCopy.json",
    "09_PatientID.json",
    "10_BankDetails.json"
  ],
  "files_uploaded_count": 10,
  "timestamp": "2025-11-01T13:30:00.000000",
  "validation_report": {
    "folder_path": "uploads/claim_a1b2c3d4_20251101_133000",
    "status": "CLEAN",
    "total_issues": 0,
    "files_checked": {
      "01_ClaimForm.json": {
        "status": "✅ SOURCE OF TRUTH",
        "issues": []
      },
      "02_DischargeSummary.json": {
        "status": "✅ MATCH",
        "issues": ["✅ All fields match Claim Form"]
      },
      // ... other files
    },
    "summary": ["All files are consistent with Claim Form"]
  }
}
```

**Response (Fraud Detected):**
```json
{
  "claim_id": "claim_xyz123_20251101_133500",
  "folder_path": "uploads/claim_xyz123_20251101_133500",
  "uploaded_files": [...],
  "files_uploaded_count": 10,
  "timestamp": "2025-11-01T13:35:00.000000",
  "validation_report": {
    "status": "FRAUD DETECTED",
    "total_issues": 2,
    "files_checked": {
      "04_PaymentReceipts.json": {
        "status": "❌ ISSUES FOUND",
        "issues": [
          "❌ Amount Paid: Expected ₹500000, Found ₹450000 (Diff: ₹50000)"
        ]
      },
      "09_PatientID.json": {
        "status": "❌ ISSUES FOUND",
        "issues": [
          "❌ Name on ID: Expected 'John Doe', Found 'Jane Smith'"
        ]
      }
    },
    "summary": ["Found 2 issue(s) across 2 file(s)"]
  }
}
```

---

### 4. **Upload Single File**
```http
POST /upload/single?claim_id={claim_id}
```

**Description:** Upload a single file to a specific claim folder.

**Parameters:**
- `claim_id` (query): Claim folder ID

**Request Body:**
- `file`: Single JSON file

**Example:**
```bash
curl -X POST "http://localhost:8000/upload/single?claim_id=my_claim_001" \
  -F "file=@01_ClaimForm.json"
```

**Response:**
```json
{
  "message": "File uploaded successfully",
  "claim_id": "my_claim_001",
  "filename": "01_ClaimForm.json",
  "file_path": "uploads/my_claim_001/01_ClaimForm.json",
  "timestamp": "2025-11-01T13:40:00.000000"
}
```

---

### 5. **Upload Multiple Files**
```http
POST /upload/multiple?claim_id={claim_id}
```

**Description:** Upload multiple files without validation.

**Parameters:**
- `claim_id` (query): Claim folder ID

**Request Body:**
- `files`: Multiple JSON files

**Response:**
```json
{
  "message": "Files upload completed",
  "claim_id": "my_claim_001",
  "folder_path": "uploads/my_claim_001",
  "uploaded_files": [
    "01_ClaimForm.json",
    "02_DischargeSummary.json"
  ],
  "uploaded_count": 2,
  "errors": [],
  "timestamp": "2025-11-01T13:45:00.000000"
}
```

---

### 6. **Validate Existing Claim**
```http
GET /validate/{claim_id}
```

**Description:** Validate a previously uploaded claim folder.

**Parameters:**
- `claim_id` (path): Claim folder ID

**Example:**
```bash
curl -X GET "http://localhost:8000/validate/claim_a1b2c3d4_20251101_133000"
```

**Response:**
```json
{
  "claim_id": "claim_a1b2c3d4_20251101_133000",
  "folder_path": "uploads/claim_a1b2c3d4_20251101_133000",
  "files_in_folder": [
    "01_ClaimForm.json",
    "02_DischargeSummary.json",
    // ...
  ],
  "timestamp": "2025-11-01T13:50:00.000000",
  "validation_report": {
    // Same format as /validate endpoint
  }
}
```

---

### 7. **List All Claims**
```http
GET /claims/list
```

**Description:** Get a list of all uploaded claim folders.

**Response:**
```json
{
  "claims": [
    {
      "claim_id": "claim_a1b2c3d4_20251101_133000",
      "folder_path": "uploads/claim_a1b2c3d4_20251101_133000",
      "files_count": 10,
      "files": [
        "01_ClaimForm.json",
        "02_DischargeSummary.json",
        // ...
      ]
    }
  ],
  "count": 1,
  "timestamp": "2025-11-01T13:55:00.000000"
}
```

---

### 8. **Delete Claim**
```http
DELETE /claims/{claim_id}
```

**Description:** Delete a claim folder and all its files.

**Parameters:**
- `claim_id` (path): Claim folder ID

**Response:**
```json
{
  "message": "Claim folder deleted successfully",
  "claim_id": "claim_a1b2c3d4_20251101_133000",
  "timestamp": "2025-11-01T14:00:00.000000"
}
```

---

### 9. **Get Required Files**
```http
GET /files/required
```

**Description:** Get list of required files for validation.

**Response:**
```json
{
  "required_files": [
    "01_ClaimForm.json",
    "02_DischargeSummary.json",
    "03_FinalHospitalBill.json",
    "04_PaymentReceipts.json",
    "05_BillBreakup.json",
    "06_DoctorNotes.json",
    "07_LabReports.json",
    "08_PolicyCopy.json",
    "09_PatientID.json",
    "10_BankDetails.json"
  ],
  "count": 10,
  "note": "01_ClaimForm.json is mandatory. Others are optional but recommended."
}
```

---

## 🔍 Validation Logic

The API compares all files against `01_ClaimForm.json` (Source of Truth):

### Checks Performed:

1. **Patient Identity**
   - Name consistency across all documents
   - Date of Birth verification
   - ID document validation

2. **Financial Validation**
   - Bill amount vs payment receipts
   - Bill breakup totals
   - Amount discrepancies detection

3. **Date Validation**
   - Admission date consistency
   - Discharge date verification
   - Date manipulation detection

4. **Document Completeness**
   - Missing file detection
   - Corrupt file identification

---

## 📁 File Storage

- **Location:** `uploads/` folder
- **Structure:** Each claim gets a unique folder
- **Naming:** `claim_{uuid}_{timestamp}`
- **Format:** JSON files with proper formatting

Example:
```
uploads/
├── claim_a1b2c3d4_20251101_133000/
│   ├── 01_ClaimForm.json
│   ├── 02_DischargeSummary.json
│   └── ...
└── claim_xyz123_20251101_133500/
    ├── 01_ClaimForm.json
    └── ...
```

---

## 🧪 Testing

### Run Test Suite
```bash
python test_api.py
```

### Manual Testing with Postman

1. Import the following cURL commands into Postman
2. Test each endpoint
3. Verify responses

---

## ⚠️ Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (Invalid JSON, Missing ClaimForm) |
| 404 | Not Found (Claim folder doesn't exist) |
| 500 | Internal Server Error |

---

## 🔒 Security Considerations

- **File Validation:** Only JSON files accepted
- **Size Limits:** Configure as needed
- **CORS:** Currently allows all origins (configure for production)
- **Authentication:** Add JWT/OAuth for production use

---

## 📝 Notes

1. **ClaimForm Required:** `01_ClaimForm.json` must be included in every upload
2. **Unique IDs:** Each upload generates a unique claim ID
3. **Local Storage:** Files are stored in the `uploads/` folder
4. **JSON Format:** All files must be valid JSON

---

## 🚀 Production Deployment

1. **Environment Variables:**
   ```bash
   export UPLOAD_FOLDER=/path/to/uploads
   export API_HOST=0.0.0.0
   export API_PORT=8000
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Use Nginx as Reverse Proxy**

4. **Add Authentication & Rate Limiting**

---

**API Version:** 1.0.0  
**Last Updated:** November 1, 2025
