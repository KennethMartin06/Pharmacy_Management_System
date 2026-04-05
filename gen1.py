from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, Preformatted)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

W, H = A4
DARK  = colors.HexColor('#2c3e50')
BLUE  = colors.HexColor('#3498db')
GREEN = colors.HexColor('#27ae60')
LGRAY = colors.HexColor('#f2f2f2')
WHITE = colors.white

styles = getSampleStyleSheet()

def s(name, **kw):
    base = styles[name]
    return ParagraphStyle(base.name+'_c', parent=base, **kw)

TITLE    = s('Title',   fontSize=20, textColor=DARK,  spaceAfter=6,  leading=24, alignment=TA_CENTER)
SUB      = s('Normal',  fontSize=12, textColor=colors.HexColor('#7f8c8d'), alignment=TA_CENTER, spaceAfter=4)
H1       = s('Heading1',fontSize=14, textColor=WHITE,  spaceAfter=4,  spaceBefore=14, leading=18)
H2       = s('Heading2',fontSize=12, textColor=DARK,   spaceAfter=3,  spaceBefore=10, leading=15)
BODY     = s('Normal',  fontSize=10, leading=14, spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = s('Normal',  fontSize=10, leading=14, spaceAfter=3, leftIndent=16, bulletIndent=6)
CODE_ST  = ParagraphStyle('code', fontName='Courier', fontSize=8, leading=11,
                           backColor=LGRAY, leftIndent=8, rightIndent=8,
                           spaceAfter=8, spaceBefore=4)

def header_row(txt):
    return [Table([[Paragraph(txt, s('Normal', fontSize=13, textColor=WHITE, fontName='Helvetica-Bold'))]],
                  colWidths=[W - 5*cm],
                  style=TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK),
                                    ('TOPPADDING',(0,0),(-1,-1),6),
                                    ('BOTTOMPADDING',(0,0),(-1,-1),6),
                                    ('LEFTPADDING',(0,0),(-1,-1),10)]))]

def code_block(text):
    lines = text.strip().split('\n')
    rows  = [[Paragraph(l.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'),
                        CODE_ST)] for l in lines]
    t = Table(rows, colWidths=[W - 5.5*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LGRAY),
                            ('TOPPADDING',(0,0),(-1,-1),1),
                            ('BOTTOMPADDING',(0,0),(-1,-1),1),
                            ('LEFTPADDING',(0,0),(-1,-1),8),
                            ('RIGHTPADDING',(0,0),(-1,-1),4),
                            ('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#cccccc'))]))
    return t

print("Module 1 ok")
