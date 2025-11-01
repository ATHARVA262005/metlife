"""
Complete Example: Testing FastAPI with JSON File Uploads
This script demonstrates how to upload individual JSON files to the API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Sample JSON data for each file
# These are example data structures - replace with your actual data

# 1. Claim Form (REQUIRED - Source of Truth)
claim_form_data = {
    "claim_id": "CL-12345",
    "part_a_insured_details": {
        "policy_id": "POL-789456",
        "insured_name": "Rajesh Kumar",
        "patient_name": "Rajesh Kumar",
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

# 2. Discharge Summary
discharge_summary_data = {
    "patient_id": "PID-11111",
    "patient_name": "Rajesh Kumar",
    "admission_date": "2025-10-15",
    "discharge_date": "2025-10-20",
    "final_diagnosis": "Acute Appendicitis",
    "diagnosis_code": "K35.80",
    "treatment_summary": "Patient presented with acute abdominal pain... Successful Laparoscopic Appendectomy performed.",
    "doctor_in_charge": "Dr. Sharma"
}

# 3. Final Hospital Bill
final_bill_data = {
    "bill_number": "HB-2025-1234",
    "patient_id": "PID-11111",
    "patient_name": "Rajesh Kumar",
    "billing_date": "2025-10-20",
    "admission_date": "2025-10-15",
    "total_amount": 150000
}

# 4. Payment Receipts
payment_receipts_data = {
    "receipt_id": "PR-2025-5678",
    "patient_name": "Rajesh Kumar",
    "payment_date": "2025-10-20",
    "amount_paid": 150000,
    "payment_mode": "Credit Card"
}

# 5. Bill Breakup
bill_breakup_data = {
    "bill_number": "HB-2025-1234",
    "patient_id": "PID-11111",
    "line_items": [
        {"service": "Room Rent", "cost": 22500},
        {"service": "Surgeon Fees (Dr. Sharma)", "cost": 60000},
        {"service": "OT Charges (Laparoscopic Appendectomy)", "cost": 37500},
        {"service": "Medicines & Consumables", "cost": 30000}
    ],
    "total_calculated": 150000
}

# 6. Doctor Notes
doctor_notes_data = {
    "patient_id": "PID-11111",
    "consultation_date": "2025-10-15",
    "doctor_name": "Dr. Sharma",
    "notes": "Patient presented with acute abdominal pain...",
    "prescription": [
        {"drug": "IV Fluids", "dosage": "STAT"},
        {"drug": "Antibiotics (Pre-Op)", "dosage": "STAT"},
        {"drug": "Painkiller (SOS)", "dosage": "SOS"}
    ]
}

# 7. Lab Reports
lab_reports_data = {
    "report_id": "LAB-99999",
    "patient_id": "PID-11111",
    "patient_name": "Rajesh Kumar",
    "test_name": "Complete Blood Count (CBC)",
    "test_date": "2025-10-15",
    "result": "See attached film / values.",
    "analysis": "Findings consistent with Acute Appendicitis."
}

# 8. Policy Copy
policy_copy_data = {
    "policy_id": "POL-789456",
    "policy_holder_name": "Rajesh Kumar",
    "valid_from": "2025-01-01",
    "valid_to": "2025-12-31",
    "status": "Active"
}

# 9. Patient ID
patient_id_data = {
    "patient_name_on_id": "Rajesh Kumar",
    "id_type": "Aadhaar Card",
    "id_number_masked": "XXXX-XXXX-1234",
    "dob_on_id": "1985-05-15"
}

# 10. Bank Details
bank_details_data = {
    "account_holder_name": "Rajesh Kumar",
    "bank_name": "HDFC Bank",
    "account_number_masked": "XXXXXX5678",
    "ifsc_code": "HDFC0123456"
}


def save_json_files_locally():
    """Save all JSON data to local files for upload"""
    import os
    
    test_folder = "test_claim_files"
    os.makedirs(test_folder, exist_ok=True)
    
    files_data = {
        "01_ClaimForm.json": claim_form_data,
        "02_DischargeSummary.json": discharge_summary_data,
        "03_FinalHospitalBill.json": final_bill_data,
        "04_PaymentReceipts.json": payment_receipts_data,
        "05_BillBreakup.json": bill_breakup_data,
        "06_DoctorNotes.json": doctor_notes_data,
        "07_LabReports.json": lab_reports_data,
        "08_PolicyCopy.json": policy_copy_data,
        "09_PatientID.json": patient_id_data,
        "10_BankDetails.json": bank_details_data
    }
    
    for filename, data in files_data.items():
        filepath = os.path.join(test_folder, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Created: {filepath}")
    
    return test_folder


def test_upload_all_files():
    """Test uploading all files at once"""
    print("\n" + "="*80)
    print("TEST 1: Upload All Files at Once")
    print("="*80)
    
    # Save files locally first
    test_folder = save_json_files_locally()
    
    # Prepare files for upload
    files = [
        ('files', ('01_ClaimForm.json', open(f'{test_folder}/01_ClaimForm.json', 'rb'), 'application/json')),
        ('files', ('02_DischargeSummary.json', open(f'{test_folder}/02_DischargeSummary.json', 'rb'), 'application/json')),
        ('files', ('03_FinalHospitalBill.json', open(f'{test_folder}/03_FinalHospitalBill.json', 'rb'), 'application/json')),
        ('files', ('04_PaymentReceipts.json', open(f'{test_folder}/04_PaymentReceipts.json', 'rb'), 'application/json')),
        ('files', ('05_BillBreakup.json', open(f'{test_folder}/05_BillBreakup.json', 'rb'), 'application/json')),
        ('files', ('06_DoctorNotes.json', open(f'{test_folder}/06_DoctorNotes.json', 'rb'), 'application/json')),
        ('files', ('07_LabReports.json', open(f'{test_folder}/07_LabReports.json', 'rb'), 'application/json')),
        ('files', ('08_PolicyCopy.json', open(f'{test_folder}/08_PolicyCopy.json', 'rb'), 'application/json')),
        ('files', ('09_PatientID.json', open(f'{test_folder}/09_PatientID.json', 'rb'), 'application/json')),
        ('files', ('10_BankDetails.json', open(f'{test_folder}/10_BankDetails.json', 'rb'), 'application/json'))
    ]
    
    print("\n📤 Uploading all 10 files to /validate endpoint...")
    response = requests.post(f'{BASE_URL}/validate', files=files)
    
    # Close file handles
    for _, file_tuple in files:
        file_tuple[1].close()
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Upload Successful!")
        print(f"\nClaim ID: {result['claim_id']}")
        print(f"Files Uploaded: {result['files_uploaded_count']}")
        print(f"Folder Path: {result['folder_path']}")
        
        print("\n" + "-"*80)
        print("VALIDATION RESULTS")
        print("-"*80)
        print(f"Status: {result['validation_report']['status']}")
        print(f"Total Issues: {result['validation_report']['total_issues']}")
        
        print("\nFile-by-File Results:")
        for filename, file_data in result['validation_report']['files_checked'].items():
            print(f"\n📄 {filename}")
            print(f"   Status: {file_data['status']}")
            for issue in file_data['issues'][:2]:  # Show first 2 issues
                print(f"      {issue}")
        
        return result['claim_id']
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.json())
        return None


def test_upload_one_by_one(claim_id="my_test_claim"):
    """Test uploading files one by one"""
    print("\n" + "="*80)
    print("TEST 2: Upload Files One by One")
    print("="*80)
    
    test_folder = "test_claim_files"
    
    files_to_upload = [
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
    ]
    
    print(f"\nClaim ID: {claim_id}")
    print(f"Uploading files one by one to /upload/single endpoint...\n")
    
    for filename in files_to_upload:
        filepath = f"{test_folder}/{filename}"
        
        with open(filepath, 'rb') as f:
            files = {'file': (filename, f, 'application/json')}
            response = requests.post(
                f'{BASE_URL}/upload/single',
                params={'claim_id': claim_id},
                files=files
            )
        
        if response.status_code == 200:
            print(f"✅ {filename} uploaded successfully")
        else:
            print(f"❌ {filename} failed: {response.json()}")
    
    # Now validate the claim
    print(f"\n📋 Validating claim: {claim_id}")
    response = requests.get(f'{BASE_URL}/validate/{claim_id}')
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Validation Complete!")
        print(f"Status: {result['validation_report']['status']}")
        print(f"Total Issues: {result['validation_report']['total_issues']}")
    else:
        print(f"❌ Validation failed: {response.json()}")


def test_with_fraud_data():
    """Test with fraudulent data (amount mismatch)"""
    print("\n" + "="*80)
    print("TEST 3: Upload with Fraud (Amount Mismatch)")
    print("="*80)
    
    # Modify payment receipt to have different amount (fraud!)
    fraudulent_payment_data = payment_receipts_data.copy()
    fraudulent_payment_data['amount_paid'] = 120000  # Less than bill amount!
    
    test_folder = "test_claim_fraud"
    import os
    os.makedirs(test_folder, exist_ok=True)
    
    # Save files
    files_data = {
        "01_ClaimForm.json": claim_form_data,
        "03_FinalHospitalBill.json": final_bill_data,
        "04_PaymentReceipts.json": fraudulent_payment_data
    }
    
    for filename, data in files_data.items():
        with open(f"{test_folder}/{filename}", 'w') as f:
            json.dump(data, f, indent=2)
    
    # Upload
    files = [
        ('files', ('01_ClaimForm.json', open(f'{test_folder}/01_ClaimForm.json', 'rb'), 'application/json')),
        ('files', ('03_FinalHospitalBill.json', open(f'{test_folder}/03_FinalHospitalBill.json', 'rb'), 'application/json')),
        ('files', ('04_PaymentReceipts.json', open(f'{test_folder}/04_PaymentReceipts.json', 'rb'), 'application/json'))
    ]
    
    print("\n📤 Uploading files with fraudulent data...")
    response = requests.post(f'{BASE_URL}/validate', files=files)
    
    for _, file_tuple in files:
        file_tuple[1].close()
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Upload Successful!")
        print(f"Claim ID: {result['claim_id']}")
        
        print("\n🚨 VALIDATION RESULTS:")
        print(f"Status: {result['validation_report']['status']}")
        print(f"Total Issues: {result['validation_report']['total_issues']}")
        
        if result['validation_report']['total_issues'] > 0:
            print("\n❌ FRAUD DETECTED!")
            for filename, file_data in result['validation_report']['files_checked'].items():
                if file_data['status'].startswith('❌'):
                    print(f"\nFile: {filename}")
                    for issue in file_data['issues']:
                        print(f"   {issue}")


def test_direct_json_post():
    """Test sending JSON data directly without files"""
    print("\n" + "="*80)
    print("TEST 4: Direct JSON POST (Alternative Method)")
    print("="*80)
    print("\nNote: This would require a different endpoint.")
    print("Current API uses multipart/form-data for file uploads.")
    print("If you need pure JSON POST, we can add a new endpoint!")


def list_all_claims():
    """List all uploaded claims"""
    print("\n" + "="*80)
    print("Listing All Claims")
    print("="*80)
    
    response = requests.get(f'{BASE_URL}/claims/list')
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTotal Claims: {result['count']}")
        
        for claim in result['claims']:
            print(f"\n📁 {claim['claim_id']}")
            print(f"   Files: {claim['files_count']}")
            print(f"   Location: {claim['folder_path']}")


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("FASTAPI CLAIM VALIDATION - COMPLETE TEST SUITE")
    print("#"*80)
    print("\n🔗 API URL:", BASE_URL)
    print("📝 Make sure the server is running: python main.py")
    print()
    
    try:
        # Check if server is running
        health = requests.get(f'{BASE_URL}/health', timeout=2)
        if health.status_code != 200:
            raise Exception("Server not responding")
        
        print("✅ Server is running!\n")
        
        # Run tests
        input("Press Enter to run TEST 1 (Upload All Files)...")
        claim_id = test_upload_all_files()
        
        input("\nPress Enter to run TEST 2 (Upload One by One)...")
        test_upload_one_by_one("my_manual_claim_001")
        
        input("\nPress Enter to run TEST 3 (Fraud Detection)...")
        test_with_fraud_data()
        
        input("\nPress Enter to list all claims...")
        list_all_claims()
        
        print("\n" + "#"*80)
        print("ALL TESTS COMPLETED!")
        print("#"*80)
        print("\n💡 Tips:")
        print("1. Check 'uploads/' folder to see stored files")
        print("2. Use Swagger UI at http://localhost:8000/docs")
        print("3. Modify JSON data in this file to test different scenarios")
        print()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Please start the server first: python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
