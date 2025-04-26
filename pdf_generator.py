import os
from timeit import main
from email_handler import EmailHandler
from pdf_processor import PDFProcessor
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_pdf_and_send(email_data, email_handler):
    try:
        crn = email_handler.generate_crn()
        logger.info(f"Generating PDF for CRN: {crn}")

        processor = PDFProcessor(crn)

        # Save the original PDF
        pdf_path = processor.save_pdf(email_data['pdf_data'], email_data['pdf_name'])
        logger.info(f"Original PDF saved: {pdf_path}")

        # Extract specific lines (3rd to 8th)
        pdf_text_lines = email_data['pdf_text'].splitlines()
        extracted_lines = pdf_text_lines[2:8]  # 3rd to 8th lines

        # Assume the first image is the one we want to use
        image_path = os.path.join(processor.folder_path, 'images', 'image_p1_1.png')  # Adjust as necessary

        # Create summary PDF
        summary_pdf_path = processor.create_summary_pdf(extracted_lines, image_path, f"summary_{crn}.pdf")

        # Send the summary PDF to the sender
        email_handler.send_email(email_data['from'], crn, summary_pdf_path)
        logger.info(f"Summary PDF sent to {email_data['from']} for CRN: {crn}")

    except Exception as e:
        logger.error(f"Error generating PDF and sending: {e}")
        raise

if __name__ == "__main__":
    main()
    