"""
Test script for the new PDF Fraud Detection API endpoint
"""

import requests
import os

# Configuration
API_URL = "http://127.0.0.1:8000/detect-fraud-from-pdf/"
PDF_FILE_PATH = r"D:\sankar_projects\hack\merged.pdf"  # Update this path
GEMINI_API_KEY = "AIzaSyAihflqadt3dQmXsuXPK-ItB4DCaWEZwR0"  # Update with your API key

def test_pdf_fraud_detection():
    """Test the PDF fraud detection endpoint."""
    
    # Check if PDF file exists
    if not os.path.exists(PDF_FILE_PATH):
        print(f"❌ Error: PDF file not found at {PDF_FILE_PATH}")
        print("Please update PDF_FILE_PATH in this script.")
        return
    
    print(f"📄 Testing PDF: {PDF_FILE_PATH}")
    print(f"🔗 API Endpoint: {API_URL}")
    print("⏳ Processing... (This may take a minute for OCR)\n")
    
    try:
        # Prepare the request
        with open(PDF_FILE_PATH, 'rb') as pdf_file:
            files = {
                'pdf_file': (os.path.basename(PDF_FILE_PATH), pdf_file, 'application/pdf')
            }
            params = {
                'gemini_api_key': GEMINI_API_KEY
            }
            
            # Send request
            response = requests.post(API_URL, files=files, params=params)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            print("=" * 80)
            print("✅ FRAUD DETECTION RESULT")
            print("=" * 80)
            print(f"Success: {result.get('success', False)}")
            print(f"Fraud Score: {result.get('fraud_score', 'N/A')}/100")
            print(f"Risk Level: {result.get('risk_level', 'N/A')}")
            print(f"Pages Processed: {result.get('total_pages_processed', 'N/A')}")
            print("\n📋 Summary:")
            print(f"   {result.get('summary', 'No summary available')}")
            
            if result.get('red_flags'):
                print("\n🚩 Red Flags Detected:")
                for flag in result['red_flags']:
                    print(f"   • {flag}")
            
            if result.get('missing_documents'):
                print("\n📄 Missing Documents:")
                for doc in result['missing_documents']:
                    print(f"   • {doc}")
            
            if result.get('inconsistencies'):
                print("\n⚠️  Inconsistencies Found:")
                for issue in result['inconsistencies']:
                    print(f"   • {issue}")
            
            print("\n📊 Extracted Data:")
            if result.get('extracted_data'):
                print(f"   Total documents extracted: {len(result['extracted_data'])}")
                for i, doc in enumerate(result['extracted_data'], 1):
                    doc_types = doc.get('document_types', [])
                    print(f"   Page {i}: {', '.join(doc_types) if doc_types else 'Unknown document type'}")
            
            print("=" * 80)
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the FastAPI server is running.")
        print("   Start it with: python main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("\n🔍 PDF Fraud Detection API Test\n")
    test_pdf_fraud_detection()
