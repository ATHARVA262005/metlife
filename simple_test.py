"""
Simple script to create a ZIP file and test the FastAPI
"""

import zipfile
import os
import requests
import json

def create_zip_from_folder(folder_path, output_zip):
    """Create a ZIP file from a claim folder"""
    print(f"\n📦 Creating ZIP file: {output_zip}")
    print(f"   From folder: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"   ❌ Error: Folder '{folder_path}' not found!")
        return False
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        
        if not json_files:
            print(f"   ❌ Error: No JSON files found in '{folder_path}'!")
            return False
        
        for file in json_files:
            file_path = os.path.join(folder_path, file)
            # Add file to ZIP with the folder name as root
            arcname = os.path.join(os.path.basename(folder_path), file)
            zipf.write(file_path, arcname)
            print(f"   ✅ Added: {file}")
    
    print(f"\n✅ ZIP file created successfully: {output_zip}")
    return True


def test_api_with_zip(zip_file_path):
    """Test the FastAPI by uploading a ZIP file"""
    API_URL = "http://127.0.0.1:8000/validate-zip-claim/"
    
    print(f"\n🔍 Testing API with ZIP file: {zip_file_path}")
    print(f"   API Endpoint: {API_URL}")
    
    if not os.path.exists(zip_file_path):
        print(f"   ❌ Error: ZIP file '{zip_file_path}' not found!")
        return
    
    try:
        # Upload the ZIP file
        with open(zip_file_path, 'rb') as f:
            files = {'file': (os.path.basename(zip_file_path), f, 'application/zip')}
            print(f"\n📤 Uploading ZIP file...")
            response = requests.post(API_URL, files=files)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "="*80)
            print("VALIDATION RESULTS")
            print("="*80)
            print(f"Status: {result['status']}")
            print(f"Total Issues: {result['total_issues']}")
            print(f"Files Checked: {len(result['files_checked'])}")
            
            print("\n" + "-"*80)
            print("FILE-BY-FILE RESULTS:")
            print("-"*80)
            
            for filename, file_data in result['files_checked'].items():
                print(f"\n📄 {filename}")
                print(f"   Status: {file_data['status']}")
                for issue in file_data['issues'][:3]:  # Show first 3 issues
                    print(f"      {issue}")
            
            print("\n" + "="*80)
            print(f"FINAL VERDICT: {result['status']}")
            print("="*80)
            
            # Print summary
            for summary in result['summary']:
                print(f"   {summary}")
            
            return result
        else:
            print(f"\n❌ API Error: {response.status_code}")
            print(f"   {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("   Make sure the FastAPI server is running:")
        print("   python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def test_local_folder_api(folder_path):
    """Test the API with local folder validation"""
    API_URL = f"http://127.0.0.1:8000/validate-local-folder/?folder_path={folder_path}"
    
    print(f"\n🔍 Testing API with local folder: {folder_path}")
    print(f"   API Endpoint: {API_URL}")
    
    try:
        response = requests.get(API_URL)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Status: {result['status']}")
            print(f"   Total Issues: {result['total_issues']}")
            return result
        else:
            print(f"\n❌ API Error: {response.status_code}")
            print(f"   {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("   Make sure the FastAPI server is running:")
        print("   python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("FASTAPI CLAIM VALIDATION - SIMPLE TEST")
    print("#"*80)
    
    # Configuration
    FOLDER_PATH = "claim_folder_001"  # Change this to your folder
    ZIP_FILE = "claim_test.zip"
    
    # Step 1: Create ZIP file
    success = create_zip_from_folder(FOLDER_PATH, ZIP_FILE)
    
    if success:
        # Step 2: Test API with ZIP
        print("\n" + "-"*80)
        print("TEST 1: Upload and Validate ZIP")
        print("-"*80)
        test_api_with_zip(ZIP_FILE)
    
    # Step 3: Test API with local folder (if folder exists on server)
    if os.path.exists(FOLDER_PATH):
        print("\n" + "-"*80)
        print("TEST 2: Validate Local Folder")
        print("-"*80)
        test_local_folder_api(FOLDER_PATH)
    
    print("\n" + "#"*80)
    print("TEST COMPLETED")
    print("#"*80)
    print("\n💡 TIP: You can also test the API at http://127.0.0.1:8000/docs\n")
