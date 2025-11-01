import os
import json
from typing import Any, Dict, Optional

def load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Safely loads a JSON file, returning None if it's missing or invalid."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"_error": "Invalid JSON format"}

def compare_files_to_claim_form(folder_path):
    """
    This is the core logic.
    It compares all files *inside* one folder to the 01_ClaimForm.json.
    Returns a detailed report with file-by-file comparison results.
    """
    report = {
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
                diff = abs(paid_amount - sot_total_amount) if paid_amount else 0
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
                diff = abs(calc_total - sot_total_amount) if calc_total else 0
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
        report["summary"].append("All files are consistent with Claim Form")

    return report

# --- How to Use This Function ---

def print_detailed_report(report):
    """Print a detailed comparison report."""
    print("\n" + "="*80)
    print(f"CLAIM VALIDATION REPORT")
    print("="*80)
    print(f"Folder: {report['folder_path']}")
    print(f"Status: {report['status']}")
    print("="*80 + "\n")
    
    for filename, file_data in report["files_checked"].items():
        print(f"📄 {filename}")
        print(f"   Status: {file_data['status']}")
        for issue in file_data['issues']:
            print(f"      {issue}")
        print()
    
    print("="*80)
    print(f"FINAL VERDICT: {report['status']}")
    if report['total_issues'] > 0:
        print(f"Total Issues Found: {report['total_issues']}")
    for summary in report['summary']:
        print(f"   {summary}")
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    
    # Get folder path from command line or use default
    if len(sys.argv) > 1:
        my_claim_folder = sys.argv[1]
    else:
        my_claim_folder = "claim_folder_001"  # Default to the attached folder
    
    if not os.path.exists(my_claim_folder):
        print(f"❌ Error: Folder '{my_claim_folder}' does not exist.")
        print("\nUsage: python compatre.py <folder_path>")
        print("Example: python compatre.py claim_folder_001")
        sys.exit(1)
    
    print(f"\n🔍 Validating Claim Folder: {my_claim_folder}")
    
    # Run the comparison
    report = compare_files_to_claim_form(my_claim_folder)
    
    # Print detailed report
    print_detailed_report(report)