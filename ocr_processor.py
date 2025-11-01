import os
import json
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import numpy as np
import cv2
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import tempfile

# Set Tesseract executable path (Windows example)
pytesseract.pytesseract.tesseract_cmd = r"D:\hackathon\metlife\3\libraries\tesseract.exe"

def ocr_page_to_text(page, zoom=2.0):
    """Extract text from a PDF page using OCR."""
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)  # Use tuple instead of list
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return pytesseract.image_to_string(img_cv)

def extract_claim_with_gemini(full_text: str, api_key: str) -> str:
    """Extract structured claim data from text using Gemini API."""
    
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    instruction = (
        "You are an information extraction system for Indian health insurance claims. "
        "Extract fields exactly according to the following format as JSON:\n"
        "{\n"
        "  'file_name': string,\n"
        "  'claim_id': string,\n"
        "  'policy_number': string,\n"
        "  'insurer_name': string (REQUIRED),\n"
        "  'insured_name': string (REQUIRED),\n"
        "  'patient_name': string,\n"
        "  'relationship_to_insured': string,\n"
        "  'date_of_birth': string (YYYY-MM-DD),\n"
        "  'hospital_name': string,\n"
        "  'hospital_address': string,\n"
        "  'admission_date': string (YYYY-MM-DD),\n"
        "  'discharge_date': string (YYYY-MM-DD),\n"
        "  'diagnosis': string,\n"
        "  'procedure': string,\n"
        "  'doctor_name': string,\n"
        "  'claim_amount': string,\n"
        "  'currency': string,\n"
        "  'bank_account': {account_name, account_number, ifsc, bank_name, branch},\n"
        "  'contact': {phone, email, address},\n"
        "  'document_types': array of strings (identify: lab report, doctor notes, bill breakup, "
        "payment receipt, final hospital bill, discharge summary, claim form, policy copy, patient id, bank statement),\n"
        "  'missing_fields': array of field names that were not found,\n"
        "  'notes': string\n"
        "}\n\n"
        "Extract exact strings from the text. If a field is missing, leave it empty and add to missing_fields. "
        "Return only valid JSON."
    )

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([instruction, full_text])
    return response.text

def process_pdf_to_json(pdf_path: str, output_folder: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Process a PDF file to extract claim data from all pages.
    Returns a list of extracted claim data dictionaries.
    """
    doc = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    all_extracted_data = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        page_text = ocr_page_to_text(page, zoom=2.0)

        # Save OCR text for debugging
        with open(os.path.join(output_folder, f"ocr_text_page_{i+1}.txt"), "w", encoding="utf-8") as f:
            f.write(page_text)

        # Extract claim JSON via Gemini
        page_json = extract_claim_with_gemini(page_text, api_key)

        # Save JSON per page
        json_path = os.path.join(output_folder, f"claim_extracted_page_{i+1}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(page_json)

        try:
            parsed = json.loads(page_json)
            # Filter out unwanted keys
            filtered_entry = dict(parsed)
            filtered_entry.pop("missing_fields", None)
            filtered_entry.pop("line_items", None)
            all_extracted_data.append(filtered_entry)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON from page {i+1}")
            continue

    # Save combined filtered data
    filtered_combined_path = os.path.join(output_folder, "filtered_combined.json")
    with open(filtered_combined_path, "w", encoding="utf-8") as f:
        json.dump(all_extracted_data, f, indent=2, ensure_ascii=False)

    return all_extracted_data

def calculate_fraud_score(extracted_data: List[Dict[str, Any]], api_key: str) -> Dict[str, Any]:
    """
    Analyze extracted claim data and return a boolean fraud detection result.
    Returns True if fraud detected, False if clean.
    """
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    prompt_instruction = """
You are an expert insurance fraud detection analyst.

Analyze the following insurance claim data given as JSON objects. Pay special attention to:
1. Consistency of patient names, dates, and amounts across documents
2. Missing required documents (should have: claim form, discharge summary, hospital bill, payment receipt, policy copy, patient id, bank details)
3. Suspicious patterns in amounts or dates
4. Name mismatches between documents
5. Date inconsistencies (admission/discharge dates)

Determine if this claim is fraudulent or clean.

Return your response as a JSON object with:
{
    "fraud_detected": true or false,
    "confidence": "High" or "Medium" or "Low",
    "reason": "brief explanation of the decision",
    "red_flags": ["list of specific issues found if fraud detected"],
    "missing_documents": ["list of missing document types"],
    "inconsistencies": ["list of data inconsistencies"]
}
"""
    data_text = json.dumps(extracted_data, indent=2, ensure_ascii=False)

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt_instruction, data_text])
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "fraud_detected": True,
            "confidence": "Low",
            "reason": "Error in fraud detection analysis",
            "red_flags": ["Unable to parse fraud detection response"],
            "missing_documents": [],
            "inconsistencies": []
        }

def process_pdf_and_detect_fraud(pdf_path: str, api_key: str, classic_validation_func=None) -> Dict[str, Any]:
    """
    Main function: Process PDF and return fraud detection results.
    Combines AI detection with optional classic approach validation.
    """
    # Create temporary directory for extracted data
    temp_dir = tempfile.mkdtemp(prefix="claim_ocr_")
    
    try:
        # Extract data from PDF
        extracted_data = process_pdf_to_json(pdf_path, temp_dir, api_key)
        
        if not extracted_data:
            return {
                "success": False,
                "error": "No data could be extracted from the PDF",
                "Final_AI_Fraud_Detection_Result": True,
                "classic_approach": None
            }
        
        # Calculate fraud detection using AI
        fraud_analysis = calculate_fraud_score(extracted_data, api_key)
        
        fraud_detected = fraud_analysis.get("fraud_detected", False)
        
        # Prepare response
        result = {
            "success": True,
            "Final_AI_Fraud_Detection_Result": fraud_detected,
            "AI_analysis": {
                "confidence": fraud_analysis.get("confidence", "Unknown"),
                "reason": fraud_analysis.get("reason", ""),
                "red_flags": fraud_analysis.get("red_flags", []),
                "missing_documents": fraud_analysis.get("missing_documents", []),
                "inconsistencies": fraud_analysis.get("inconsistencies", [])
            },
            "total_pages_processed": len(extracted_data),
            "temp_folder": temp_dir
        }
        
        # If fraud detected and classic validation function provided, run it
        if fraud_detected and classic_validation_func:
            # Create the expected JSON files from extracted data
            # Map document types to expected filenames
            file_mapping = {
                "claim form": "01_ClaimForm.json",
                "discharge summary": "02_DischargeSummary.json",
                "final hospital bill": "03_FinalHospitalBill.json",
                "payment receipt": "04_PaymentReceipts.json",
                "bill breakup": "05_BillBreakup.json",
                "doctor notes": "06_DoctorNotes.json",
                "lab report": "07_LabReports.json",
                "policy copy": "08_PolicyCopy.json",
                "patient id": "09_PatientID.json",
                "bank details": "10_BankDetails.json",
                "bank statement": "10_BankDetails.json"
            }
            
            # Create standardized JSON files for classic validation
            for doc_data in extracted_data:
                doc_types = doc_data.get("document_types", [])
                for doc_type in doc_types:
                    doc_type_lower = doc_type.lower()
                    if doc_type_lower in file_mapping:
                        filename = file_mapping[doc_type_lower]
                        filepath = os.path.join(temp_dir, filename)
                        # Only write if file doesn't exist (first match wins)
                        if not os.path.exists(filepath):
                            with open(filepath, 'w', encoding='utf-8') as f:
                                json.dump(doc_data, f, indent=2, ensure_ascii=False)
            
            # Run classic validation
            try:
                classic_result = classic_validation_func(temp_dir)
                result["classic_approach"] = classic_result
            except Exception as e:
                result["classic_approach"] = {
                    "error": f"Classic validation failed: {str(e)}",
                    "note": "AI fraud detection completed successfully"
                }
        else:
            result["classic_approach"] = None
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "Final_AI_Fraud_Detection_Result": True,
            "classic_approach": None
        }
