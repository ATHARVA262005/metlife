# FastAPI Claim Validation - Quick Start Guide

## 🚀 Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
python main.py
```

The server will start at: **http://localhost:8000**

### 3. Access the Documentation
- **Swagger UI:** http://localhost:8000/docs (Interactive API testing)
- **ReDoc:** http://localhost:8000/redoc (Clean documentation)

---

## 📤 How to Use

### Method 1: Using Swagger UI (Easiest)

1. Open http://localhost:8000/docs in your browser
2. Click on **POST /validate** endpoint
3. Click **"Try it out"**
4. Click **"Add file"** multiple times to upload JSON files
5. Upload at least `01_ClaimForm.json` (required)
6. Click **"Execute"**
7. See the validation results below!

### Method 2: Using Python Code

```python
import requests

# Prepare files
files = [
    ('files', open('claim_folder_001/01_ClaimForm.json', 'rb')),
    ('files', open('claim_folder_001/02_DischargeSummary.json', 'rb')),
    ('files', open('claim_folder_001/03_FinalHospitalBill.json', 'rb')),
    ('files', open('claim_folder_001/04_PaymentReceipts.json', 'rb')),
    ('files', open('claim_folder_001/05_BillBreakup.json', 'rb')),
    ('files', open('claim_folder_001/06_DoctorNotes.json', 'rb')),
    ('files', open('claim_folder_001/07_LabReports.json', 'rb')),
    ('files', open('claim_folder_001/08_PolicyCopy.json', 'rb')),
    ('files', open('claim_folder_001/09_PatientID.json', 'rb')),
    ('files', open('claim_folder_001/10_BankDetails.json', 'rb')),
]

# Upload and validate
response = requests.post('http://localhost:8000/validate', files=files)

# Print results
result = response.json()
print(f"Claim ID: {result['claim_id']}")
print(f"Status: {result['validation_report']['status']}")
print(f"Total Issues: {result['validation_report']['total_issues']}")
```

### Method 3: Using cURL

```bash
curl -X POST "http://localhost:8000/validate" \
  -F "files=@claim_folder_001/01_ClaimForm.json" \
  -F "files=@claim_folder_001/02_DischargeSummary.json" \
  -F "files=@claim_folder_001/03_FinalHospitalBill.json" \
  -F "files=@claim_folder_001/04_PaymentReceipts.json" \
  -F "files=@claim_folder_001/05_BillBreakup.json" \
  -F "files=@claim_folder_001/06_DoctorNotes.json" \
  -F "files=@claim_folder_001/07_LabReports.json" \
  -F "files=@claim_folder_001/08_PolicyCopy.json" \
  -F "files=@claim_folder_001/09_PatientID.json" \
  -F "files=@claim_folder_001/10_BankDetails.json"
```

### Method 4: Using Test Script

```bash
python test_api.py
```

---

## 📝 Response Format

### Clean Claim (No Fraud)
```json
{
  "claim_id": "claim_abc123_20251101_140000",
  "uploaded_files": ["01_ClaimForm.json", "02_DischargeSummary.json", ...],
  "files_uploaded_count": 10,
  "validation_report": {
    "status": "CLEAN",
    "total_issues": 0,
    "files_checked": {
      "01_ClaimForm.json": {
        "status": "✅ SOURCE OF TRUTH"
      },
      "02_DischargeSummary.json": {
        "status": "✅ MATCH",
        "issues": ["✅ All fields match Claim Form"]
      }
      // ... all other files
    },
    "summary": ["All files are consistent with Claim Form"]
  }
}
```

### Fraudulent Claim (Issues Found)
```json
{
  "claim_id": "claim_xyz456_20251101_140500",
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

## 🎯 Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/validate` | POST | Upload & validate files (main endpoint) |
| `/validate/{claim_id}` | GET | Validate existing claim |
| `/claims/list` | GET | List all uploaded claims |
| `/claims/{claim_id}` | DELETE | Delete a claim folder |
| `/files/required` | GET | Get list of required files |
| `/health` | GET | Health check |

---

## 📁 File Storage

Files are stored in: `uploads/claim_{id}_{timestamp}/`

Example:
```
uploads/
├── claim_a1b2c3d4_20251101_133000/
│   ├── 01_ClaimForm.json
│   ├── 02_DischargeSummary.json
│   └── ... (all 10 files)
```

---

## ✅ What Gets Validated

1. **Patient Identity**
   - Name consistency across documents
   - Date of Birth verification
   - ID document validation

2. **Financial Data**
   - Bill amounts vs receipts
   - Bill breakup calculations
   - Payment discrepancies

3. **Dates**
   - Admission/discharge consistency
   - Date manipulation detection

4. **Documents**
   - Missing files
   - Corrupt/invalid JSON

---

## 🧪 Testing Example

```python
# test_simple.py
import requests

# Upload files from claim_folder_001
files = []
folder = "claim_folder_001"
for i in range(1, 11):
    filename = f"{i:02d}_*.json"  # Match pattern
    # Add logic to find and open files
    
response = requests.post('http://localhost:8000/validate', files=files)
print(response.json())
```

---

## ⚠️ Important Notes

1. **ClaimForm Required:** `01_ClaimForm.json` must always be included
2. **JSON Format:** All files must be valid JSON
3. **Multiple Files:** Upload all 10 files for complete validation
4. **Unique IDs:** Each upload gets a unique claim ID

---

## 🔧 Troubleshooting

### Server won't start
```bash
# Make sure port 8000 is free
# Or change port in main.py:
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Import errors
```bash
pip install -r requirements.txt
```

### File upload fails
- Check file is valid JSON
- Ensure file extension is .json
- Verify file size (if you set limits)

---

## 📖 Full Documentation

See **API_DOCUMENTATION.md** for complete API reference.

---

**Happy Validating! 🎉**
