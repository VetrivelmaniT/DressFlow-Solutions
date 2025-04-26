from datetime import datetime
import os
import fitz  # PyMuPDF
from pdf2docx import Converter
import pandas as pd
import logging
from PIL import Image
import pdfplumber
from mongo_storage import MongoDBManager
from typing import List, Optional, Dict


class PDFProcessor:
    def __init__(self, crn: str):
        self.crn = crn
        self.folder_path = f"{crn}_download"
        os.makedirs(self.folder_path, exist_ok=True)
        os.makedirs(os.path.join(self.folder_path, 'images'), exist_ok=True)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.mongo_manager = MongoDBManager("pdf_processing_db", "pdf_data")

    def save_pdf(self, pdf_data: bytes, pdf_name: str) -> str:
        # Save PDF data to the local directory and log metadata to MongoDB.
        
        pdf_path = os.path.join(self.folder_path, pdf_name)
        try:
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)
            self.logger.info(f"PDF saved at: {pdf_path}")

            # Save metadata to MongoDB
            self.mongo_manager.insert_data({
                "crn": self.crn,
                "pdf_name": pdf_name,
                "pdf_path": pdf_path
            })
            return pdf_path
        except Exception as e:
            self.logger.error(f"Error saving PDF: {e}")
            raise

    def extract_images(self, pdf_path: str) -> List[str]:
        
        # Extract all images from the given PDF and save them locally.
        
        images_folder = os.path.join(self.folder_path, 'images')
        try:
            doc = fitz.open(pdf_path)
            extracted_images = []
            for page_num, page in enumerate(doc):
                for img_index, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image['ext']

                    image_filename = f"image_p{page_num + 1}_{img_index + 1}.{image_ext}"
                    image_path = os.path.join(images_folder, image_filename)

                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_bytes)
                    extracted_images.append(image_path)

            self.logger.info(f"Extracted {len(extracted_images)} images to {images_folder}")

            # Save metadata to MongoDB
            self.mongo_manager.insert_data({
            "crn": self.crn,
            "file_type": "image",
            "images": extracted_images,
            "created_at": datetime.now().isoformat()
        })

            return extracted_images
        except Exception as e:
            self.logger.error(f"Error extracting images from PDF: {e}")
            raise

    def convert_pdf_to_excel(self, pdf_path: str) -> str:
        # Extract tables from the given PDF and save them as an Excel file.
        
        excel_path = os.path.join(self.folder_path, os.path.basename(pdf_path).replace('.pdf', '_tables.xlsx'))
        try:
            tables_found = False

            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                with pdfplumber.open(pdf_path) as pdf:
                    for idx, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        for table_idx, table in enumerate(tables):
                            if table:
                                tables_found = True
                                df = pd.DataFrame(table[1:], columns=table[0])
                                df = df.replace('', pd.NA).dropna(how='all')
                                df.columns = df.columns.str.strip()

                                sheet_name = f"Page{idx + 1}_Table{table_idx + 1}"
                                df.to_excel(writer, sheet_name=sheet_name, index=False)
                                self.logger.info(f"Extracted table to sheet: {sheet_name}")

                if not tables_found:
                    self.logger.warning("No tables found in the PDF. Adding a placeholder sheet.")
                    pd.DataFrame({"Message": ["No tables were found in this PDF."]}).to_excel(
                        writer, sheet_name="NoTablesFound", index=False
                    )

            self.logger.info(f"Excel file created at: {excel_path}")

            # Save metadata to MongoDB
            self.mongo_manager.insert_data({
            "crn": self.crn,
            "file_type": "excel",
            "excel_path": excel_path,
            "created_at": datetime.now().isoformat()
        })

            return excel_path
        except Exception as e:
            self.logger.error(f"Error converting PDF to Excel: {e}")
            raise