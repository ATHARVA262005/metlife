# import os
# import json
# import random
# import datetime
# from faker import Faker

# # Initialize Faker for data generation
# fake = Faker('en_IN')  # Using India locale for more relevant names/data

# # --- Configuration ---
# NUM_FOLDERS = 20
# OUTPUT_DIR = "claim_dataset"

# # --- Data for Realistic Generation ---
# diagnosis_map = {
#     "Acute Appendicitis": ("K35.80", "Laparoscopic Appendectomy", "Patient presented with acute abdominal pain..."),
#     "Pneumonia": ("J18.9", "Antibiotic Therapy", "Patient admitted with high fever, cough, and chest X-ray confirmed pneumonia..."),
#     "Coronary Artery Disease": ("I25.10", "Coronary Angioplasty", "Patient with history of angina, underwent planned angioplasty..."),
#     "Fractured Tibia": ("S82.2", "Surgical Fixation (ORIF)", "Patient sustained trauma, X-ray confirmed displaced tibial fracture..."),
#     "Cataract": ("H25.9", "Phacoemulsification", "Patient with progressive vision loss, scheduled for cataract surgery...")
# }

# hospital_names = [
#     "Apollo Hospital", "Fortis Healthcare", "Max Healthcare Institute", 
#     "Manipal Hospital", "Global City Medical Center", "Sunshine General Hospital"
# ]

# # --- Helper Function to Write JSON ---
# def write_json_file(folder_path, filename, data):
#     """Saves a dictionary as a JSON file."""
#     filepath = os.path.join(folder_path, filename)
#     with open(filepath, 'w') as f:
#         # default=str is used to handle datetime objects
#         json.dump(data, f, indent=2, default=str)

# # --- Core Data Generation ---
# def generate_core_data():
#     """Generates the set of common features for one entire claim."""
    
#     # Patient Details
#     patient_name = fake.name()
#     patient_gender = random.choice(["Male", "Female", "Other"])
#     patient_dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
    
#     # Hospital & Treatment Details
#     admission_date = fake.date_between(start_date='-1y', end_date='today')
#     discharge_date = admission_date + datetime.timedelta(days=random.randint(3, 10))
    
#     # Get consistent diagnosis and procedure
#     diag_name, (diag_code, proc_name, notes) = random.choice(list(diagnosis_map.items()))
    
#     # Financials
#     total_bill = round(random.randint(80000, 500000) / 100) * 100  # Clean, round numbers
    
#     core_data = {
#         "claim_id": f"CL-{random.randint(10000, 99999)}",
#         "policy_id": f"POL-{random.randint(100000, 999999)}",
#         "patient_name": patient_name,
#         "patient_id": f"PID-{random.randint(10000, 99999)}",
#         "patient_dob": patient_dob,
#         "patient_gender": patient_gender,
#         "hospital_name": random.choice(hospital_names),
#         "hospital_id": f"HOSP-{random.randint(100, 999)}",
#         "admission_date": admission_date,
#         "discharge_date": discharge_date,
#         "primary_diagnosis": diag_name,
#         "diagnosis_code": diag_code,
#         "procedure_name": proc_name,
#         "treating_doctor": f"Dr. {fake.name()}",
#         "total_bill_amount": total_bill,
#         "doctor_notes_base": notes,
#         "bank_account_masked": f"XXXXXX{random.randint(1000, 9999)}",
#         "ifsc_code": f"{random.choice(['SBIN', 'HDFC', 'ICIC', 'AXIS'])}0{random.randint(100000, 999999)}",
#         "id_masked": f"XXXX-XXXX-{random.randint(1000, 9999)}"
#     }
#     return core_data

# # --- 10 File Generation Functions ---

# def create_claim_form(data):
#     return {
#         "claim_id": data['claim_id'],
#         "part_a_insured_details": {
#             "policy_id": data['policy_id'],
#             "insured_name": data['patient_name'],
#             "patient_name": data['patient_name'],
#             "patient_dob": data['patient_dob']
#         },
#         "part_b_hospital_details": {
#             "hospital_name": data['hospital_name'],
#             "admission_date": data['admission_date'],
#             "discharge_date": data['discharge_date'],
#             "diagnosis": data['primary_diagnosis'],
#             "procedure_performed": data['procedure_name']
#         }
#     }

# def create_discharge_summary(data):
#     return {
#         "patient_id": data['patient_id'],
#         "patient_name": data['patient_name'],
#         "admission_date": data['admission_date'],
#         "discharge_date": data['discharge_date'],
#         "final_diagnosis": data['primary_diagnosis'],
#         "diagnosis_code": data['diagnosis_code'],
#         "treatment_summary": f"{data['doctor_notes_base']} Successful {data['procedure_name']} performed. Post-operative recovery was uneventful.",
#         "doctor_in_charge": data['treating_doctor']
#     }

# def create_final_bill(data):
#     return {
#         "bill_number": f"HB-{data['admission_date'].year}-{random.randint(1000, 9999)}",
#         "patient_id": data['patient_id'],
#         "patient_name": data['patient_name'],
#         "billing_date": data['discharge_date'],
#         "admission_date": data['admission_date'],
#         "total_amount": data['total_bill_amount']
#     }

# def create_payment_receipts(data):
#     return {
#         "receipt_id": f"PR-{data['discharge_date'].year}-{random.randint(1000, 9999)}",
#         "patient_name": data['patient_name'],
#         "payment_date": data['discharge_date'],
#         "amount_paid": data['total_bill_amount'],
#         "payment_mode": random.choice(["Credit Card", "Bank Transfer", "UPI"])
#     }

# def create_bill_breakup(data):
#     # Ensure the breakup sums exactly to the total
#     total = data['total_bill_amount']
#     room_rent = round(total * 0.15)
#     surgeon_fees = round(total * 0.40)
#     ot_charges = round(total * 0.25)
#     medicines = round(total * 1.0 - room_rent - surgeon_fees - ot_charges) # Remainder
    
#     return {
#         "bill_number": f"HB-{data['admission_date'].year}-{random.randint(1000, 9999)}",
#         "patient_id": data['patient_id'],
#         "line_items": [
#             {"service": "Room Rent", "cost": room_rent},
#             {"service": f"Surgeon Fees ({data['treating_doctor']})", "cost": surgeon_fees},
#             {"service": f"OT Charges ({data['procedure_name']})", "cost": ot_charges},
#             {"service": "Medicines & Consumables", "cost": medicines}
#         ],
#         "total_calculated": room_rent + surgeon_fees + ot_charges + medicines
#     }

# def create_doctor_notes(data):
#     return {
#         "patient_id": data['patient_id'],
#         "consultation_date": data['admission_date'],
#         "doctor_name": data['treating_doctor'],
#         "notes": data['doctor_notes_base'],
#         "prescription": [
#             {"drug": "IV Fluids", "dosage": "STAT"},
#             {"drug": "Antibiotics (Pre-Op)", "dosage": "STAT"},
#             {"drug": "Painkiller (SOS)", "dosage": "SOS"}
#         ]
#     }

# def create_lab_reports(data):
#     return {
#         "report_id": f"LAB-{random.randint(10000, 99999)}",
#         "patient_id": data['patient_id'],
#         "patient_name": data['patient_name'],
#         "test_name": random.choice(["Complete Blood Count (CBC)", "X-Ray Chest", "ECG"]),
#         "test_date": data['admission_date'],
#         "result": "See attached film / values.",
#         "analysis": f"Findings consistent with {data['primary_diagnosis']}."
#     }

# def create_policy_copy(data):
#     return {
#         "policy_id": data['policy_id'],
#         "policy_holder_name": data['patient_name'],
#         "valid_from": data['admission_date'].replace(month=1, day=1).isoformat(),
#         "valid_to": data['admission_date'].replace(month=12, day=31).isoformat(),
#         "status": "Active"
#     }

# def create_patient_id(data):
#     return {
#         "patient_name_on_id": data['patient_name'],
#         "id_type": random.choice(["Aadhaar Card", "PAN Card", "Voter ID"]),
#         "id_number_masked": data['id_masked'],
#         "dob_on_id": data['patient_dob']
#     }

# def create_bank_details(data):
#     return {
#         "account_holder_name": data['patient_name'],
#         "bank_name": random.choice(["State Bank of India", "HDFC Bank", "ICICI Bank"]),
#         "account_number_masked": data['bank_account_masked'],
#         "ifsc_code": data['ifsc_code']
#     }

# # --- Main Script Execution ---
# def main():
#     # Create the main output directory
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     print(f"Generating {NUM_FOLDERS} claim folders in '{OUTPUT_DIR}'...")

#     for i in range(1, NUM_FOLDERS + 1):
#         folder_name = os.path.join(OUTPUT_DIR, f"claim_folder_{i:03d}")
#         os.makedirs(folder_name, exist_ok=True)
        
#         # 1. Generate ONE set of core data for this folder
#         core_data = generate_core_data()

#         # 2. Use this core data to create all 10 files
#         write_json_file(folder_name, "01_ClaimForm.json", create_claim_form(core_data))
#         write_json_file(folder_name, "02_DischargeSummary.json", create_discharge_summary(core_data))
#         write_json_file(folder_name, "03_FinalHospitalBill.json", create_final_bill(core_data))
#         write_json_file(folder_name, "04_PaymentReceipts.json", create_payment_receipts(core_data))
#         write_json_file(folder_name, "05_BillBreakup.json", create_bill_breakup(core_data))
#         write_json_file(folder_name, "06_DoctorNotes.json", create_doctor_notes(core_data))
#         write_json_file(folder_name, "07_LabReports.json", create_lab_reports(core_data))
#         write_json_file(folder_name, "08_PolicyCopy.json", create_policy_copy(core_data))
#         write_json_file(folder_name, "09_PatientID.json", create_patient_id(core_data))
#         write_json_file(folder_name, "10_BankDetails.json", create_bank_details(core_data))

#     print(f"\nSuccessfully generated {NUM_FOLDERS} folders.")
#     print(f"Each folder contains 10 consistent JSON files.")

# if __name__ == "__main__":
#     main()



import os
import json
import random
import datetime
import shutil
from faker import Faker

# Initialize Faker for data generation
fake = Faker('en_IN')

# --- Configuration ---
NUM_FOLDERS = 20
OUTPUT_DIR = "claim_dataset_with_fraud"
# Probability that a folder will be corrupted (e.g., 0.4 = 40% chance)
CORRUPTION_PROBABILITY = 0.4
# Of the corrupted folders, the chance it's a 'mismatch' vs. 'missing file'
MISMATCH_PROBABILITY = 0.7 

# --- Data for Realistic Generation ---
diagnosis_map = {
    "Acute Appendicitis": ("K35.80", "Laparoscopic Appendectomy", "Patient presented with acute abdominal pain..."),
    "Pneumonia": ("J18.9", "Antibiotic Therapy", "Patient admitted with high fever, cough..."),
    "Coronary Artery Disease": ("I25.10", "Coronary Angioplasty", "Patient with history of angina..."),
    "Fractured Tibia": ("S82.2", "Surgical Fixation (ORIF)", "Patient sustained trauma..."),
    "Cataract": ("H25.9", "Phacoemulsification", "Patient with progressive vision loss...")
}

hospital_names = [
    "Apollo Hospital", "Fortis Healthcare", "Max Healthcare Institute", 
    "Manipal Hospital", "Global City Medical Center", "Sunshine General Hospital"
]

# --- Helper Function to Write JSON ---
def write_json_file(folder_path, filename, data):
    """Saves a dictionary as a JSON file."""
    filepath = os.path.join(folder_path, filename)
    with open(filepath, 'w') as f:
        # default=str is used to handle datetime objects
        json.dump(data, f, indent=2, default=str)

# --- Core Data Generation ---
def generate_core_data():
    """Generates the set of common features for one entire claim."""
    
    patient_name = fake.name()
    admission_date = fake.date_between(start_date='-1y', end_date='today')
    discharge_date = admission_date + datetime.timedelta(days=random.randint(3, 10))
    diag_name, (diag_code, proc_name, notes) = random.choice(list(diagnosis_map.items()))
    total_bill = round(random.randint(80000, 500000) / 100) * 100
    
    core_data = {
        "claim_id": f"CL-{random.randint(10000, 99999)}",
        "policy_id": f"POL-{random.randint(100000, 999999)}",
        "patient_name": patient_name,
        "patient_id": f"PID-{random.randint(10000, 99999)}",
        "patient_dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "hospital_name": random.choice(hospital_names),
        "admission_date": admission_date,
        "discharge_date": discharge_date,
        "primary_diagnosis": diag_name,
        "diagnosis_code": diag_code,
        "procedure_name": proc_name,
        "treating_doctor": f"Dr. {fake.name()}",
        "total_bill_amount": total_bill,
        "doctor_notes_base": notes,
        "bank_account_masked": f"XXXXXX{random.randint(1000, 9999)}",
        "ifsc_code": f"{random.choice(['SBIN', 'HDFC', 'ICIC', 'AXIS'])}0{random.randint(100000, 999999)}",
        "id_masked": f"XXXX-XXXX-{random.randint(1000, 9999)}"
    }
    return core_data

# --- 10 File Generation Functions (Identical to previous script) ---

def create_claim_form(data):
    return {
        "claim_id": data['claim_id'],
        "part_a_insured_details": {
            "policy_id": data['policy_id'], "insured_name": data['patient_name'],
            "patient_name": data['patient_name'], "patient_dob": data['patient_dob']
        },
        "part_b_hospital_details": {
            "hospital_name": data['hospital_name'], "admission_date": data['admission_date'],
            "discharge_date": data['discharge_date'], "diagnosis": data['primary_diagnosis'],
            "procedure_performed": data['procedure_name']
        }
    }

def create_discharge_summary(data):
    return {
        "patient_id": data['patient_id'], "patient_name": data['patient_name'],
        "admission_date": data['admission_date'], "discharge_date": data['discharge_date'],
        "final_diagnosis": data['primary_diagnosis'], "diagnosis_code": data['diagnosis_code'],
        "treatment_summary": f"{data['doctor_notes_base']} Successful {data['procedure_name']} performed. Post-operative recovery was uneventful.",
        "doctor_in_charge": data['treating_doctor']
    }

def create_final_bill(data):
    return {
        "bill_number": f"HB-{data['admission_date'].year}-{random.randint(1000, 9999)}",
        "patient_id": data['patient_id'], "patient_name": data['patient_name'],
        "billing_date": data['discharge_date'], "admission_date": data['admission_date'],
        "total_amount": data['total_bill_amount']
    }

def create_payment_receipts(data):
    return {
        "receipt_id": f"PR-{data['discharge_date'].year}-{random.randint(1000, 9999)}",
        "patient_name": data['patient_name'], "payment_date": data['discharge_date'],
        "amount_paid": data['total_bill_amount'],
        "payment_mode": random.choice(["Credit Card", "Bank Transfer", "UPI"])
    }

def create_bill_breakup(data):
    total = data['total_bill_amount']
    room_rent = round(total * 0.15)
    surgeon_fees = round(total * 0.40)
    ot_charges = round(total * 0.25)
    medicines = total - room_rent - surgeon_fees - ot_charges # Remainder
    
    return {
        "bill_number": f"HB-{data['admission_date'].year}-{random.randint(1000, 9999)}",
        "patient_id": data['patient_id'],
        "line_items": [
            {"service": "Room Rent", "cost": room_rent},
            {"service": f"Surgeon Fees ({data['treating_doctor']})", "cost": surgeon_fees},
            {"service": f"OT Charges ({data['procedure_name']})", "cost": ot_charges},
            {"service": "Medicines & Consumables", "cost": medicines}
        ],
        "total_calculated": room_rent + surgeon_fees + ot_charges + medicines
    }

def create_doctor_notes(data):
    return {
        "patient_id": data['patient_id'], "consultation_date": data['admission_date'],
        "doctor_name": data['treating_doctor'], "notes": data['doctor_notes_base'],
        "prescription": [{"drug": "IV Fluids", "dosage": "STAT"}, {"drug": "Painkiller (SOS)", "dosage": "SOS"}]
    }

def create_lab_reports(data):
    return {
        "report_id": f"LAB-{random.randint(10000, 99999)}",
        "patient_id": data['patient_id'], "patient_name": data['patient_name'],
        "test_name": random.choice(["Complete Blood Count (CBC)", "X-Ray Chest", "ECG"]),
        "test_date": data['admission_date'], "result": "See attached film / values.",
        "analysis": f"Findings consistent with {data['primary_diagnosis']}."
    }

def create_policy_copy(data):
    return {
        "policy_id": data['policy_id'], "policy_holder_name": data['patient_name'],
        "valid_from": data['admission_date'].replace(month=1, day=1).isoformat(),
        "valid_to": data['admission_date'].replace(month=12, day=31).isoformat(),
        "status": "Active"
    }

def create_patient_id(data):
    return {
        "patient_name_on_id": data['patient_name'],
        "id_type": random.choice(["Aadhaar Card", "PAN Card", "Voter ID"]),
        "id_number_masked": data['id_masked'], "dob_on_id": data['patient_dob']
    }

def create_bank_details(data):
    return {
        "account_holder_name": data['patient_name'],
        "bank_name": random.choice(["State Bank of India", "HDFC Bank", "ICICI Bank"]),
        "account_number_masked": data['bank_account_masked'], "ifsc_code": data['ifsc_code']
    }

# --- Main Script Execution ---
def main():
    # Clean up old directory if it exists
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Generating {NUM_FOLDERS} claim folders in '{OUTPUT_DIR}'...")
    print(f"Applying {CORRUPTION_PROBABILITY*100}% corruption rate.\n")

    file_names = [
        "01_ClaimForm.json", "02_DischargeSummary.json", "03_FinalHospitalBill.json",
        "04_PaymentReceipts.json", "05_BillBreakup.json", "06_DoctorNotes.json",
        "07_LabReports.json", "08_PolicyCopy.json", "09_PatientID.json", "10_BankDetails.json"
    ]

    for i in range(1, NUM_FOLDERS + 1):
        folder_name = f"claim_folder_{i:03d}"
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        print(f"Creating {folder_name}...")
        
        # 1. Generate ONE set of core data for this folder
        core_data = generate_core_data()

        # 2. Use this core data to create all 10 *perfect* files first
        write_json_file(folder_path, "01_ClaimForm.json", create_claim_form(core_data))
        write_json_file(folder_path, "02_DischargeSummary.json", create_discharge_summary(core_data))
        write_json_file(folder_path, "03_FinalHospitalBill.json", create_final_bill(core_data))
        write_json_file(folder_path, "04_PaymentReceipts.json", create_payment_receipts(core_data))
        write_json_file(folder_path, "05_BillBreakup.json", create_bill_breakup(core_data))
        write_json_file(folder_path, "06_DoctorNotes.json", create_doctor_notes(core_data))
        write_json_file(folder_path, "07_LabReports.json", create_lab_reports(core_data))
        write_json_file(folder_path, "08_PolicyCopy.json", create_policy_copy(core_data))
        write_json_file(folder_path, "09_PatientID.json", create_patient_id(core_data))
        write_json_file(folder_path, "10_BankDetails.json", create_bank_details(core_data))

        # 3. --- NEW: Corruption Step ---
        if random.random() < CORRUPTION_PROBABILITY:
            # This folder will be corrupted
            
            if random.random() < MISMATCH_PROBABILITY:
                # --- Type 1: Data Mismatch Fraud ---
                corruption_type = random.choice(['amount', 'name', 'date'])
                
                if corruption_type == 'amount':
                    # Mismatch: Final Bill vs. Payment Receipt
                    print("   -> CORRUPTION (Mismatch): Inflating Final Bill amount...")
                    filepath = os.path.join(folder_path, '03_FinalHospitalBill.json')
                    with open(filepath, 'r') as f: doc = json.load(f)
                    # Add a fraudulent amount
                    doc['total_amount'] += random.randint(10000, 50000)
                    with open(filepath, 'w') as f: json.dump(doc, f, indent=2)

                elif corruption_type == 'name':
                    # Mismatch: Patient ID vs. Claim Form
                    print("   -> CORRUPTION (Mismatch): Changing name on Patient ID...")
                    filepath = os.path.join(folder_path, '09_PatientID.json')
                    with open(filepath, 'r') as f: doc = json.load(f)
                    doc['patient_name_on_id'] = fake.name() # A completely different name
                    with open(filepath, 'w') as f: json.dump(doc, f, indent=2)

                elif corruption_type == 'date':
                    # Mismatch: Discharge Summary vs. Final Bill (billing for extra days)
                    print("   -> CORRUPTION (Mismatch): Changing Discharge Date on summary...")
                    filepath = os.path.join(folder_path, '02_DischargeSummary.json')
                    with open(filepath, 'r') as f: doc = json.load(f)
                    # Add 2 days to the discharge date string
                    original_date = datetime.date.fromisoformat(doc['discharge_date'])
                    new_date = original_date + datetime.timedelta(days=2)
                    doc['discharge_date'] = new_date.isoformat()
                    with open(filepath, 'w') as f: json.dump(doc, f, indent=2)

            else:
                # --- Type 2: Missing File Fraud ---
                file_to_delete = random.choice([
                    "04_PaymentReceipts.json", "05_BillBreakup.json", "07_LabReports.json"
                ])
                print(f"   -> CORRUPTION (Missing File): Deleting {file_to_delete}...")
                os.remove(os.path.join(folder_path, file_to_delete))
        
        else:
            print("   -> (Clean): All 10 files are present and consistent.")

    print(f"\nSuccessfully generated {NUM_FOLDERS} folders in '{OUTPUT_DIR}'.")
    print("Dataset now contains a mix of clean and corrupted data for testing.")

if __name__ == "__main__":
    main()