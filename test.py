#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-

from re import I
import sys, os
sys.path.append('/Users/Ye/GitHub/PdfBookmark/')

from PdfBookmark import PdfBookmark

def P_export(TOC_File):
    if TOC_File[-3:] == 'pdf':
        TOC_File0 = PdfBookmark(TOC_File)
        TOC = TOC_File.rstrip('pdf')+'bm'
        TOC_File0.exportBookmark(TOC)
        pt = input('\n是否需要删除带目录的PDF文件？\n***注意！此操作无法撤销！***\n[*] [y/n]' )
        if pt == 'y' or pt == 'Y':
            os.remove(TOC_File)
            print('已删除', TOC_File)
    elif TOC_File[-2:] == 'bm':
        TOC = TOC_File
        print('已读取%s为目录！' % TOC_File)
    else:
        print('文件格式错误！')
        return(0)
    return(TOC)
        
def P_import(TOC):
    PDF_Without_TOC = input(r"[*] 待导入目录的PDF文件路径：")
    PDF_Without_TOC0 = PdfBookmark(PDF_Without_TOC)
    PDF_Without_TOC0.importBookmark(TOC)
    print('目录导入中......')

    p = input('目录导入完毕！\n新文件为%s。\n是否需要删除无目录的PDF文件？\n***注意！此操作无法撤销！***\n[*] [y/n]' % (PDF_Without_TOC.rstrip('.pdf')+'_bookmark.pdf') )
    if p == 'y' or p == 'Y':
        os.remove(PDF_Without_TOC)
        print('已删除',PDF_Without_TOC)
        
    d = input('是否需要删除bm文件？\n***注意！此操作无法撤销！***\n[*] [y/n]')
    if d == 'y' or d == 'Y':
        os.remove(TOC)
        print('已删除',TOC)

i = 0
while True:
    TOC_File = input(r"[*] 目录（bm或带目录的PDF）文件路径：")
    a = P_export(TOC_File)
    if a == 0:
        continue
    else:
        P_import(a)
        i+=1
    if input('已为%s个PDF导入目录。\n是否继续导入？\n[*] [y/n]' % i ) in ['n','N']:
        break
    else:
        continue
    

