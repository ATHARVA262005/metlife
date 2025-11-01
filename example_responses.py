"""
Example response formats for the PDF Fraud Detection API
"""

# Example 1: Fraud Detected (AI finds issues)
fraud_detected_response = {
    "Final_AI_Fraud_Detection_Result": True,
    "AI_analysis": {
        "confidence": "High",
        "reason": "Patient name inconsistency detected across multiple documents",
        "red_flags": [
            "Name mismatch between Claim Form and Discharge Summary",
            "Missing bank statement document"
        ],
        "missing_documents": [
            "Bank Statement"
        ],
        "inconsistencies": [
            "Patient name 'Vedika Tara' in Claim Form vs 'Vedika' in Discharge Summary"
        ]
    },
    "classic_approach": {
        "folder_path": "temp_extracted_data",
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
                "issues": [
                    "✅ All fields match (Total: ₹260800)"
                ]
            },
            "04_PaymentReceipts.json": {
                "status": "✅ MATCH",
                "issues": [
                    "✅ Amount matches Final Bill"
                ]
            },
            "05_BillBreakup.json": {
                "status": "✅ MATCH",
                "issues": [
                    "✅ Breakup matches Final Bill"
                ]
            },
            "06_DoctorNotes.json": {
                "status": "✅ MATCH",
                "issues": [
                    "✅ File present and valid"
                ]
            },
            "07_LabReports.json": {
                "status": "✅ MATCH",
                "issues": [
                    "✅ All fields match Claim Form"
                ]
            },
            "08_PolicyCopy.json": {
                "status": "✅ MATCH",
                "issues": [
                    "✅ All fields match Claim Form"
                ]
            },
            "09_PatientID.json": {
                "status": "✅ MATCH",
                "issues": [
                    "✅ All fields match Claim Form"
                ]
            },
            "10_BankDetails.json": {
                "status": "✅ MATCH",
                "issues": [
                    "✅ All fields match Claim Form"
                ]
            }
        },
        "summary": [
            "Found 1 issue(s) across 1 file(s)"
        ]
    },
    "total_pages_processed": 10
}


# Example 2: No Fraud Detected (Clean claim)
clean_response = {
    "Final_AI_Fraud_Detection_Result": False,
    "AI_analysis": {
        "confidence": "High",
        "reason": "All documents are consistent and complete",
        "red_flags": [],
        "missing_documents": [],
        "inconsistencies": []
    },
    "total_pages_processed": 10
}


# How to interpret the response:

def interpret_response(response):
    """
    Helper function to interpret the API response
    """
    if response["Final_AI_Fraud_Detection_Result"]:
        print("🚨 FRAUD DETECTED!")
        print(f"   Confidence: {response['AI_analysis']['confidence']}")
        print(f"   Reason: {response['AI_analysis']['reason']}")
        
        if "classic_approach" in response and response["classic_approach"]:
            print("\n📋 Classic Validation Details:")
            classic = response["classic_approach"]
            print(f"   Status: {classic['status']}")
            print(f"   Total Issues: {classic['total_issues']}")
            
            # Show files with issues
            for filename, file_data in classic["files_checked"].items():
                if file_data["status"].startswith("❌"):
                    print(f"\n   {filename}:")
                    for issue in file_data["issues"]:
                        print(f"      {issue}")
    else:
        print("✅ CLEAN - No Fraud Detected")
        print(f"   AI Confidence: {response['AI_analysis']['confidence']}")
        print(f"   Reason: {response['AI_analysis']['reason']}")


if __name__ == "__main__":
    print("=" * 80)
    print("EXAMPLE 1: Fraud Detected Response")
    print("=" * 80)
    interpret_response(fraud_detected_response)
    
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Clean Response")
    print("=" * 80)
    interpret_response(clean_response)
