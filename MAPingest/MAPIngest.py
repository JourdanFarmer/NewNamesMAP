import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import os


# Function to perform OCR on a PDF page
def perform_ocr_on_pdf(pdf_path):
    images = convert_from_path(pdf_path)  # Convert each page to image
    text = ""

    for image in images:
        text += pytesseract.image_to_string(image)  # Perform OCR on each image

    return text


# Function to extract the third line of text
def extract_third_line(text):
    lines = text.splitlines()
    if len(lines) >= 3:
        return lines[2].strip()  # Return the third line (index 2)
    return None


# Function to save the PDF with a new name in the specified directory
def save_pdf_with_new_name(pdf_path, new_name, save_directory):
    # Construct the full path for the new PDF
    new_pdf_path = os.path.join(save_directory, f"{new_name}.pdf")

    # Open the original PDF
    pdf = fitz.open(pdf_path)
    # Save it with the new name
    pdf.save(new_pdf_path)
    pdf.close()
    return new_pdf_path


# Function to process a single PDF
def process_pdf(pdf_path, save_directory, season, year):
    # Perform OCR and get the text
    text = perform_ocr_on_pdf(pdf_path)

    # Extract the third line
    third_line = extract_third_line(text)

    if third_line:
        # Create the new file name based on the third line and additional info
        new_pdf_name = third_line.replace(" ", "_")  # Replace spaces with underscores
        new_pdf_name = f"{new_pdf_name}_{season}_{year}"  # Append season and year
        # Save the PDF with the new name in the specified directory
        new_pdf_path = save_pdf_with_new_name(pdf_path, new_pdf_name, save_directory)
        print(f"New PDF saved as: {new_pdf_path}")
    else:
        print(f"Third line could not be extracted for: {pdf_path}")


# Function to process all PDFs in a folder
def process_pdfs_in_folder(input_folder, save_directory, season, year):
    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # Iterate through all files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            process_pdf(pdf_path, save_directory, season, year)


# Request user input for the folder containing PDFs, save directory, season, and year
input_folder = input("Please enter the folder containing the PDF files: ")
save_directory = input("Please enter the directory where you want to save the new files: ")
season = input("Please enter the season (e.g., Fall, Spring): ")
year = input("Please enter the year (e.g., 2024): ")

# Process all PDFs in the specified folder
process_pdfs_in_folder(input_folder, save_directory, season, year)
