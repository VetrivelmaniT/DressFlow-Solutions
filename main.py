from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mongo_storage import MongoDBManager
import os
import smtplib
import time
import logging
from email_handler import EmailHandler
from pdf_processor import PDFProcessor
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_document(email_data, email_handler):
    """
    Processes a single document from the email data.
    """
    try:
        crn = email_handler.generate_crn()
        logger.info(f"Processing started for CRN: {crn}")

        processor = PDFProcessor(crn)

        # Save PDF
        pdf_path = processor.save_pdf(email_data['pdf_data'], email_data['pdf_name'])
        logger.info(f"PDF saved successfully: {pdf_path}")

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(processor.extract_images, pdf_path): "images",
                executor.submit(processor.convert_pdf_to_excel, pdf_path): "excel"
            }

            results = {}
            for future in as_completed(futures):
                task = futures[future]
                try:
                    results[task] = future.result()
                    logger.info(f"{task.capitalize()} processing completed.")
                except Exception as e:
                    logger.error(f"Error in {task} processing: {str(e)}")
                    results[task] = None

        excel_path = results.get("excel")
        if excel_path:
            email_handler.send_email(email_data['from'], crn, pdf_path)
            logger.info(f"Confirmation email sent for CRN: {crn}")
            time.sleep(30)
            email_handler.send_email(email_data['from'], f"Processed Excel File - CRN: {crn}", excel_path)
            logger.info(f"Excel file sent for CRN: {crn}")

    except Exception as e:
        logger.error(f"Error during document processing: {str(e)}")
        raise

def send_email(self, to_address, subject, body, attachment_path=None):
            try:
                with smtplib.SMTP(self.smtp_server, self.port) as server:
                    server.starttls()  # Upgrade the connection to secure
                    server.login(self.email, self.password)
                    
                    # Create the email
                    msg = MIMEMultipart()
                    msg['From'] = self.email
                    msg['To'] = to_address
                    msg['Subject'] = subject
                    
                    # Attach the email body
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # Attach a file if specified
                    if attachment_path:
                        with open(attachment_path, 'rb') as f:
                            from email.mime.base import MIMEBase
                            from email import encoders
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(attachment_path)}',
                            )
                            msg.attach(part)
                    
                    # Send the email
                    server.sendmail(self.email, to_address, msg.as_string())
                    logger.info(f"Email sent to {to_address} with subject '{subject}'")
            except Exception as e:
                logger.error(f"Failed to send email: {str(e)}")
                raise
def main():
    email = "vetrivelmaniv2m@gmail.com"
    password = "jsxh jaiq psnb mzhb"
    mongo_uri = "mongodb://localhost:27017/?directConnection=true"  # Replace with your MongoDB URI if needed
    db_name = "email_processing_db"
    collection_name = "email_data"

    email_handler = EmailHandler(email, password, mongo_uri, db_name, collection_name)
    logger.info("Email handler initialized successfully.")

    while True:
        try:
            email_data = email_handler.read_emails()
            if email_data:
                logger.info("New email data received. Starting processing.")
                process_document(email_data, email_handler)
            else:
                logger.info("No new emails. Retrying after a delay.")

            time.sleep(30)
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            time.sleep(60)


if __name__ == "__main__":
    main()