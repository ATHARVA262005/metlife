"""
Test script for the FastAPI Claim Validation API
"""

import requests
import json
import os

# API Configuration
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_upload_and_validate(folder_path="claim_folder_001"):
    """Test upload and validate endpoint"""
    print("\n" + "="*60)
    print(f"Testing Upload & Validate with folder: {folder_path}")
    print("="*60)
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' not found")
        return
    
    # Prepare files
    files = []
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    print(f"\nUploading {len(json_files)} files...")
    for filename in json_files:
        file_path = os.path.join(folder_path, filename)
        files.append(
            ('files', (filename, open(file_path, 'rb'), 'application/json'))
        )
    
    # Make request
    response = requests.post(f"{BASE_URL}/validate", files=files)
    
    # Close files
    for _, file_tuple in files:
        file_tuple[1].close()
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Claim ID: {result['claim_id']}")
        print(f"Files Uploaded: {result['files_uploaded_count']}")
        print(f"\nValidation Status: {result['validation_report']['status']}")
        print(f"Total Issues: {result['validation_report']['total_issues']}")
        
        print("\n" + "-"*60)
        print("File-by-File Validation Results:")
        print("-"*60)
        for filename, file_data in result['validation_report']['files_checked'].items():
            print(f"\n📄 {filename}")
            print(f"   Status: {file_data['status']}")
            for issue in file_data['issues'][:2]:  # Show first 2 issues
                print(f"      {issue}")
    else:
        print(f"❌ Error: {response.json()}")


def test_list_claims():
    """Test list all claims endpoint"""
    print("\n" + "="*60)
    print("Testing List All Claims")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/claims/list")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTotal Claims: {result['count']}")
        for claim in result['claims'][:5]:  # Show first 5
            print(f"\n  Claim ID: {claim['claim_id']}")
            print(f"  Files: {claim['files_count']}")
    else:
        print(f"Error: {response.json()}")


def test_validate_existing(claim_id):
    """Test validate existing claim endpoint"""
    print("\n" + "="*60)
    print(f"Testing Validate Existing Claim: {claim_id}")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/validate/{claim_id}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nValidation Status: {result['validation_report']['status']}")
        print(f"Total Issues: {result['validation_report']['total_issues']}")
    else:
        print(f"Error: {response.json()}")


def test_required_files():
    """Test get required files endpoint"""
    print("\n" + "="*60)
    print("Testing Get Required Files")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/files/required")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nRequired Files ({result['count']}):")
        for i, filename in enumerate(result['required_files'], 1):
            print(f"  {i}. {filename}")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("CLAIM VALIDATION API - TEST SUITE")
    print("#"*60)
    
    try:
        # Test 1: Health Check
        test_health()
        
        # Test 2: Get Required Files
        test_required_files()
        
        # Test 3: Upload and Validate
        test_upload_and_validate("claim_folder_001")
        
        # Test 4: List All Claims
        test_list_claims()
        
        print("\n" + "#"*60)
        print("TEST SUITE COMPLETED")
        print("#"*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
