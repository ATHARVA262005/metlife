# Claim Comparison Tool - User Guide

## Overview
`compatre.py` is a tool that compares all 10 files in a claim folder against the `01_ClaimForm.json` (Source of Truth) and provides a detailed report.

## Usage

### Basic Usage
```bash
python compatre.py <folder_path>
```

### Examples
```bash
# Compare files in claim_folder_001
python compatre.py claim_folder_001

# Compare files in a different location
python compatre.py claim_dataset_with_fraud/claim_folder_001

# If no folder path is provided, it defaults to claim_folder_001
python compatre.py
```

## What It Checks

The tool compares **all 10 files** in the folder:

### 1. **01_ClaimForm.json** 
- Marked as SOURCE OF TRUTH
- Not compared (it's the reference)

### 2. **02_DischargeSummary.json**
- ✅ Patient Name
- ✅ Admission Date
- ✅ Discharge Date
- ✅ Diagnosis

### 3. **03_FinalHospitalBill.json**
- ✅ Patient Name
- ✅ Admission Date
- ✅ Total Amount

### 4. **04_PaymentReceipts.json**
- ✅ Patient Name
- ✅ Amount Paid (must match Final Bill)

### 5. **05_BillBreakup.json**
- ✅ Calculated Total (must match Final Bill)

### 6. **06_DoctorNotes.json**
- ✅ File existence and validity

### 7. **07_LabReports.json**
- ✅ Patient Name

### 8. **08_PolicyCopy.json**
- ✅ Policy ID
- ✅ Policy Holder Name

### 9. **09_PatientID.json**
- ✅ Patient Name on ID
- ✅ Date of Birth

### 10. **10_BankDetails.json**
- ✅ Account Holder Name

## Report Format

The tool generates a detailed report showing:

```
================================================================================
CLAIM VALIDATION REPORT
================================================================================
Folder: claim_folder_001
Status: CLEAN / FRAUD DETECTED
================================================================================

📄 01_ClaimForm.json
   Status: ✅ SOURCE OF TRUTH

📄 02_DischargeSummary.json
   Status: ✅ MATCH
      ✅ All fields match Claim Form

📄 04_PaymentReceipts.json
   Status: ❌ ISSUES FOUND
      ❌ Amount Paid: Expected ₹500000, Found ₹450000 (Diff: ₹50000)

...

================================================================================
FINAL VERDICT: CLEAN / FRAUD DETECTED
Total Issues Found: X
================================================================================
```

## Status Indicators

- ✅ **MATCH** - All fields in the file match the Claim Form
- ❌ **ISSUES FOUND** - One or more mismatches detected
- ✅ **SOURCE OF TRUTH** - The reference file (ClaimForm)

## Fraud Types Detected

### 1. **Amount Fraud**
- Final bill amount doesn't match payment receipts
- Bill breakup doesn't total to final bill amount
- Example: Bill shows ₹500,000 but receipt shows ₹450,000

### 2. **Identity Fraud**
- Patient name on ID doesn't match claim form
- Date of birth mismatch
- Account holder name doesn't match

### 3. **Date Manipulation**
- Discharge date changed to bill for extra days
- Admission date inconsistencies

### 4. **Missing Files**
- Required documents not present
- Common: Payment receipts, Lab reports, Bill breakup

## Output

### Clean Folder
```
FINAL VERDICT: CLEAN
   All files are consistent with Claim Form
```

### Fraudulent Folder
```
FINAL VERDICT: FRAUD DETECTED
Total Issues Found: 2
   Found 2 issue(s) across 2 file(s)
```

## Requirements

- Python 3.x
- No external packages required (uses only standard library)

## Tips

1. **Always provide full or relative path** to the folder
2. **Folder must contain all 10 JSON files** (or at least the ClaimForm)
3. **Check the detailed report** to see which files have issues
4. **Amount differences** are shown in rupees (₹)

## Folder Structure Expected

```
claim_folder_001/
├── 01_ClaimForm.json
├── 02_DischargeSummary.json
├── 03_FinalHospitalBill.json
├── 04_PaymentReceipts.json
├── 05_BillBreakup.json
├── 06_DoctorNotes.json
├── 07_LabReports.json
├── 08_PolicyCopy.json
├── 09_PatientID.json
└── 10_BankDetails.json
```

## Common Errors

### Error: Folder does not exist
```
❌ Error: Folder 'xyz' does not exist.
```
**Solution**: Check the folder path and ensure it exists

### Error: ClaimForm missing
```
CRITICAL: 01_ClaimForm.json is missing. Cannot validate.
```
**Solution**: Ensure the folder contains `01_ClaimForm.json`

### Error: ClaimForm corrupt
```
CRITICAL: 01_ClaimForm.json is corrupt - Invalid JSON format
```
**Solution**: Check if the JSON file is valid

---

**Happy Validating! 🔍**
