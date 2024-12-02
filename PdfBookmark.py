#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
#
# Author: Shaoqian Qin
# Contact: qinshaoq@gmail.com
#
# Function: 
# 	1) Export PDF's bookmarks to a user-defined bookmark file
#	2) Import from bookmark file and add bookmarks to PDF
#
# Requirement:
#	Python 3.10, PyPDF2
#
# Bookmark file format(Example):
# ******************************************
# *Chapter 1 Title 1 1                     *
# *Chapter 2 Title 2 4                     *
# *\t2.1 SubTitle 2.1 4.2                  *
# *\t\t2.1.1 SubTitle 2.1.1 4.5            *
# *\t2.2 SubTitle 2.2 7.3                  *
# *Chapter 3 Title 3 8                     *
# ******************************************
# \t represents a Tab key, other white spaces are not available temporarily.
# The number of Tab represents the hierarchical structure of the bookmark.
# In each line, the content is |tabs| |bookmark title| |page ratio|.
# |bookmark title| and |page ratio| must be separated by white spaces.
# |page ratio| is a decimal number, the integer part represents the page number
# of the bookmark, the fractional part represents the location of the bookmark.
# .0 indicates that the bookmark is on the top of the page, .99 indicates that
# the bookmark is almost on the bottom of the page.
#

import sys
import re
import codecs
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import PAGE_FIT


def _writeBookmarkToStream(outlines, stream, level):
    """
    Write bookmark to file strem.
    param outlines: PyPDF2.generic.Destination list
    param level: bookmark level, the topmost level is 0
    """
    for i in range(0, len(outlines)):
        outline = outlines[i]
        if type(outline) == list:
            _writeBookmarkToStream(outline, stream, level + 1)
        elif type(outline['/Page']) == PyPDF2.generic.NullObject:  # 存在不指向具体页面的空白目录（标签）项，跳过
            continue
        else:
            for j in range(0, level):
                stream.write('\t')
            bmTitle = outline['/Title']
            bmRatio = outline['/Ratio']
            stream.write(bmTitle + ' ' + ('%.2f' % bmRatio) + '\n')


def readBookmarkFromFile(bmPathName):
    """
    Read bookmark from file and store the content in dict list.
    return: outlines-dict list which has '/Title' and '/Ratio' keys
    """
    outlines = []
    lastTabNum = 0
    r = re.compile(r'\s*(.*)\s+(\d+\.*\d*)\s*')
    r2 = re.compile(r'\s*\S.*')
    for line in open(bmPathName):
        if not r2.match(line):  # line contain only white spaces
            continue
        matchObj = r.match(line)
        if not matchObj:
            print('bookmark file format error in: ' + line)
            sys.exit(0)
        tabNum = matchObj.start(1)
        bmTitle = matchObj.group(1)
        pageRatio = float(matchObj.group(2)) - 1
        bmPage = int(pageRatio)
        bmRatio = pageRatio - bmPage
        outline = {}
        outline['/Title'] = bmTitle
        outline['/Ratio'] = pageRatio
        tempOutlines = outlines
        if tabNum > lastTabNum + 1:
            print('bookmark file format error in: ' + line)
            sys.exit(0)
        elif tabNum == lastTabNum + 1:
            for i in range(0, tabNum - 1):
                tempOutlines = tempOutlines[-1]
            tempOutlines.append([outline])
        else:
            for i in range(0, tabNum):
                tempOutlines = tempOutlines[-1]
            tempOutlines.append(outline)
        lastTabNum = tabNum
    return outlines


def _writeOutlinesToPdf(outlines, output, parent):
    """
    Add bookmarks stored in outlines.
    param output: PyPDF2.PdfWriter object
    param parent: parent bookmark
    """
    lastBm = parent
    for i in range(0, len(outlines)):
        outline = outlines[i]
        if not type(outline) == list:
            ratio = outline['/Ratio']
            bmTitle = outline['/Title']
            bmTitle = u'\uFEFF' + bmTitle
            bmPage = int(ratio)
            bmCur = output.add_outline_item(str(bmTitle), bmPage, parent, None, None, False, False, PAGE_FIT)
            lastBm = bmCur
        else:
            _writeOutlinesToPdf(outline, output, lastBm)


class PdfBookmark(object):
    """
    This class supports import/export PDF's
    bookmarks from/to a file.
    """

    def __init__(self, pdfPathName):
        self.pdfFileName = pdfPathName
        self._pdfStream = open(self.pdfFileName, 'rb')
        self._pdfReader = PdfReader(self._pdfStream)

        self.pageLabels = self._getPageLabels()
        self.outlines = self._pdfReader.outline
        self._addPageRatio(self.outlines, self.pageLabels)

    def getBookmark(self):
        """
        Retrieve this pdf's bookmark.
        """
        return self.outlines

    def exportBookmark(self, bookmarkFile):
        """
        Export bookmarks to a file.
        """
        stream = codecs.open(bookmarkFile, 'w', encoding='utf8')
        _writeBookmarkToStream(self.outlines, stream, 0)
        print("Export %s's bookmarks to %s finished!" % (self.pdfFileName, bookmarkFile))

    def importBookmark(self, bookmarkFile, saveAsPdfName=None):
        """
        Import the contents from a bookmark file and add these bookmarks
        to the current pdf file or another pdf file.
        """
        outlines = readBookmarkFromFile(bookmarkFile)
        output = PdfWriter()
        for i in range(0, len(self._pdfReader.pages)):
            output.add_page(self._pdfReader.pages[i])
        _writeOutlinesToPdf(outlines, output, None)

        if saveAsPdfName == None:
            saveAsPdfName = self.pdfFileName[0:-4] + '_bookmark.pdf'
        stream = open(saveAsPdfName, 'wb')
        output.write(stream)
        print("Add bookmarks in %s to %s finished!" % (bookmarkFile, saveAsPdfName))

    def _getPageLabels(self):
        """
        Get the map from IndirectObject id to real page number.
        """
        pageLabels = {}
        pages = list(self._pdfReader.pages)
        for i in range(0, len(pages)):
            page: PyPDF2.pdf.PageObject = pages[i]
            pageLabels[page.indirect_ref.idnum] = i + 1
        return pageLabels

    def _addPageRatio(self, outlines, pageLabels):
        """
        Retrieves page ratio from Destination list.
        param outlines: Destination list
        param pageLabels: map from IndirectObject id to real page number
        """
        for i in range(0, len(outlines)):
            outline = outlines[i]
            if type(outline) == list:
                self._addPageRatio(outlines[i], pageLabels)
                continue
            elif not '/Page' in outline:
                print("Error: outline has no key '/Page'")
                sys.exit(-1)
            if type(outline['/Page']) == PyPDF2.generic.NullObject:  # 存在不指向具体页面的空白目录（标签）项，跳过
                continue
            pageHeight = outline['/Page']['/mediabox'][-1]
            idIndirect = outline.page.idnum
            if idIndirect in pageLabels:
                pageNum = pageLabels[idIndirect]
            else:
                print('Error: Page corresponds to IndirectObject %d not Found' % idIndirect)
                sys.exit(-1)
            if '/Top' in outline:
                top = outline['/Top']
            else:
                top = pageHeight
            if '/Zoom' in outline and type(outline['/Zoom']) != PyPDF2.generic.NullObject and outline[
                '/Zoom'] != 0:  # 排除outline['/Zoom']存在的特殊情况
                zoom = outline['/Zoom']
            else:
                zoom = 1
            outline = dict(outline)
            outline['/Ratio'] = pageNum + (1 - top / zoom / pageHeight)
            outlines[i] = outline


def main():

    # 以下为测试代码
    bm = PdfBookmark('/Users/name/Downloads/带目录的PDF/[美]卡斯滕·哈里斯：无限与视角.pdf')
    print (bm.getBookmark())
    bm.exportBookmark('/Users/name/Downloads/导出的bm文件/test1.bm')
    bm.importBookmark('/Users/name/Downloads/导入的bm文件/test2.bm')


if __name__ == '__main__':
    main()
