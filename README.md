
<img src="https://github.com/CodeShady/PaperROM/blob/main/banner.png" alt="PaperROM Banner">

## What is PaperROM?
PaperRom is an easy way to store **actual** digital files on a piece of paper.
By encoding your files with the PaperROM encoder, you can get a printable PDF with your data which can later be decoded by the PaperROM decoder.
One sheet of paper can hold an estimated **200 Kilobytes** of data with the best settings.

## But why paper?
> "Generally speaking, good quality paper stored in good conditions (cooler temperatures; 30-40% relative humidity) are able to last a long time -- even hundreds of years." -Google.com

## How Does It Work?
**QR Codes are cool,** but I thought it would be way cooler if they could hold something more than just a URL. Of course, QR Codes can be expanded to a **huge size** and can hold about **3KB** of data. But, I didn't want to just throw a giant QR Code on a piece of paper and call it a day. **I wanted multiple QR Codes. I wanted more data.**

📥 **The PaperROM encoder** works by taking a file and breaking it up into multiple pieces. It then distributes those pieces into multiple QR Codes. The script then saves each QR Code into a directory the user selected. The script also gets some information such as the **MD5 hash** of your original file which gets stored into a small QR Code you'll find at the bottom right of your printable PDF. You can then use another script to take all these QR Codes and format them onto a printable PDF.

📤 **The PaperROM decoder** works by taking an encoded PDF or PNG (decoding manually is also possible) and detecting all QR Codes. It then takes all the QR Code's data and places them in the correct order. Then, it constructs the file back into the original file. After everything is finished, the decoder checks to see if the original file's hash matches with the newly generated file. It also checks to make sure that the expected number of QR Codes were scanned and will notify the user if some were unreadable.

⚠️ **The PaperROM encoder does not compress your files!!!** If the file you're trying to encode is something that should be compressed, do it before encoding!

## Usage 🛠
Usage is pretty simple. You'll get a few self explanatory prompts when you run the script.

**To Encode a File**

	$ python3 encode.py

**To Generate a Printable PDF**

	$ python3 qr2pdf.py

**To Decode a PDF or PNG File**

	$ python3 decode.py

### ⚠️ If you got an error saying...
	
**`ImportError: Unable to find zbar shared library`**

You'll need to install the **[zbar](https://github.com/ZBar/ZBar)** package on your computer. This is a package that helps with reading barcodes.

	(Max OSX) $ brew install zbar
	(Ubuntu)  $ sudo apt-get install zbar-tools
	(Fedora)  $ dnf install zbar

**`Unable to get page count. Is poppler installed and in PATH?`**

You'll need to install the **[poppler](https://poppler.freedesktop.org)** package on your computer. This is a package that helps with reading pdf files.

	(Max OSX) $ brew install poppler
	(Ubuntu)  $ sudo apt-get install poppler-utils


## Possible Upgrades

 - Displaying checksum hash on PDF. (Not really needed because the decode.py script checks this automatically)
 - Add an option that the user can select to display the text data next to the QR code in case the QR code becomes unreadable (aka. manual restoration).
