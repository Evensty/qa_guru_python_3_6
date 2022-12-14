import os
import zipfile
import pathlib
from PyPDF2 import PdfReader
from io import BytesIO, TextIOWrapper
import PyPDF2
import csv


current_dir = os.path.dirname(os.path.abspath(__file__))
res_dir = os.path.join(current_dir, 'resources')
file_dir = pathlib.Path(os.path.join(current_dir, 'files'))
files = os.path.join(current_dir, 'files')
archive = os.path.join(res_dir, 'resources.zip')


# ADD FILES TO ZIP
with zipfile.ZipFile(archive, 'w') as zf:
    for file in file_dir.iterdir():
        zf.write(file, arcname=file.name)
    archive_file_names = []
    for file in zf.namelist():
        archive_file_names.append(file)


# READ INITIAL FILE DIRECTORY
for file in os.listdir(files):
    if '.pdf' in file:
        reader = PdfReader(os.path.join(file_dir, file))
        pdf_text = ''
        for page in reader.pages:
            pdf_text += page.extractText()

    if '.csv' in file:
        with open(os.path.join(file_dir, file), 'r') as csv_:
            csv_reader = csv.reader(csv_)
            csv_text = []
            for row in csv_reader:
                csv_text += row
    if '.jpg' in file:
        img = (os.path.join(file_dir, file))
        img_size = os.path.getsize(img)


# TESTS
def test_should_be_match_number_of_files():
    assert len(archive_file_names) == len(os.listdir(file_dir))


def test_should_be_match_pdf_text():
    with zipfile.ZipFile(archive, 'r') as zf:
        for file in zf.namelist():
            if '.pdf' in file:
                pdf = PyPDF2.PdfFileReader(BytesIO(zf.read(file)))
                archived_pdf_text = ''
                for page in pdf.pages:
                    archived_pdf_text += page.extractText()
                    assert archived_pdf_text in pdf_text


def test_should_be_match_csv_text():
    with zipfile.ZipFile(archive, 'r') as zf:
        for file in zf.namelist():
            if '.csv' in file:
                with zf.open(file) as infile:
                    reader = csv.reader(TextIOWrapper(infile, 'utf-8'))
                    archived_csv_text = []
                    for row in reader:
                        archived_csv_text += row
    assert archived_csv_text == csv_text


def test_should_be_match_file_size(remove_zip_after_tests):
    with zipfile.ZipFile(archive, 'r') as zf:
        for file in zf.namelist():
            if '.jpg' in file:
                img = zf.getinfo(file)
                archived_img_size = img.file_size
    assert archived_img_size == img_size


