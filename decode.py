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

import pickle
import cv2 as cv
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
import os, sys, hashlib, binascii
from natsort import natsorted

class PaperROMDecoder:
    def __init__(self):
        self.output_string = []
        self.final_output_string = []
        self.counted_qr_codes = 0 # Keep track of number of counted QR codes
        self.total_qr_codes = None # Total number of QR codes
        self.correct_hash = None # MD5 Hash
        self.output_file_name = None # Output File Name 
        self.date_created = ""

    def decode_png(self):
        # Read image
        img = cv.imread("tmp-reading-file.png")
        
        # Loop through PDF to find all QR codes
        for code in decode(img):
            # Check if the code is an info QR code
            if code.data[:10] == b'!INFOFILE!' or code.data[:7] == b'qr-info':
                # print(code.data)
                # Extract info from info QR code
                info_code = code.data.decode("utf-8").split("\n")
                self.total_qr_codes = info_code[1]      # Total number of QR codes
                self.correct_hash = info_code[2]        # MD5 Hash
                self.output_file_name = info_code[3]    # Output File Name
                self.date_created = info_code[4]        # Timestamp of when the codes were created
            else:
                # Increment counter qr code variable
                self.counted_qr_codes += 1
                # Save QR code data to a big string
                self.output_string.append(code.data.decode("utf-8"))
    
    def manual_decode(self, document_path, output_filename):
        # Read text file
        with open(document_path, "r") as document_data:
            for code_data in document_data.readlines():
                self.output_string.append(code_data)
        
        # Sort the output string
        output_string = natsorted(self.output_string)

        # Convert the data into a decoded file
        with open(output_filename, "wb+") as output_file:
            combined_data = ""
            for string in output_string:
                # Write the data to the file (also remove the numbering order at the start of the data "1-...", "2-...", etc.)
                combined_data += string[string.index("-")+1:]
            
            # Decode the Pickled data and write it to the new file
            output_file.write(pickle.loads(self.numbers_to_string(combined_data)))
            
            # Close the file
            output_file.close()
    
    def get_file_hash(self):
        return hashlib.md5(self.output_file_name.encode("utf-8")).hexdigest()
    

    def numbers_to_string(self, input_numbers):
        # This function converts the hexadecimal numbers back to the original text
        return binascii.unhexlify(format(int(input_numbers), "x").encode("utf-8"))


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
            print(" Continuing anyway...")

        # Save the big string to the output file
        with open(self.output_file_name, "wb+") as output_file:
            combined_data = ""
            for string in self.final_output_string:
                # Write the data to the file
                combined_data += string
            
            # Decode the Pickled data and write it to the new file
            output_file.write(pickle.loads(self.numbers_to_string(combined_data)))
            
            # Close the file
            output_file.close()

        # Check if file hashes match
        if self.get_file_hash() == self.correct_hash:
            print(" INFO - Hashes match! Meaning, no data was lost!")
        else:
            print(f" WARNING!!! - {self.counted_qr_codes}/{self.total_qr_codes} QR Codes were scanned successfully, but the original MD5 hash doesn't match with your new file!\n This could mean that your file is corrupt!")

        # Cleanup!
        os.system("rm tmp-reading-file.png")

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
    # Prompt user to select the input file type
    print(" -- Select Input Type --")
    print(" 1) .PDF (pdf)")
    print(" 2) .PNG (png)")
    print(" 2) Text File (txt)")

    input_filetype = input("\n Is your PaperROM file a PDF, or PNG file? (pdf/png/txt): ")
    document_path = input(" Enter Document Location: ")

    # Create a PaperROM class
    paperROM = PaperROMDecoder()

    # Convert PDF to image
    if input_filetype == "pdf":
        # User is using a PDF file
        conversion_pdf = convert_from_path(document_path, 500)
        for page in conversion_pdf:
            page.save("tmp-reading-file.png", "png")
            #input(" Continue? ")
            paperROM.decode_png()
    
    elif input_filetype == "png":
        # User has a PNG, don't convert PDF!
        os.rename(document_path, "tmp-reading-file.png")
        # Decode PNG
        paperROM.decode_png()
    
    elif input_filetype == "txt":
        # User wants to decode a txt file with individual qr code scans
        print(" -- Manual QR Decode --")
        print(" To manually decode your data, make sure to scan each QR code individually. Then place the data of each qr code into a .txt file on seperate lines.")
        print(" Note: The manual decoding option doesn't currently support using the info QR code (small qr code at the bottom right of the page).")
        print("       The info QR code is plain text, so if you want to verify the checksum, scan it and you'll see a MD5 hash of the original file on the third line along with some more useful information. :)")

        output_filename = input("\n What is the output filename? (You can view this in the info QR code): ")

        # Decode Manually
        paperROM.manual_decode(document_path, output_filename)

        print(" Done!")

        sys.exit(0)

    else:
        print(" Oops! That's not a valid filetype option!")
        sys.exit(1)
    
    paperROM.generate_file()
