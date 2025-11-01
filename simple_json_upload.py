"""
Simple Example: How to Insert JSON Files into FastAPI
This shows the easiest way to upload JSON data to the API
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8000/validate"

# Step 1: Define your JSON data for each file
# You can copy-paste your actual JSON data here

claim_form = {
    "claim_id": "CL-12345",
    "part_a_insured_details": {
        "policy_id": "POL-789456",
        "insured_name": "John Doe",
        "patient_name": "John Doe",
        "patient_dob": "1985-05-15"
    },
    "part_b_hospital_details": {
        "hospital_name": "Apollo Hospital",
        "admission_date": "2025-10-15",
        "discharge_date": "2025-10-20",
        "diagnosis": "Acute Appendicitis",
        "procedure_performed": "Laparoscopic Appendectomy"
    }
}

discharge_summary = {
    "patient_id": "PID-11111",
    "patient_name": "John Doe",
    "admission_date": "2025-10-15",
    "discharge_date": "2025-10-20",
    "final_diagnosis": "Acute Appendicitis",
    "diagnosis_code": "K35.80",
    "treatment_summary": "Successful surgery performed",
    "doctor_in_charge": "Dr. Smith"
}

final_bill = {
    "bill_number": "HB-2025-1234",
    "patient_id": "PID-11111",
    "patient_name": "John Doe",
    "billing_date": "2025-10-20",
    "admission_date": "2025-10-15",
    "total_amount": 150000
}

payment_receipt = {
    "receipt_id": "PR-2025-5678",
    "patient_name": "John Doe",
    "payment_date": "2025-10-20",
    "amount_paid": 150000,
    "payment_mode": "Credit Card"
}

# Add more files as needed...

# Step 2: Convert JSON to files and upload
def upload_json_data():
    """Upload JSON data to the API"""
    
    # Save JSON to temporary files
    import os
    import tempfile
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Dictionary of all files to upload
    files_data = {
        "01_ClaimForm.json": claim_form,
        "02_DischargeSummary.json": discharge_summary,
        "03_FinalHospitalBill.json": final_bill,
        "04_PaymentReceipts.json": payment_receipt
        # Add more files here
    }
    
    # Save each JSON to a file
    file_paths = {}
    for filename, data in files_data.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        file_paths[filename] = filepath
    
    # Prepare files for upload
    files = []
    for filename, filepath in file_paths.items():
        files.append(
            ('files', (filename, open(filepath, 'rb'), 'application/json'))
        )
    
    # Upload to API
    print("📤 Uploading files to API...")
    response = requests.post(API_URL, files=files)
    
    # Close file handles
    for _, file_tuple in files:
        file_tuple[1].close()
    
    # Clean up temp files
    import shutil
    shutil.rmtree(temp_dir)
    
    # Return response
    return response


# Step 3: Run the upload and see results
if __name__ == "__main__":
    print("="*60)
    print("UPLOADING JSON DATA TO FASTAPI")
    print("="*60)
    
    try:
        response = upload_json_data()
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ SUCCESS!")
            print(f"\nClaim ID: {result['claim_id']}")
            print(f"Files Uploaded: {result['files_uploaded_count']}")
            print(f"Stored in: {result['folder_path']}")
            
            print("\n📋 VALIDATION RESULTS:")
            print(f"Status: {result['validation_report']['status']}")
            print(f"Issues Found: {result['validation_report']['total_issues']}")
            
            if result['validation_report']['total_issues'] == 0:
                print("\n✅ All files are consistent!")
            else:
                print("\n❌ Issues detected:")
                for filename, data in result['validation_report']['files_checked'].items():
                    if data['status'].startswith('❌'):
                        print(f"\n{filename}:")
                        for issue in data['issues']:
                            print(f"  {issue}")
            
            # Print full response
            print("\n" + "="*60)
            print("FULL RESPONSE:")
            print("="*60)
            print(json.dumps(result, indent=2))
            
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
