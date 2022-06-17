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

import qrcode
import hashlib
import binascii
import pickle
from datetime import datetime

class PaperROMEncoder:
    def __init__(self, input_filename, output_directory, qr_block_size=2100):
        self.input_filename = input_filename # input_file = "myFile.txt" (or something like that)
        self.output_directory = output_directory
        self.qr_block_size = qr_block_size

        # Info
        self.qr_codes_generated = 0 # Keep track of how many QR codes were generated
        self.file_hash = self.get_file_hash()
    
    def convert_to_numbers(self, input_string):
        # QR Codes can store more numbers than charaters
        # So, this function converts the input_file/some string into numbers converting it to hexadecimal codes.
        return str(int(binascii.hexlify(input_string), 16))
  
    
    def get_file_hash(self):
        return hashlib.md5(self.input_filename.encode("utf-8")).hexdigest()


    def generate_info_file(self):
        # datetime object containing current date and time
        current_timestamp = str(datetime.now())
        # Generate information file (another QR code) for qr2pdf.py & decoder.py to pick up
        info_data = "qr-info\n" + str(self.qr_codes_generated) + "\n" + self.file_hash + "\n" + self.input_filename + "\n" + current_timestamp
        self.generate_qr(info_data, "qr-codes-info.png")


    def read_file_contents(self):
        # Read file and return value as base64
        with open(file_name, "rb") as input_file:
            file_bytes = input_file.read()
            # Encode file with the Pickle Library (and return the value)
            # Encoding with Pickle will ensure that no encoding will be messed up when
            # loading and storing any data.
            return pickle.dumps(file_bytes)


    def split_data(self, data):
        qr_index = 1
        counter = 0
        qr_current_block_data = ""
        
        if len(data) >= self.qr_block_size:
            # Data is larger than qr_block_size variable, iterate through it then:
            for byte in data:
                # If data is > than qr_block_size, break up the data into multiple QR codes
                if counter >= self.qr_block_size:
                    # Generate a qr code with this data
                    self.generate_qr(f"{qr_index}-" + qr_current_block_data, f"{qr_index}.png")
                    
                    # Reset counter / reset the temporary data / increase the index number for filenames
                    counter = 0
                    qr_current_block_data = ""
                    qr_index += 1

                # Add byte to qr_current_block_data
                qr_current_block_data += byte

                # Increment counter
                counter += 1
        else:
            # Data is smaller than qr_block_size variable, just create one QR code then:
            self.generate_qr(f"{qr_index}-" + data, f"{qr_index}.png")

        # Check if qr_current_block_data string is empty! If it isn't, then we're forgetting about valuable data!!
        if not len(qr_current_block_data) == 0:
            # Generate a last QR code for forgotten data
            self.generate_qr(f"{qr_index}-" + qr_current_block_data, f"{qr_index}.png")


    def generate_qr(self, block_data, qr_output_filename):
        # Increment info counter
        self.qr_codes_generated += 1

        # Print info message
        print(" Generating QR code! (QR Code block length = %s chars)" % len(block_data))
        
        # Create QR Code class
        QR = qrcode.QRCode(
            #version=40,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )

        # Add data to QR code
        QR.add_data(block_data)
        QR.make(fit=True)

        # Create the image
        img = QR.make_image(fill_color="black", back_color="white").convert("RGB")

        # Save the image
        img.save(self.output_directory + "/" + qr_output_filename)


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

 Welcome to PaperROM!

 PaperROM is an easy way to store digital files/data on pieces of paper for long term storage!

 This is the encode.py script. If you're trying to decode PaperROM data, use the decode.py script!

 For the documentation, visit the GitHub repo: https://github.com/CodeShady/PaperROM
""")

    # Get information
    file_name = input(" File To Encode (Tip: compress your data before encoding to save space!): ")
    output_directory = input(" Where should I put all your QR codes? Path: ")

    if output_directory == "":
        output_directory = "./"

    # Message
    print(" Generating... This may take a few minutes depending on how large your file is...")

    # Create PaperROMEncoder class                           \/ You can also add a custom QR block size! (Default is 2100 bytes)
    paperROM = PaperROMEncoder(file_name, output_directory, 5500)#1480)#5500)
    paperROM.split_data(paperROM.convert_to_numbers(paperROM.read_file_contents()))
    paperROM.generate_info_file()
