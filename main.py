

import os
import json
import zipfile
import tempfile
import shutil
from typing import Any, Dict, Optional
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import JSONResponse
import uvicorn  # Import uvicorn

# Import OCR processor for PDF fraud detection
try:
    from ocr_processor import process_pdf_and_detect_fraud
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: OCR processor not available. Install dependencies: pymupdf pillow pytesseract opencv-python google-generativeai")

# --- 1. Initialize FastAPI App ---
app = FastAPI(
    title="Claim Validation API",
    description="Analyzes a folder of 10 JSON claim files for fraud and inconsistencies. "
                "Use the /docs endpoint to test.",
    version="1.0.0"
)

# --- 2. Paste Your Existing Comparison Logic (No Changes Needed) ---

def load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Safely loads a JSON file, returning None if it's missing or invalid."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"_error": "Invalid JSON format"}

def compare_files_to_claim_form(folder_path: str) -> Dict[str, Any]:
    """
    This is the core logic.
    It compares all files *inside* one folder to the 01_ClaimForm.json.
    Returns a detailed report with file-by-file comparison results.
    """
    report: Dict[str, Any] = {
        "folder_path": folder_path,
        "status": "CLEAN",
        "total_issues": 0,
        "files_checked": {},
        "summary": []
    }
    
    # --- 1. Load Source of Truth ---
    claim_form_path = os.path.join(folder_path, "01_ClaimForm.json")
    claim_form_data = load_json_file(claim_form_path)

    final_bill_path = os.path.join(folder_path, "03_FinalHospitalBill.json")
    final_bill_data = load_json_file(final_bill_path)

    # --- 2. Check for Missing Master Files ---
    if claim_form_data is None or "_error" in claim_form_data:
        report["status"] = "CRITICAL ERROR"
        report["summary"].append("CRITICAL: 01_ClaimForm.json is missing or corrupt. Cannot validate.")
        return report
    
    # --- 3. Extract Truth from Claim Form ---
    try:
        sot_patient_name = claim_form_data['part_a_insured_details']['patient_name']
        sot_patient_dob = claim_form_data['part_a_insured_details']['patient_dob']
        sot_policy_id = claim_form_data['part_a_insured_details']['policy_id']
        sot_admission_date = claim_form_data['part_b_hospital_details']['admission_date']
        sot_discharge_date = claim_form_data['part_b_hospital_details']['discharge_date']
        sot_diagnosis = claim_form_data['part_b_hospital_details']['diagnosis']
        sot_hospital = claim_form_data['part_b_hospital_details']['hospital_name']
    except KeyError as e:
        report["status"] = "CRITICAL ERROR"
        report["summary"].append(f"CRITICAL: 01_ClaimForm.json is malformed. Missing key: {e}")
        return report

    sot_total_amount = None
    if final_bill_data and "_error" not in final_bill_data:
        sot_total_amount = final_bill_data.get('total_amount')

    # --- 4. Compare Each File to the Truth ---

    # File 1: 01_ClaimForm.json (Source of Truth)
    report["files_checked"]["01_ClaimForm.json"] = {
        "status": "✅ SOURCE OF TRUTH",
        "issues": []
    }

    # File 2: 02_DischargeSummary.json
    file_issues = []
    summary_data = load_json_file(os.path.join(folder_path, "02_DischargeSummary.json"))
    if summary_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in summary_data:
        file_issues.append(f"❌ File is corrupt: {summary_data['_error']}")
    else:
        if summary_data.get('patient_name') != sot_patient_name:
            file_issues.append(f"❌ Patient Name: Expected '{sot_patient_name}', Found '{summary_data.get('patient_name')}'")
        if summary_data.get('admission_date') != sot_admission_date:
            file_issues.append(f"❌ Admission Date: Expected '{sot_admission_date}', Found '{summary_data.get('admission_date')}'")
        if summary_data.get('discharge_date') != sot_discharge_date:
            file_issues.append(f"❌ Discharge Date: Expected '{sot_discharge_date}', Found '{summary_data.get('discharge_date')}'")
        if summary_data.get('final_diagnosis') != sot_diagnosis:
            file_issues.append(f"❌ Diagnosis: Expected '{sot_diagnosis}', Found '{summary_data.get('final_diagnosis')}'")
    
    report["files_checked"]["02_DischargeSummary.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ All fields match Claim Form"]
    }

    # File 3: 03_FinalHospitalBill.json
    file_issues = []
    if final_bill_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in final_bill_data:
        file_issues.append(f"❌ File is corrupt: {final_bill_data['_error']}")
    else:
        if final_bill_data.get('patient_name') != sot_patient_name:
            file_issues.append(f"❌ Patient Name: Expected '{sot_patient_name}', Found '{final_bill_data.get('patient_name')}'")
        if final_bill_data.get('admission_date') != sot_admission_date:
            file_issues.append(f"❌ Admission Date: Expected '{sot_admission_date}', Found '{final_bill_data.get('admission_date')}'")
        if 'total_amount' not in final_bill_data:
            file_issues.append("❌ Missing 'total_amount' field")
    
    report["files_checked"]["03_FinalHospitalBill.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else [f"✅ All fields match (Total: ₹{sot_total_amount})"]
    }

    # File 4: 04_PaymentReceipts.json
    file_issues = []
    receipt_data = load_json_file(os.path.join(folder_path, "04_PaymentReceipts.json"))
    if receipt_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in receipt_data:
        file_issues.append(f"❌ File is corrupt: {receipt_data['_error']}")
    else:
        if receipt_data.get('patient_name') != sot_patient_name:
            file_issues.append(f"❌ Patient Name: Expected '{sot_patient_name}', Found '{receipt_data.get('patient_name')}'")
        if sot_total_amount is not None:
            paid_amount = receipt_data.get('amount_paid')
            if paid_amount != sot_total_amount:
                diff = abs(paid_amount - sot_total_amount) if (paid_amount is not None and sot_total_amount is not None) else 0
                file_issues.append(f"❌ Amount Paid: Expected ₹{sot_total_amount}, Found ₹{paid_amount} (Diff: ₹{diff})")
    
    report["files_checked"]["04_PaymentReceipts.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ Amount matches Final Bill"]
    }

    # File 5: 05_BillBreakup.json
    file_issues = []
    breakup_data = load_json_file(os.path.join(folder_path, "05_BillBreakup.json"))
    if breakup_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in breakup_data:
        file_issues.append(f"❌ File is corrupt: {breakup_data['_error']}")
    else:
        if sot_total_amount is not None:
            calc_total = breakup_data.get('total_calculated')
            if calc_total != sot_total_amount:
                diff = abs(calc_total - sot_total_amount) if (calc_total is not None and sot_total_amount is not None) else 0
                file_issues.append(f"❌ Calculated Total: Expected ₹{sot_total_amount}, Found ₹{calc_total} (Diff: ₹{diff})")
    
    report["files_checked"]["05_BillBreakup.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ Breakup matches Final Bill"]
    }

    # File 6: 06_DoctorNotes.json
    file_issues = []
    notes_data = load_json_file(os.path.join(folder_path, "06_DoctorNotes.json"))
    if notes_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in notes_data:
        file_issues.append(f"❌ File is corrupt: {notes_data['_error']}")
    report["files_checked"]["06_DoctorNotes.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ File present and valid"]
    }

    # File 7: 07_LabReports.json
    file_issues = []
    lab_data = load_json_file(os.path.join(folder_path, "07_LabReports.json"))
    if lab_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in lab_data:
        file_issues.append(f"❌ File is corrupt: {lab_data['_error']}")
    else:
        if lab_data.get('patient_name') != sot_patient_name:
            file_issues.append(f"❌ Patient Name: Expected '{sot_patient_name}', Found '{lab_data.get('patient_name')}'")
    report["files_checked"]["07_LabReports.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ All fields match Claim Form"]
    }

    # File 8: 08_PolicyCopy.json
    file_issues = []
    policy_data = load_json_file(os.path.join(folder_path, "08_PolicyCopy.json"))
    if policy_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in policy_data:
        file_issues.append(f"❌ File is corrupt: {policy_data['_error']}")
    else:
        if policy_data.get('policy_id') != sot_policy_id:
            file_issues.append(f"❌ Policy ID: Expected '{sot_policy_id}', Found '{policy_data.get('policy_id')}'")
        if policy_data.get('policy_holder_name') != sot_patient_name:
            file_issues.append(f"❌ Policy Holder: Expected '{sot_patient_name}', Found '{policy_data.get('policy_holder_name')}'")
    report["files_checked"]["08_PolicyCopy.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ All fields match Claim Form"]
    }

    # File 9: 09_PatientID.json
    file_issues = []
    id_data = load_json_file(os.path.join(folder_path, "09_PatientID.json"))
    if id_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in id_data:
        file_issues.append(f"❌ File is corrupt: {id_data['_error']}")
    else:
        if id_data.get('patient_name_on_id') != sot_patient_name:
            file_issues.append(f"❌ Name on ID: Expected '{sot_patient_name}', Found '{id_data.get('patient_name_on_id')}'")
        if id_data.get('dob_on_id') != sot_patient_dob:
            file_issues.append(f"❌ DOB on ID: Expected '{sot_patient_dob}', Found '{id_data.get('dob_on_id')}'")
    report["files_checked"]["09_PatientID.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ All fields match Claim Form"]
    }

    # File 10: 10_BankDetails.json
    file_issues = []
    bank_data = load_json_file(os.path.join(folder_path, "10_BankDetails.json"))
    if bank_data is None:
        file_issues.append("❌ File is missing")
    elif "_error" in bank_data:
        file_issues.append(f"❌ File is corrupt: {bank_data['_error']}")
    else:
        if bank_data.get('account_holder_name') != sot_patient_name:
            file_issues.append(f"❌ Account Holder: Expected '{sot_patient_name}', Found '{bank_data.get('account_holder_name')}'")
    report["files_checked"]["10_BankDetails.json"] = {
        "status": "✅ MATCH" if not file_issues else "❌ ISSUES FOUND",
        "issues": file_issues if file_issues else ["✅ All fields match Claim Form"]
    }

    # --- 5. Calculate Final Status ---
    total_issues = sum(
        len([i for i in file_data["issues"] if i.startswith("❌")])
        for file_data in report["files_checked"].values()
    )
    
    report["total_issues"] = total_issues
    if total_issues > 0:
        report["status"] = "FRAUD DETECTED"
        report["summary"].append(f"Found {total_issues} issue(s) across {len([f for f in report['files_checked'].values() if f['status'].startswith('❌')])} file(s)")
    else:
        report["status"] = "CLEAN"
        report["summary"].append("All 10 files are present and consistent with Claim Form")

    return report

# --- 3. Define API Endpoints ---

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Claim Validation API is running. Go to /docs to use it."}

@app.post("/validate-zip-claim/", summary="Validate a claim from a .zip file")
async def validate_zip_claim(file: UploadFile = File(..., description="A .zip file containing the 10 claim JSON files.")):
    """
    **[RECOMMENDED]**
    
    Upload a .zip file of a claim folder (e.g., `claim_folder_001.zip`). 
    The API will:
    1.  Extract the files to a temporary directory.
    2.  Run the full validation logic.
    3.  Return the detailed JSON report.
    4.  Securely delete the temporary files.
    """
    if not file.filename or not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .zip file.")

    # Create a secure temporary directory
    temp_dir = tempfile.mkdtemp(prefix="claim_zip_")
    zip_path = os.path.join(temp_dir, file.filename)

    try:
        # Save the uploaded zip file to the temp dir
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Create a subdirectory to extract into
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir)

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # We need to find the folder to scan.
        # It could be `zip_root/claim_folder_001/files...` or `zip_root/files...`
        folder_to_scan = extract_dir
        extracted_items = os.listdir(extract_dir)
        
        # If the zip contains a single folder (e.g., `claim_folder_001`), dive into it
        if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_dir, extracted_items[0])):
            folder_to_scan = os.path.join(extract_dir, extracted_items[0])

        # Run the core comparison logic
        report = compare_files_to_claim_form(folder_to_scan)
        return JSONResponse(content=report)

    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="File is not a valid .zip file.")
    except Exception as e:
        # Catch-all for other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        # ALWAYS clean up the temp directory, even if errors occurred
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        await file.close()

@app.get("/validate-local-folder/", summary="Validate a local server path (FOR TESTING)")
async def validate_local_folder(
    folder_path: str = Query(
        ..., 
        description="Local path *on the server* to the claim folder.",
        examples=["claim_dataset/claim_folder_001"]
    )
):
    """
    **[FOR TESTING ONLY]**
    
    This endpoint validates a claim folder that *already exists* on the server's
    local file system. This is useful for testing your generator scripts.
    """
    if not os.path.isdir(folder_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Folder not found on server at path: {folder_path}"
        )
    
    # Run the core comparison logic
    report = compare_files_to_claim_form(folder_path)
    return JSONResponse(content=report)


# --- 3C. NEW ENDPOINT: PDF OCR Fraud Detection ---
@app.post("/detect-fraud-from-pdf/", summary="Upload PDF and Get AI + Classic Fraud Detection")
async def detect_fraud_from_pdf(
    pdf_file: UploadFile = File(..., description="The PDF file containing claim documents"),
    gemini_api_key: str = Query(
        ...,
        description="Your Google Gemini API key for OCR and fraud detection",
        examples=["AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0"]
    )
):
    """
    **NEW Endpoint**: Upload a PDF file of claim documents.
    
    This endpoint will:
    1. Perform OCR on all pages of the PDF
    2. Extract claim data using Google Gemini AI
    3. Use AI to detect fraud (returns true/false)
    4. If fraud detected, also run classic validation approach
    
    **Returns**:
    - `Final_AI_Fraud_Detection_Result`: true if fraud detected, false if clean
    - `classic_approach`: Detailed file-by-file validation (only if fraud detected)
    - `AI_analysis`: Confidence, reason, red flags, missing docs, inconsistencies
    
    **Format**:
    If fraud detected:
    {
      "Final_AI_Fraud_Detection_Result": true,
      "AI_analysis": {...},
      "classic_approach": {
        "folder_path": "...",
        "status": "FRAUD DETECTED",
        "files_checked": {...}
      }
    }
    
    If no fraud:
    {
      "Final_AI_Fraud_Detection_Result": false,
      "AI_analysis": {...},
      "classic_approach": "Not applicable - AI detected no fraud"
    }
    
    **Requirements**:
    - Tesseract OCR must be installed
    - Valid Google Gemini API key required
    - PDF should contain claim documents
    """
    
    # Check if OCR processor is available
    if not OCR_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="OCR functionality not available. Please install required packages: "
                   "pymupdf pillow pytesseract opencv-python google-generativeai numpy"
        )
    
    # Validate file type
    if not pdf_file.filename or not pdf_file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    # Save uploaded PDF to temporary file
    temp_pdf_path = None
    temp_output_folder = None
    try:
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf_path = temp_pdf.name
            # Read and write PDF content
            content = await pdf_file.read()
            temp_pdf.write(content)
        
        # Process PDF and detect fraud with classic validation callback
        result = process_pdf_and_detect_fraud(
            temp_pdf_path, 
            gemini_api_key,
            classic_validation_func=compare_files_to_claim_form
        )
        
        # Save temp folder path before cleanup
        temp_output_folder = result.get("temp_folder")
        
        # Remove temp_folder from response (internal detail)
        result.pop("temp_folder", None)
        
        # Format response according to requirements
        formatted_response = {
            "Final_AI_Fraud_Detection_Result": result.get("Final_AI_Fraud_Detection_Result", False)
        }
        
        # Add classic approach if fraud detected
        if result.get("Final_AI_Fraud_Detection_Result") and result.get("classic_approach"):
            formatted_response["classic_approach"] = result["classic_approach"]
        elif not result.get("Final_AI_Fraud_Detection_Result"):
            # No fraud detected - don't show classic approach
            pass
        
        # Add AI analysis details
        if "AI_analysis" in result:
            formatted_response["AI_analysis"] = result["AI_analysis"]
        
        # Add metadata
        if "total_pages_processed" in result:
            formatted_response["total_pages_processed"] = result["total_pages_processed"]
        
        return JSONResponse(content=formatted_response)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )
    
    finally:
        # Clean up temporary files
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.unlink(temp_pdf_path)
            except:
                pass
        
        if temp_output_folder and os.path.exists(temp_output_folder):
            try:
                shutil.rmtree(temp_output_folder)
            except:
                pass


# --- 4. Add block to run with `python main.py` ---
if __name__ == "__main__":
    """
    This allows you to run the API directly using `python main.py`.
    It will start the Uvicorn server on http://127.0.0.1:8000.
    """
    print("Starting Claim Validation API server on http://127.0.0.1:8000")
    print("Go to http://127.0.0.1:8000/docs for the API interface.")
    uvicorn.run(app, host="127.0.0.1", port=8000)

