# -*- coding: utf-8 -*-

import sys
sys.path.append('PyPDF2/')

from PdfBookmark import PdfBookmark

bm1 = PdfBookmark('Samples/a1.pdf')
bm1.exportBookmark('Samples/a1.bm')

bm0 = PdfBookmark('Samples/a0.pdf')
bm0.importBookmark('Samples/a1.bm')
