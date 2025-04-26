# 🛍️ AutoDressOrder – Automated Email Order Processor

**AutoDressOrder** is a Python-based automation tool developed to streamline the dress shop's order processing. It automatically handles incoming order emails, extracts content from attached PDFs, generates a unique Customer Reference Number (CRN), stores data in MongoDB, and responds to the sender with processed documents.

---

## 📦 Features

- ✅ Automatically responds to the **first email** from: `vetrivelmaniv2m@gmail.com`
- 📧 Extracts **email subject, body**, and **attached PDF**
- 🔍 Parses PDFs for:
  - Text
  - Images
  - Tables
- 📊 Splits tables into:
  - `Communication Dimensions.xlsx`
  - `Specifications Table.xlsx` (with `Cost` and `Total` rows added)
- 🧾 Generates a new PDF containing:
  - Updated specifications
  - Order summary and visuals
- 📬 Sends a confirmation email including:
  - New PDF
  - Excel files
- 🗂️ All data stored in **MongoDB**, organized by unique **CRN**

---

## 🛠️ Tech Stack

- **Python**
- **IMAP / SMTP** – Email automation
- **PyMuPDF / pdfplumber** – PDF reading
- **Pandas / OpenPyXL** – Excel generation
- **ReportLab / FPDF** – PDF creation
- **MongoDB** with `pymongo`
- **Faker / UUID** – CRN generation

---

## 🚀 Setup Instructions

### 1. Clone the Repository

bash
git clone https://github.com/VetrivelmaniT/DressFlow-Solutions.git
cd AutoDressOrder
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
📁 Folder Structure
arduino
Copy
Edit
AutoDressOrder/
├── email_handler.py
├── pdf_parser.py
├── excel_generator.py
├── pdf_generator.py
├── database.py
├── config.py
├── requirements.txt
└── README.md
✅ Output Example
After running the system:

✅ Extracted Excel files: Communication Dimensions.xlsx, Specifications Table.xlsx

✅ Generated PDF with watermark and order summary

✅ MongoDB entry: { CRN: <unique>, ...order_data }

✅ Confirmation email sent with attachments

📧 Contact Created by Vetrivel Mani T Email: tvetrivelmani@gmail.com Portfolio: https://vetrivel-mani-t-portfolio-com.vercel.app/
