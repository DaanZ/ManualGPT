import glob

from cto_toolshed.ai.documents.reader import read_pdf_path
from cto_toolshed.util.files import write_to_file

path = "data/Manual/*.pdf"

for file in glob.glob(path):
    text = read_pdf_path(file)
    write_to_file(file.replace(".pdf", ".txt"), text)
