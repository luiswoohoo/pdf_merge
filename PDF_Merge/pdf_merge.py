from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader
from natsort import natsorted

# Define input directory for the pdf files
pdf_dir = Path(__file__).parent / "pdf_files"

# Define and create output directory
pdf_output_dir = Path(__file__).parent / "OUTPUT"
pdf_output_dir.mkdir(parents=True, exist_ok=True)

# List all pdf files in the input directory
pdf_files = natsorted(list(pdf_dir.glob("*.pdf")))

# Use first 4 characters as the key
keys = set([file.name[:7] for file in pdf_files])

for key in keys:
    merger = PdfFileMerger()
    for file in pdf_files:
        if file.name.find(key) != -1:  # returns an index, if not found returns -1
            merger.append(PdfFileReader(str(file), "rb"))
    merger.write(str(pdf_output_dir / f"{key}.pdf"))
    merger.close()
