"""
Test script to demonstrate the combined AI + Classic approach response
This simulates what happens when AI detects fraud and runs classic validation
"""

import json
from compatre import compare_files_to_claim_form

# Simulate the response format when fraud is detected
def generate_sample_response():
    """
    Generate a sample response showing what the API returns when fraud is detected.
    This combines AI fraud detection with classic validation approach.
    """
    
    # Run classic validation on claim_folder_001
    classic_result = compare_files_to_claim_form("claim_folder_001")
    
    # Simulate AI fraud detection result
    ai_fraud_result = {
        "fraud_detected": True,
        "confidence": "High",
        "reason": "Patient name inconsistency detected in discharge summary",
        "red_flags": [
            "Patient name mismatch: 'Vedika Tara' vs 'Vedika'",
            "Potential identity fraud or data entry error"
        ],
        "missing_documents": [],
        "inconsistencies": [
            "Name field differs between Claim Form and Discharge Summary"
        ]
    }
    
    # Build the final response in the requested format
    final_response = {
        "Final_AI_Fraud_Detection_Result": True,
        "AI_analysis": {
            "confidence": ai_fraud_result["confidence"],
            "reason": ai_fraud_result["reason"],
            "red_flags": ai_fraud_result["red_flags"],
            "missing_documents": ai_fraud_result["missing_documents"],
            "inconsistencies": ai_fraud_result["inconsistencies"]
        },
        "classic_approach": classic_result,
        "total_pages_processed": 10
    }
    
    return final_response

if __name__ == "__main__":
    print("\n" + "="*80)
    print("SAMPLE API RESPONSE - FRAUD DETECTED")
    print("="*80)
    print("\nThis is what the API returns when:")
    print("1. AI detects fraud (Final_AI_Fraud_Detection_Result = true)")
    print("2. Classic validation runs on the claim folder")
    print("\n" + "="*80)
    
    # Generate the response
    response = generate_sample_response()
    
    # Pretty print the response
    print("\n📋 COMPLETE API RESPONSE:\n")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    print("\n" + "="*80)
    print("RESPONSE BREAKDOWN:")
    print("="*80)
    
    print(f"\n✅ Final AI Result: {response['Final_AI_Fraud_Detection_Result']}")
    print(f"✅ AI Confidence: {response['AI_analysis']['confidence']}")
    print(f"✅ AI Reason: {response['AI_analysis']['reason']}")
    
    print(f"\n🚩 Red Flags ({len(response['AI_analysis']['red_flags'])}):")
    for flag in response['AI_analysis']['red_flags']:
        print(f"   • {flag}")
    
    print(f"\n📊 Classic Approach Status: {response['classic_approach']['status']}")
    print(f"📊 Total Issues Found: {response['classic_approach']['total_issues']}")
    
    print(f"\n📄 Files Checked: {len(response['classic_approach']['files_checked'])}")
    for filename, file_data in response['classic_approach']['files_checked'].items():
        print(f"   {filename}: {file_data['status']}")
    
    print("\n" + "="*80)
    print("🎯 KEY INSIGHT:")
    print("="*80)
    print("When AI detects fraud, the response includes BOTH:")
    print("1. AI analysis (confidence, reasons, red flags)")
    print("2. Classic approach (detailed file-by-file validation)")
    print("\nThis gives you the best of both worlds - AI speed + detailed validation!")
    print("="*80 + "\n")
