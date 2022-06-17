"""

    Created by me (CodeShady)
    GitHub: https://github.com/CodeShady/PaperROM

      ___         ___           ___         ___           ___           ___           ___           ___     
     /  /\       /  /\         /  /\       /  /\         /  /\         /  /\         /  /\         /__/\    
    /  /::\     /  /::\       /  /::\     /  /:/_       /  /::\       /  /::\       /  /::\       |  |::\   
   /  /:/\:\   /  /:/\:\     /  /:/\:\   /  /:/ /\     /  /:/\:\     /  /:/\:\     /  /:/\:\      |  |:|:\  
  /  /:/~/:/  /  /:/~/::\   /  /:/~/:/  /  /:/ /:/_   /  /:/~/:/    /  /:/~/:/    /  /:/  \:\   __|__|:|\:\ 
 /__/:/ /:/  /__/:/ /:/\:\ /__/:/ /:/  /__/:/ /:/ /\ /__/:/ /:/___ /__/:/ /:/___ /__/:/ \__\:\ /__/::::| \:\
 \  \:\/:/   \  \:\/:/__\/ \  \:\/:/   \  \:\/:/ /:/ \  \:\/:::::/ \  \:\/:::::/ \  \:\ /  /:/ \  \:\~~\__\/
  \  \::/     \  \::/       \  \::/     \  \::/ /:/   \  \::/~~~~   \  \::/~~~~   \  \:\  /:/   \  \:\      
   \  \:\      \  \:\        \  \:\      \  \:\/:/     \  \:\        \  \:\        \  \:\/:/     \  \:\     
    \  \:\      \  \:\        \  \:\      \  \::/       \  \:\        \  \:\        \  \::/       \  \:\    
     \__\/       \__\/         \__\/       \__\/         \__\/         \__\/         \__\/         \__\/    
    
    This script puts multiple qr code .png files onto a printable pdf.

    >>-- Links Used -->>
    Generate QR Codes - https://betterprogramming.pub/how-to-generate-and-decode-qr-codes-in-python-a933bce56fd0
    Create PDF Files - https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html

"""

from fpdf import FPDF
from natsort import natsorted
from pdfpresets import QRCodePresetClass
import os
import math

QRCodePreset = None
OG_FILENAME = None
qr_code_directory = None
custom_description = ""


class PDF(FPDF):
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-14)
        # Arial italic 8
        self.set_font('Arial', '', 14)
        # Text color in gray
        self.set_text_color(100)
        # Page number
        self.cell(0, 2, str(OG_FILENAME), 0, 0, 'C')

        self.ln(3)

        # Print page number
        self.set_text_color(128)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 0, str(self.page_no()) + " of " + str(self.alias_nb_pages()), 0, 0, 'L')
        self.ln(1)
        
        # Text color in gray
        self.ln(2)
        self.set_text_color(128)
        self.set_font('Arial', 'I', 7)
        self.cell(0, 0, "github.com/CodeShady/PaperROM", 0, 0, 'C')

def generate_pdf():
    global OG_FILENAME,qr_code_directory

    # Get additional information about document
    OG_FILENAME = input(" Enter PDF Title (My Documents): ")
    qr_code_directory = input(" Where are your QR codes located? (Default: ./): ")
    printable_file_location = input(" What should I name the PDF file? ")

    if printable_file_location == "":
        printable_file_location = "Printable-File.pdf"

    if qr_code_directory == "":
        qr_code_directory = "./"

    # Generate PDF!
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Helvetica', '', 10)

    # Add the little QR code that contains information about the data on the page for the decode program to read later.
    pdf.image(qr_code_directory + "qr-codes-info.png", 188, 275.8, 20)

    # The Y position to place each QR code.
    current_y_pos = 2

    # Sizing & layout variables
    QR_CODES_PER_ROW  = QRCodePreset.get_preset()["qr_codes_per_row"]  # Number of QR codes allowed on one row
    QR_CODES_PER_PAGE = QRCodePreset.get_preset()["qr_codes_per_page"] # Number of QR codes allowed on one page
    qr_code_size = QRCodePreset.get_preset()["qr_codes_size"] # Size of QR codes
    
    # Counter variables
    qr_codes_on_row = 0             # Keep track of how many QR codes are on a single row so we can create a new row when needed.
    number_of_qrcodes_placed = 0    # Keep track of how many QR Codes were placed already so we know when to make a new page.
    page_number_counter = 1

    # Area where QR codes are allowed to be placed (the y area isn't needed)
    qr_placement_area_x = 206.0
    # qr_placement_area_y = 288.0

    # Uncomment this code to display where the QR codes are allowed to be placed.
    # pdf.set_fill_color(255, 255, 255) # color for inner rectangle
    # pdf.rect(4.0, 4.0, qr_placement_area_x, qr_placement_area_y, 'FD')

    # Get a list of all QR codes in the directory
    qr_codes_in_directory = natsorted(os.listdir(qr_code_directory))

    # Get images in directory
    for qr_png in qr_codes_in_directory:
        if qr_png.endswith(".png") and not qr_png == "qr-codes-info.png":
            qr_png = qr_code_directory + qr_png
            # Increment Counters
            number_of_qrcodes_placed += 1

            # Add QR code to PDF
            qr_position = ((qr_placement_area_x / (QR_CODES_PER_ROW)) * qr_codes_on_row) + 2
            # Uncomment this line for even spacing! -> qr_position = ((qr_placement_area_x * qr_codes_on_row) / (QR_CODES_PER_ROW+1)) - (qr_code_size/2) + 4
            
            pdf.image(qr_png, qr_position, current_y_pos, qr_code_size)

            # Increment the amount of qr codes on the page
            qr_codes_on_row += 1

            # Check if we've reached the max limit of QR codes for this page
            if number_of_qrcodes_placed >= QR_CODES_PER_PAGE:
                # Add data/info QR code to footer of page
                pdf.image(qr_code_directory + "qr-codes-info.png", 188, 275.8, 20)
                # Add another page to PDF
                pdf.add_page()

                # Reset counters
                number_of_qrcodes_placed = 0
                qr_codes_on_row = 0
                current_y_pos = 2

                # Add a page to the page number counter
                page_number_counter += 1

            # Check if the amount of QR codes has exceeded the amount of QR codes per row.
            if qr_codes_on_row >= QR_CODES_PER_ROW:
                # Increment Y position
                current_y_pos += qr_code_size

                # Reset counter
                qr_codes_on_row = 0

    # Add data/info QR code to footer of page (make sure none were forgotten!)
    pdf.image(qr_code_directory + "qr-codes-info.png", 188, 275.8, 20)

    # Save the PDF
    pdf.output(printable_file_location, 'F')


# Main
if __name__ == "__main__":
    # Print welcome message
    print("""
      ___         ___           ___         ___           ___           ___           ___           ___     
     /  /\       /  /\         /  /\       /  /\         /  /\         /  /\         /  /\         /__/\    
    /  /::\     /  /::\       /  /::\     /  /:/_       /  /::\       /  /::\       /  /::\       |  |::\   
   /  /:/\:\   /  /:/\:\     /  /:/\:\   /  /:/ /\     /  /:/\:\     /  /:/\:\     /  /:/\:\      |  |:|:\  
  /  /:/~/:/  /  /:/~/::\   /  /:/~/:/  /  /:/ /:/_   /  /:/~/:/    /  /:/~/:/    /  /:/  \:\   __|__|:|\:\ 
 /__/:/ /:/  /__/:/ /:/\:\ /__/:/ /:/  /__/:/ /:/ /\ /__/:/ /:/___ /__/:/ /:/___ /__/:/ \__\:\ /__/::::| \:\\
 \  \:\/:/   \  \:\/:/__\/ \  \:\/:/   \  \:\/:/ /:/ \  \:\/:::::/ \  \:\/:::::/ \  \:\ /  /:/ \  \:\~~\__\/
  \  \::/     \  \::/       \  \::/     \  \::/ /:/   \  \::/~~~~   \  \::/~~~~   \  \:\  /:/   \  \:\      
   \  \:\      \  \:\        \  \:\      \  \:\/:/     \  \:\        \  \:\        \  \:\/:/     \  \:\     
    \  \:\      \  \:\        \  \:\      \  \::/       \  \:\        \  \:\        \  \::/       \  \:\    
     \__\/       \__\/         \__\/       \__\/         \__\/         \__\/         \__\/         \__\/    

 Welcome to "qr2pdf.py"!

 You can use this script to generate a fancy lookin' PDF which would be fully printable!
 Or, you can use your individual QR codes and print them out however you want. :)

 This is the qr2pdf.py script. This isn't for encoding or decoding files!

 For the documentation, visit the GitHub repo: https://github.com/CodeShady/PaperROM
""")

    # Ask user to select preset mode
    QRCodePreset = QRCodePresetClass()
    
    # Create PDF!
    generate_pdf()
