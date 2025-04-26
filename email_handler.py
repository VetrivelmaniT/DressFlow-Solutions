
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import fitz  # PyMuPDF
from imap_tools import MailBox, AND
import random
import string
import logging
from pymongo import MongoClient
from datetime import datetime

class EmailHandler:
    def __init__(self, email, password, mongo_uri, db_name, collection_name):
        self.email = email
        self.password = password
        self.imap_server = "imap.gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_crn(self):
        # Generates a unique CRN.
        timestamp = ''.join(random.choices(string.digits, k=4))
        letters = ''.join(random.choices(string.ascii_uppercase, k=4))
        return f"{letters}{timestamp}"

    def extract_pdf_text(self, pdf_data):
        # Extracts text from a PDF file.
        try:
            with fitz.open(stream=pdf_data, filetype="pdf") as pdf:
                text_content = ""
                for page in pdf:
                    text_content += page.get_text()
                return text_content
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            return None

    def read_emails(self):
        try:
            with MailBox(self.imap_server).login(self.email, self.password) as mailbox:
                messages = list(mailbox.fetch(AND(seen=False)))
                for msg in messages:
                    for att in msg.attachments:
                        if att.filename.endswith('.pdf'):
                            self.logger.info(f"Found PDF: {att.filename}")

                            # Extract PDF text
                            pdf_text = self.extract_pdf_text(att.payload)
                            if pdf_text:
                                email_data = {
                                    'from': msg.from_,
                                    'subject': msg.subject,
                                    'body': msg.text,
                                    'pdf_name': att.filename,
                                    'pdf_text': pdf_text,
                                    'received_at': datetime.now()
                                }

                                # Log the data before saving
                                self.logger.info(f"Attempting to save to MongoDB: {email_data}")

                                # Save to MongoDB
                                try:
                                    self.collection.insert_one(email_data)
                                    self.logger.info(f"Email details saved to MongoDB successfully.")
                                except Exception as e:
                                    self.logger.error(f"MongoDB insert error: {str(e)}")

                                return {
                                    'from': msg.from_,
                                    'subject': msg.subject,
                                    'body': msg.text,
                                    'pdf_data': att.payload,
                                    'pdf_name': att.filename,
                                    'pdf_text': pdf_text  # Include extracted text
                                }
        except Exception as e:
            self.logger.error(f"Email reading error: {str(e)}")
            raise
        
        
    def send_email(self, to_email, crn, attachment_path):
        # Sends an email with an attachment.
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = f"THANK YOU FOR YOUR ORDER: {crn}"
            msg.attach(MIMEText("Please wait a few minutes for processing.", 'plain'))
            
            with open(attachment_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header('Content-Disposition', 'attachment', 
                                   filename=os.path.basename(attachment_path))
                msg.attach(attachment)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
                self.logger.info(f"Email sent successfully to {to_email}")
        except Exception as e:
            self.logger.error(f"Email sending error: {str(e)}")
            raise