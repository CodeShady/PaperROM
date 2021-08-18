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

    >>-- Links Used -->>
    Generate QR Codes - https://betterprogramming.pub/how-to-generate-and-decode-qr-codes-in-python-a933bce56fd0
    Create PDF Files - https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html

"""

#import qrcode
import cv2 as cv
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
import os, sys
from natsort import natsorted

# Important variables
is_pdf = None

class PaperROMDecoder:
    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.output_string = []
        self.final_output_string = []

    def decode_png(self):
        # Read image
        img = cv.imread("tmp-reading-file.png")
        
        # Loop through PDF to find all QR codes
        for code in decode(img):
            # Save QR code data to a big string
            self.output_string.append(code.data.decode("utf-8"))
    
    def generate_file(self):
        # Sort the list
        output_string = natsorted(self.output_string)

        # Remove ordered numbers in the output_string
        for item in output_string:
            self.final_output_string.append(item[item.index("-")+1:])
        
        # Save the big string to the output file
        with open(".tmp-" + self.output_file_name, "w") as output_file:
            for string in self.final_output_string:
                output_file.write(string)
            output_file.close()
        
        # Rewrite the file as decoded base64
        os.system(f"cat '.tmp-{self.output_file_name}' | base64 -d > '{self.output_file_name}'")

        # Cleanup!
        os.system("rm tmp-reading-file.png")
        os.system(f"rm '.tmp-{self.output_file_name}'")


# Main
if __name__ == "__main__":

    # Get information & print welcome message
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

 Welcome to PaperROM!

 PaperROM is an easy way to store digital files/data on pieces of paper for long term storage!

 This is the decode.py script. If you're trying to encode data to PaperROM storage, use the encode.py script!

 For the documentation, visit the GitHub repo: https://github.com/CodeShady/PaperROM
""")
    # Get information about document
    is_pdf = input(" Is your PaperROM file a PDF, or PNG file? (pdf/png): ")

    if is_pdf == "png":
        is_pdf = False
    elif is_pdf == "pdf":
        is_pdf = True
    else:
        print(" That wasn't a valid option!")
        sys.exit(1)

    document_path = input(" Enter Document Location: ")
    output_filename = input(" Enter Output Filename: ")

    # Create a PaperROM class
    paperROM = PaperROMDecoder(output_filename)

    # Convert PDF to image
    if is_pdf:
        # User is using a PDF file
        conversion_pdf = convert_from_path(document_path)
        for page in conversion_pdf:
            page.save("tmp-reading-file.png", "png")
            paperROM.decode_png()
    else:
        # User has a PNG, don't convert PDF!
        os.rename(document_path, "tmp-reading-file.png")
        # Decode PNG
        paperROM.decode_png(output_filename)
    
    paperROM.generate_file()
