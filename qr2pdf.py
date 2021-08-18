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
import os
from natsort import natsorted

OG_FILENAME = None
qr_code_directory = None


class PDF(FPDF):
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', '', 14)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 2, str(OG_FILENAME), 0, 0, 'C')
        self.ln(8)
        self.set_font('Arial', 'I', 10)
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

    current_x_pos = 2
    current_y_pos = 2#12
    qr_size = 68.5

    row_counter = 0

    qr_index = 0

    # Get images in directory
    for qr_png in natsorted(os.listdir(qr_code_directory)):
        if qr_png.endswith(".png") and not qr_png == "qr-codes-info.png":
            qr_png = qr_code_directory + qr_png
            # Increment Counters
            row_counter += 1
            qr_index += 1

            # Add QR code to PDF
            pdf.image(qr_png, current_x_pos, current_y_pos, qr_size)
            
            # Change position for next QR code
            current_x_pos += qr_size

            # Check if we've reached the max limit of QR codes for this page
            if qr_index >= 12:
                # Add data/info QR code to footer of page
                pdf.image(qr_code_directory + "qr-codes-info.png", 188, 275.8, 20)
                # Add another page to PDF
                pdf.add_page()

                # Reset counters
                qr_index = 0
                current_x_pos = 2
                current_y_pos = -66

            # SPLIT ROW!!
            if row_counter >= 3:
                # Reset X position
                current_x_pos = 2

                # Increment Y position
                current_y_pos += qr_size

                # Reset counter
                row_counter = 0

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
    # Create PDF!
    generate_pdf()
