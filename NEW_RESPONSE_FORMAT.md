# 🎯 Updated API Response Format

## Overview

The PDF fraud detection endpoint now returns a combined result:
1. **AI Fraud Detection** - Boolean result (True/False)
2. **Classic Approach** - Detailed validation (only shown if AI detects fraud)

---

## Response Format

### When Fraud is Detected (AI Result = True)

```json
{
  "Final_AI_Fraud_Detection_Result": true,
  "AI_analysis": {
    "confidence": "High",
    "reason": "Patient name inconsistency detected",
    "red_flags": [
      "Name mismatch between documents"
    ],
    "missing_documents": ["Bank Statement"],
    "inconsistencies": [
      "Patient name differs in 2 documents"
    ]
  },
  "classic_approach": {
    "folder_path": "temp_folder_path",
    "status": "FRAUD DETECTED",
    "total_issues": 1,
    "files_checked": {
      "01_ClaimForm.json": {
        "status": "✅ SOURCE OF TRUTH",
        "issues": []
      },
      "02_DischargeSummary.json": {
        "status": "❌ ISSUES FOUND",
        "issues": [
          "❌ Patient Name: Expected 'Vedika Tara', Found 'Vedika'"
        ]
      },
      "03_FinalHospitalBill.json": {
        "status": "✅ MATCH",
        "issues": ["✅ All fields match (Total: ₹260800)"]
      },
      "04_PaymentReceipts.json": {
        "status": "✅ MATCH",
        "issues": ["✅ Amount matches Final Bill"]
      },
      "05_BillBreakup.json": {
        "status": "✅ MATCH",
        "issues": ["✅ Breakup matches Final Bill"]
      },
      "06_DoctorNotes.json": {
        "status": "✅ MATCH",
        "issues": ["✅ File present and valid"]
      },
      "07_LabReports.json": {
        "status": "✅ MATCH",
        "issues": ["✅ All fields match Claim Form"]
      },
      "08_PolicyCopy.json": {
        "status": "✅ MATCH",
        "issues": ["✅ All fields match Claim Form"]
      },
      "09_PatientID.json": {
        "status": "✅ MATCH",
        "issues": ["✅ All fields match Claim Form"]
      },
      "10_BankDetails.json": {
        "status": "✅ MATCH",
        "issues": ["✅ All fields match Claim Form"]
      }
    },
    "summary": [
      "Found 1 issue(s) across 1 file(s)"
    ]
  },
  "total_pages_processed": 10
}
```

### When No Fraud is Detected (AI Result = False)

```json
{
  "Final_AI_Fraud_Detection_Result": false,
  "AI_analysis": {
    "confidence": "High",
    "reason": "All documents are consistent and complete",
    "red_flags": [],
    "missing_documents": [],
    "inconsistencies": []
  },
  "total_pages_processed": 10
}
```

**Note:** When `Final_AI_Fraud_Detection_Result` is `false`, the `classic_approach` section is **not included** in the response.

---

## How to Use

### 1. Making a Request

```python
import requests

url = "http://127.0.0.1:8000/detect-fraud-from-pdf/"
files = {'pdf_file': open('claim_documents.pdf', 'rb')}
params = {'gemini_api_key': 'YOUR_API_KEY'}

response = requests.post(url, files=files, params=params)
result = response.json()
```

### 2. Processing the Response

```python
if result["Final_AI_Fraud_Detection_Result"]:
    print("🚨 FRAUD DETECTED!")
    print(f"Confidence: {result['AI_analysis']['confidence']}")
    print(f"Reason: {result['AI_analysis']['reason']}")
    
    # Check if classic validation is available
    if "classic_approach" in result:
        print("\n📋 Detailed File Validation:")
        for filename, file_data in result["classic_approach"]["files_checked"].items():
            if "❌" in file_data["status"]:
                print(f"\n{filename}: {file_data['status']}")
                for issue in file_data["issues"]:
                    print(f"  {issue}")
else:
    print("✅ CLEAN - No fraud detected")
    print(f"Reason: {result['AI_analysis']['reason']}")
```

---

## Response Fields Explained

### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `Final_AI_Fraud_Detection_Result` | boolean | `true` if fraud detected, `false` if clean |
| `AI_analysis` | object | Details from AI analysis |
| `classic_approach` | object/null | Detailed validation (only if fraud detected) |
| `total_pages_processed` | integer | Number of PDF pages processed |

### AI_analysis Object

| Field | Type | Description |
|-------|------|-------------|
| `confidence` | string | "High", "Medium", or "Low" |
| `reason` | string | Brief explanation of the decision |
| `red_flags` | array | List of suspicious findings |
| `missing_documents` | array | Required documents not found |
| `inconsistencies` | array | Data mismatches detected |

### classic_approach Object (Only when fraud detected)

| Field | Type | Description |
|-------|------|-------------|
| `folder_path` | string | Path where extracted data was analyzed |
| `status` | string | "FRAUD DETECTED" or "CLEAN" |
| `total_issues` | integer | Number of issues found |
| `files_checked` | object | File-by-file validation results |
| `summary` | array | Overall summary messages |

### files_checked Structure

Each file has:
- `status`: "✅ MATCH", "❌ ISSUES FOUND", or "✅ SOURCE OF TRUTH"
- `issues`: Array of specific findings (prefixed with ✅ or ❌)

---

## Decision Logic

```
┌─────────────────────────────────────┐
│     Upload PDF                       │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Extract text via OCR                │
│  Structure data via Gemini AI        │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  AI Fraud Detection                  │
│  Returns: true or false              │
└──────────────┬──────────────────────┘
               │
         ┌─────┴─────┐
         │           │
         ↓           ↓
   [ true ]    [ false ]
         │           │
         │           ↓
         │    Return AI result only
         │    (No classic validation)
         │
         ↓
  Run Classic Validation
  (Compare all 10 files)
         │
         ↓
  Return AI result + 
  Classic validation details
```

---

## Use Cases

### 1. Quick Screening
```python
if result["Final_AI_Fraud_Detection_Result"]:
    # Flag for manual review
    send_to_fraud_team(result)
else:
    # Auto-approve
    approve_claim()
```

### 2. Detailed Investigation
```python
if result["Final_AI_Fraud_Detection_Result"] and "classic_approach" in result:
    # Examine specific file issues
    classic = result["classic_approach"]
    for filename, data in classic["files_checked"].items():
        if "❌" in data["status"]:
            investigate_file(filename, data["issues"])
```

### 3. Confidence-Based Routing
```python
confidence = result["AI_analysis"]["confidence"]
fraud_detected = result["Final_AI_Fraud_Detection_Result"]

if fraud_detected and confidence == "High":
    reject_claim()
elif fraud_detected and confidence == "Medium":
    escalate_to_senior_reviewer()
elif fraud_detected and confidence == "Low":
    request_additional_documents()
else:
    approve_claim()
```

---

## Testing

### Test with sample PDF:
```bash
python test_pdf_fraud_api.py
```

### Expected Output (Fraud Detected):
```
✅ FRAUD DETECTION RESULT
==========================================
Final AI Result: True
Confidence: High
Reason: Name inconsistency detected

🚩 Red Flags:
   • Name mismatch in Discharge Summary

📋 Classic Validation:
   Status: FRAUD DETECTED
   Total Issues: 1
   
   02_DischargeSummary.json: ❌ ISSUES FOUND
      ❌ Patient Name: Expected 'Vedika Tara', Found 'Vedika'
```

### Expected Output (Clean):
```
✅ FRAUD DETECTION RESULT
==========================================
Final AI Result: False
Confidence: High
Reason: All documents consistent

No issues detected - Claim approved for processing
```

---

## Integration Tips

1. **Check AI result first** - It's the primary decision maker
2. **Use classic validation for details** - When you need to know exactly what's wrong
3. **Log both results** - For audit trail and model improvement
4. **Monitor confidence levels** - Adjust thresholds based on your risk tolerance

---

## Endpoint Details

**URL:** `POST /detect-fraud-from-pdf/`

**Parameters:**
- `pdf_file` (file, required): The PDF containing claim documents
- `gemini_api_key` (query, required): Your Google Gemini API key

**Returns:** JSON with fraud detection results

**Interactive Docs:** http://127.0.0.1:8000/docs

---

**Last Updated:** 2025-11-01  
**Version:** 2.0
