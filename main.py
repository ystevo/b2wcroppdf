import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyQt5 import uic, QtWidgets
import subprocess
import os
import platform

pdfSelected = ''
folderSelected = ''
current_index = 0
numPages = 0


def file_open():
    global pdfSelected
    pdfSelected = QtWidgets.QFileDialog.getOpenFileName()[0]
    window.txtPDF.setText(pdfSelected)


def folder_open():
    global folderSelected
    folderSelected = QtWidgets.QFileDialog.getExistingDirectory()
    window.txtFolder.setText(folderSelected)


def pdf_slit():
    with open(pdfSelected, "rb") as in_f:
        global current_index
        global numPages
        input1 = PdfFileReader(in_f)
        input2 = PdfFileReader(in_f)
        output = PdfFileWriter()

        numPages = input1.getNumPages()

        for i in range(numPages):
            pages = input1.getPage(i)
            if(i != 0):
                current_index = i
            progress_bar()
            pages.mediaBox.lowerRight = (813, 40)
            pages.mediaBox.upperLeft = (504, 456)
            print(pages.mediaBox.getLowerRight(),
                  pages.mediaBox.getUpperLeft())
            pages.cropBox.lowerRight = (800, 40)
            pages.cropBox.upperLeft = (472, 456)
            pages.scaleTo(4*72, 6*72)

            output.addPage(pages)

        for j in range(numPages):
            page = input2.getPage(j)
            if(j != 0):
                current_index = i+j
            progress_bar()
            page.mediaBox.lowerRight = (346, 40)
            page.mediaBox.upperLeft = (35, 456)
            page.cropBox.lowerRight = (339, 40)
            page.cropBox.upperLeft = (35, 456)
            page.scaleTo(4*72, 6*72)
            output.addPage(page)

        with open(folderSelected+"\out.pdf", "wb") as out_f:
            output.write(out_f)

        if platform.system() == 'Darwin':
            subprocess.call(('open', folderSelected+"\out.pdf"))
        elif platform.system() == 'Windows':
            os.startfile(folderSelected+"\out.pdf")
        else:
            subprocess.call(('xdg-open', folderSelected+"\out.pdf"))


def progress_bar():
    if(current_index != 0):
        prc = (current_index / numPages) * 100
        window.progressBar.setValue(int(prc))


app = QtWidgets.QApplication([])
window = uic.loadUi("mainwin.ui")

window.btnFile.clicked.connect(file_open)
window.btnFolder.clicked.connect(folder_open)
window.btnAction.clicked.connect(pdf_slit)

window.show()
app.exec()
