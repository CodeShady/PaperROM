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
import base64

class PaperROMEncoder:
    def __init__(self, input_filename, output_directory, qr_block_size=2100):
        self.input_filename = input_filename # input_file = "myFile.txt" (or something like that)
        self.output_directory = output_directory
        self.qr_block_size = qr_block_size


    def read_file_contents(self):
        # Read file and return value as base64
        with open(file_name, "rb") as input_file:
            file_bytes = input_file.read()
            # Encode file with Base64 (and return the value)
            return base64.b64encode(file_bytes).decode("utf-8")


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
        # Print info message
        print(" Generating QR code! (QR Code block length = %s chars)" % len(block_data))
        
        # Create QR Code class
        QR = qrcode.QRCode(
            version=2,
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
    file_name = input(" File To Encode (Preferrably a Zip File): ")
    output_directory = input(" Where should I put all your QR codes? Path: ")

    if output_directory == "":
        output_directory = "./"

    # Create PaperROMEncoder class                        \/ You can also add a custom QR block size! (Default is 2100 bytes)
    paperROM = PaperROMEncoder(file_name, output_directory)
    paperROM.split_data(paperROM.read_file_contents())
