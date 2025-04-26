
markdown
Copy
Edit
# 🛍️ AutoDressOrder – Automated Email Order Processor

AutoDressOrder is a Python-based automation tool designed to streamline the dress shop's order management system. It automatically processes incoming emails, extracts order data from attached PDFs, generates Customer Reference Numbers (CRNs), stores data in MongoDB, and replies to the sender with processed documents.

---

## 📦 Features

- ✅ Automatically responds to the first email from the sender: `vetrivelmaniv2m@gmail.com`
- 📧 Extracts Subject, Body, and attached PDF from email
- 🔍 Parses the PDF (text, images, tables)
- 📊 Saves extracted tables as:
  - `Communication Dimensions.xlsx`
  - `Specifications Table.xlsx` (with `Cost` and `Total` rows appended)
- 🧾 Generates a new PDF with:
  - Updated Specification Table
  - Order details and visuals
- 📬 Sends a confirmation email with:
  - Processed PDF
  - Excel sheets
- 🗂️ Stores all order data in **MongoDB** with a unique **CRN**

---

## 🛠️ Tech Stack

- **Python**
- **IMAP/SMTP** – For email automation
- **PyMuPDF / pdfplumber** – PDF parsing
- **OpenPyXL / Pandas** – Excel handling
- **ReportLab / FPDF** – PDF generation
- **MongoDB (pymongo)** – Database
- **Faker / UUID** – CRN generation

---

## 🚀 Setup Instructions

1. **Clone the repository**
   bash
   git clone https://github.com/VetrivelmaniT/DressFlow-Solutions
   cd AutoDressOrder
Install dependencies

pip install -r requirements.txt
