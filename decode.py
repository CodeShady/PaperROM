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
import hashlib

# Important variables
is_pdf = None

class PaperROMDecoder:
    def __init__(self):
        self.output_string = []
        self.final_output_string = []
        self.counted_qr_codes = 0 # Keep track of number of counted QR codes

    def decode_png(self):
        # Read image
        img = cv.imread("tmp-reading-file.png")
        
        # Loop through PDF to find all QR codes
        for code in decode(img):
            # Check if the code is an info QR code
            if code.data[:10] == b'!INFOFILE!':
                # Extract info from info QR code
                info_code = code.data.decode("utf-8").split("\n")
                self.total_qr_codes = info_code[1] # Total number of QR codes
                self.correct_hash = info_code[2] # MD5 Hash
                self.output_file_name = info_code[3] # Output File Name
            else:
                # Increment counter qr code variable
                self.counted_qr_codes += 1
                # Save QR code data to a big string
                self.output_string.append(code.data.decode("utf-8"))
    
    def get_file_hash(self):
        return hashlib.md5(self.output_file_name.encode("utf-8")).hexdigest()

    def generate_file(self):
        # Sort the list
        output_string = natsorted(self.output_string)

        # Remove ordered numbers in the output_string
        for item in output_string:
            self.final_output_string.append(item[item.index("-")+1:])
        
        # Check if correct number of QR codes were scanned
        if self.counted_qr_codes == int(self.total_qr_codes):
            print(f" INFO - Scanned {self.counted_qr_codes}/{self.total_qr_codes} QR Codes successfully!")
        else:
            # Error! Some QR codes weren't scanned!!! Oh nose!
            print(f"\n WARNING!!! - Scanned {self.counted_qr_codes}/{self.total_qr_codes}!\n Something went wrong when scanning the QR Codes!\n Try getting a clearer scan of the QR Codes!")
            sys.exit(1)

        # Save the big string to the output file
        with open(".tmp-" + self.output_file_name, "w") as output_file:
            for string in self.final_output_string:
                output_file.write(string)
            output_file.close()

        # Rewrite the file as decoded base64
        os.system(f"cat '.tmp-{self.output_file_name}' | base64 -d > '{self.output_file_name}'")

        # Check if file hashes match
        if self.get_file_hash() == self.correct_hash:
            print(" INFO - Hashes match! Meaning, no data was lost!")
        else:
            print(f" WANRING!!! - {self.counted_qr_codes}/{self.total_qr_codes} QR Codes were scanned successfully, but the authentic MD5 hash doesn't match with your new file!\n This could mean that your file is corrupt!")

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

    # Create a PaperROM class
    paperROM = PaperROMDecoder()

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
        paperROM.decode_png()
    
    paperROM.generate_file()
