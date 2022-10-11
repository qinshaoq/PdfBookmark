# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/Ye/GitHub/PdfBookmark/')

from PdfBookmark import PdfBookmark

bm1 = PdfBookmark('/Users/Ye/GitHub/PdfBookmark/Samples/a1.pdf')
bm1.exportBookmark('/Users/Ye/GitHub/PdfBookmark/Samples/a1.bm')

bm0 = PdfBookmark('/Users/Ye/GitHub/PdfBookmark/Samples/a0.pdf')
bm0.importBookmark('/Users/Ye/GitHub/PdfBookmark/Samples/a1.bm')
