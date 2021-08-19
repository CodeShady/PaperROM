
# PaperROM 📄

## What is PaperROM?
PaperRom is an easy way to store **actual** digital files on a piece of paper.
By encoding your files with the PaperROM encoder, you can get a printable PDF with your data which can later be decoded by the PaperROM decoder.
One sheet of paper hold an estimated **50 Kilobytes** of data--as of right now.

## How Does It Work?
**QR Codes are cool,** but I thought it would be way cooler if they could hold something more than just a URL. Of course, QR Codes can be expanded to a **huge size** and can hold about **3KB** of data. But, I didn't want to just throw a giant QR Code on a piece of paper and call it a day. **I wanted multiple QR Codes. I wanted more data.**

📥 **The PaperROM encoder** works by taking a file and breaking it up into multiple pieces. It then distributes those pieces into multiple QR Codes. The script then saves each QR Code into a directory the user selected. The script also gets some information such as the **MD5 hash** of your original file which gets stored into a small QR Code you'll find at the bottom right of your printable PDF. You can then use another script to take all these QR Codes and format them onto a printable PDF.

📤 **The PaperROM decoder** works by taking an encoded PDF or PNG and detecting all QR Codes. It then takes all the QR Code's data and places them in the correct order. Then, it constructs the file into the original version again. After everything is finished, the decoder checks to see if the original file's hash matches with the newly generated file. It also checks to see if they expected number of QR Codes were scanned to make sure there isnt' any corruption.

⚠️ **The PaperROM encoder does not compress your files!!!** If the file you're trying to encode is something that should be compressed, do it before encoding!

## Usage 🛠
Usage is pretty simple. You'll get a few self explanatory prompts when you run the script.


**To Encode a File**

	$ python3 decode.py

**To Generate a Printable PDF**

	$ python3 qr2pdf.py

**To Decode a PDF or PNG File**

	$ python3 decode.py



### ⚠️ If you got an error saying this...
	
**`ImportError: Unable to find zbar shared library`**

You'll need to install the **[zbar](https://github.com/ZBar/ZBar)** package on your computer. This is a package that helps with reading barcodes.

	(Max OSX) $ brew install zbar
	(Ubuntu)  $ sudo apt-get install zbar-tools
	(Fedora)  $ dnf install zbar


## Possible Upgrades

 - Displaying checksum hash on PDF. (Not really needed because the decode.py script checks this automatically)
