# Auto Bookmark
This is a python project to generate PDF's bookmarks automatically.

Use this python file, you can export PDF's bookmarks to a user-defined
file, modify it easily and then import the content in the file to the PDF.

## Bookmark file format
Example:

```
	Chapter 1 Title 1 1
	Chapter 2 Title 2 4
		2.1 SubTitle 2.1 4.2
			2.1.1 SubTitle 2.1.1 4.5
		2.2 SubTitle 2.2 7.3
	Chapter 3 Title 3 8
```

The hierarchical structure of the bookmarks is controled by the Tab numbers
at the begining of each line. In each line, the content is
|tabs| |bookmark title| |page ratio|. |bookmark title| and |page ratio|
must be separated by white spaces.|page ratio| is a decimal number,
the integer part represents the page numberof the bookmark, 
the fractional part represents the location of the bookmark:
.0 indicates that the bookmark is on the top of the page, .99 indicates that
the bookmark is almost on the bottom of the page.

## Usage
Typical usage of the file is:
```
import sys
from PdfBookmark import PdfBookmark

sys.path.append('C:/PyPDF2') # add PyPDF2 path to system path
bm = PdfBookmark('a0.pdf')
bm.exportBookmark('test.bm')
```
Then view and modify the bookmark file as you need.
When you've finished your modification, you can use the following code to create new
bookmarks in the PDF.
```
bm.importBookmark('test.bm')
```
Another PDF file with the name `*PDFFILENAME*_bookmark.pdf` will be created by default, 
you can also provide a PDF file name when you call the function `importBookmark`
```
bm.importBookmark('test.bm', 'a1.pdf')
```