# PDF Fraud Detection API - Documentation

## Overview

This new API endpoint accepts a PDF file containing insurance claim documents, performs OCR extraction, and returns a comprehensive fraud risk assessment with a score from 0-100.

## 🚀 Quick Start

### 1. Install Dependencies

First, install the required packages:

```bash
# Activate your virtual environment
.venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

**Windows:**
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR\`
3. Verify path in `ocr_processor.py` (line 11)

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

### 3. Get Google Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Save it securely (you'll need it for API calls)

### 4. Start the API Server

```bash
python main.py
```

Server will start at: **http://127.0.0.1:8000**

## 📡 API Endpoint

### POST `/detect-fraud-from-pdf/`

Upload a PDF file and get a fraud risk assessment.

**Parameters:**
- `pdf_file` (file, required): The PDF file containing claim documents
- `gemini_api_key` (query, required): Your Google Gemini API key

**Example using cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/detect-fraud-from-pdf/?gemini_api_key=YOUR_API_KEY" \
  -F "pdf_file=@claim_documents.pdf"
```

**Example using Python:**
```python
import requests

url = "http://127.0.0.1:8000/detect-fraud-from-pdf/"
files = {'pdf_file': open('claim_documents.pdf', 'rb')}
params = {'gemini_api_key': 'YOUR_GEMINI_API_KEY'}

response = requests.post(url, files=files, params=params)
result = response.json()

print(f"Fraud Score: {result['fraud_score']}/100")
print(f"Risk Level: {result['risk_level']}")
```

## 📊 Response Format

```json
{
  "success": true,
  "fraud_score": 35,
  "risk_level": "Low",
  "red_flags": [
    "Minor date format inconsistency in discharge summary"
  ],
  "missing_documents": [
    "Bank Statement"
  ],
  "inconsistencies": [
    "Patient name spelling differs in 2 documents"
  ],
  "summary": "Overall claim appears legitimate with minor documentation gaps. Recommended for manual review.",
  "extracted_data": [
    {
      "file_name": "01_ClaimForm.json",
      "claim_id": "CLM2024-12345",
      "patient_name": "John Doe",
      "hospital_name": "Apollo Hospital",
      "claim_amount": "50000",
      "document_types": ["claim form", "policy copy"]
    }
  ],
  "total_pages_processed": 10
}
```

## 🎯 Fraud Score Interpretation

| Score Range | Risk Level | Meaning |
|-------------|-----------|---------|
| 0-20 | Very Low | All documents present and consistent |
| 21-40 | Low | Minor inconsistencies or missing optional docs |
| 41-60 | Medium | Some important documents missing or moderate issues |
| 61-80 | High | Significant inconsistencies or multiple red flags |
| 81-100 | Very High | Major fraud indicators detected |

## 🔍 What the API Checks

1. **Document Completeness**
   - Claim Form
   - Discharge Summary
   - Hospital Bill
   - Payment Receipts
   - Doctor Notes
   - Lab Reports
   - Policy Copy
   - Patient ID
   - Bank Details
   - Bill Breakup

2. **Data Consistency**
   - Patient names match across documents
   - Dates are logical (admission before discharge)
   - Amounts match between bills and receipts
   - Policy numbers are consistent

3. **Red Flags**
   - Name mismatches
   - Amount discrepancies
   - Date manipulation
   - Missing critical documents
   - Suspicious patterns

## 🧪 Testing

Run the test script:

```bash
python test_pdf_fraud_api.py
```

**Before running, update:**
- `PDF_FILE_PATH`: Path to your test PDF
- `GEMINI_API_KEY`: Your actual API key

## 🌐 Interactive Documentation

Visit **http://127.0.0.1:8000/docs** for:
- Interactive API testing (Swagger UI)
- Try out the endpoint with your own PDFs
- See all available endpoints
- View request/response schemas

## 🔗 Integration with Existing Endpoints

This new endpoint works alongside the existing endpoints:

1. **POST /validate-zip-claim/**: Upload ZIP of JSON files
2. **GET /validate-local-folder/**: Validate local folder
3. **POST /detect-fraud-from-pdf/** (NEW): Upload PDF for OCR + fraud detection

## 🛠️ Troubleshooting

### "Import fitz could not be resolved"
```bash
pip install pymupdf
```

### "Tesseract is not installed"
- Install Tesseract OCR (see step 2 above)
- Update path in `ocr_processor.py` line 11

### "Invalid API key"
- Verify your Gemini API key is correct
- Check it has not expired
- Ensure you have API quota available

### "OCR functionality not available"
```bash
pip install pymupdf pillow pytesseract opencv-python google-generativeai numpy
```

## 📝 Architecture

```
PDF File Upload
    ↓
[FastAPI Endpoint] ← main.py
    ↓
[OCR Processor] ← ocr_processor.py
    ↓
├─→ [PyMuPDF] Extract pages
├─→ [Tesseract] OCR text extraction
├─→ [Google Gemini] Structure extraction
└─→ [Fraud Analyzer] Calculate risk score
    ↓
JSON Response (Fraud Score + Details)
```

## 🔐 Security Notes

- **API Key**: Never commit your Gemini API key to Git
- Store it in environment variables: `os.getenv('GEMINI_API_KEY')`
- Use `.gitignore` for config files containing keys
- Consider rate limiting for production use

## 📞 Support

For issues or questions:
1. Check the FastAPI logs in terminal
2. Visit `/docs` for API documentation
3. Test with the provided test script
4. Review OCR output files in temp folders (for debugging)

## 🎉 Example Use Case

```python
# Upload a multi-page PDF with claim documents
# API automatically:
# 1. Extracts text from each page (OCR)
# 2. Identifies document types
# 3. Extracts structured data
# 4. Checks for inconsistencies
# 5. Returns fraud score + detailed report

# Perfect for:
# - Insurance claim processing systems
# - Fraud detection pipelines
# - Document verification workflows
# - Automated claim review
```

## 📈 Next Steps

1. **Test** with your PDF files
2. **Integrate** into your workflow
3. **Monitor** fraud scores
4. **Adjust** thresholds based on your risk tolerance
5. **Combine** with existing JSON validation endpoints for comprehensive checks

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-01  
**Author:** Insurance Fraud Detection Team
