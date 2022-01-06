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

#################################
#               #               #
#               #               #
#  Upper left   #  Upper right  #
#               #               #
#               #               #
#################################
#               #               #
#               #               #
#  Lower right  #  Lower left   #
#               #               #
#               #               #
#################################


def file_open():
    global pdfSelected
    pdfSelected = QtWidgets.QFileDialog.getOpenFileName()[0]
    window.txtPDF.setText(pdfSelected)


def folder_open():
    global folderSelected
    folderSelected = QtWidgets.QFileDialog.getExistingDirectory()
    window.txtFolder.setText(folderSelected)


def b2w_split():
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

        pdf(output)


def magalu_split():
    with open(pdfSelected, "rb") as in_f:
        global current_index
        global numPages

        input1 = PdfFileReader(in_f)
        input2 = PdfFileReader(in_f)
        input3 = PdfFileReader(in_f)
        input4 = PdfFileReader(in_f)
        output = PdfFileWriter()

        numPages = input1.getNumPages() * 4 - 4
        numPagesa = input1.getNumPages()
        print("document has %s pages." % numPages)

        # upper left
        for i in range(numPagesa):
            pages1 = input1.getPage(i)
            if(i != 0):
                current_index = i
            progress_bar()
            if(i == 0):  # first page is PLP so we ignore it
                continue
            pages1.mediaBox.lowerRight = (300, 420)

            pages1.scaleTo(4*72, 6*72)
            output.addPage(pages1)
            print(i)

        # upper right
        for j in range(numPagesa):
            pages2 = input2.getPage(j)
            if(j != 0):
                current_index = i+j
            progress_bar()
            if(j == 0):  # first page is PLP so we ignore it
                continue
            pages2.mediaBox.lowerRight = (600, 420)
            pages2.mediaBox.upperLeft = (300, 840)

            pages2.scaleTo(4*72, 6*72)
            output.addPage(pages2)

        # lower left
        for k in range(numPagesa):
            pages3 = input3.getPage(k)
            if(j != 0):
                current_index = i+j+k
            progress_bar()
            if(k == 0):  # first page is PLP so we ignore it
                continue
            pages3.mediaBox.lowerRight = (300, 1)
            pages3.mediaBox.upperLeft = (1, 420)

            pages3.scaleTo(4*72, 6*72)
            output.addPage(pages3)

        # lower right
        for l in range(numPagesa):
            pages4 = input4.getPage(l)
            if(l != 0):
                current_index = i+j+k+l
            progress_bar()
            if(l == 0):  # first page is PLP so we ignore it
                continue
            pages4.mediaBox.lowerRight = (600, 1)
            pages4.mediaBox.upperLeft = (300, 420)

            pages4.scaleTo(4*72, 6*72)
            output.addPage(pages4)

        pdf(output)


def pdf(output):
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
window.btnActionB2W.clicked.connect(b2w_split)
window.btnActionMagalu.clicked.connect(magalu_split)

window.show()
app.exec()
