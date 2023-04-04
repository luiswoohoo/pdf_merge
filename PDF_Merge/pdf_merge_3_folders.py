from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader
from natsort import natsorted
import os
import shutil

# This part of the script merges the PDF files
# Define input directory for the pdf files
pdf_dir_1 = Path(__file__).parent / "pdf_files_1"
pdf_dir_2 = Path(__file__).parent / "pdf_files_2"
pdf_dir_3 = Path(__file__).parent / "pdf_files_3"

# Define and create output directory
pdf_output_dir = Path(__file__).parent / "OUTPUT"
pdf_output_dir.mkdir(parents=True, exist_ok=True)

# List all pdf files in the input directory
# Sort files in first folder
pdf_files_1 = natsorted(list(pdf_dir_1.glob("*.pdf")))
pdf_files_2 = list(pdf_dir_2.glob("*.pdf"))
pdf_files_3 = list(pdf_dir_3.glob("*.pdf"))

# Go through each file in first folder and search for matches in second and third folders
# Append matches to file in first folder
for file_1 in pdf_files_1:
    merger = PdfFileMerger()
    merger.append(PdfFileReader(str(file_1), "rb"))
    name = file_1.name[:4]

    for file_2 in pdf_files_2:
        if file_2.name.find(name) != -1:
            merger.append(PdfFileReader(str(file_2), "rb"))

    for file_3 in pdf_files_3:
        if file_3.name.find(name) != -1:
            merger.append(PdfFileReader(str(file_3), "rb"))

    merger.write(str(pdf_output_dir / f"{name}.pdf"))
    merger.close()


# This part of the script moves the original file
# used for merging into another folder
pdf_dir_og = Path(__file__).parent / "z_og_files"
pdf_dir_og.mkdir(parents=True, exist_ok=True)

sourceFolders = [pdf_dir_1, pdf_dir_2, pdf_dir_3]

for sourceFolder in sourceFolders:
    # gather all files
    allFiles = os.listdir(sourceFolder)

    # iterate on all files to move them to destination folder
    for file in allFiles:
        src_path = os.path.join(sourceFolder, file)
        dst_path = os.path.join(pdf_dir_og, file)

        # check if file exists in destination
        if os.path.exists(dst_path):
            # Split name and extension
            file_name = os.path.splitext(file)
            name, extension = file_name
            # extension = file_name[1]
            # Add the new name
            new_name = f"{name}_new{extension}"
            # construct full file path
            new_path = os.path.join(pdf_dir_og, new_name)

            shutil.move(src_path, new_path)
        else:
            shutil.move(src_path, dst_path)
