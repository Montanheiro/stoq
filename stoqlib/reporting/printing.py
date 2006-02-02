# -*- Mode: Python; coding: iso-8859-1 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2006 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
## USA.
##
"""
stoqlib/reporting/printing.py:

    Implementa��o de classe base para configura��o da p�gina e desenho de
    elementos fixos de cada p�gina.
"""

import datetime

from reportlab.lib.units import mm

# sibling imports
from stoqlib.reporting.template import BaseReportTemplate
from stoqlib.reporting.default_style import (HIGHLIGHT_COLOR, SPACING,
                                             TEXT_COLOR)

SMALL_FONT = ("Helvetica", 12)

class ReportTemplate(BaseReportTemplate):
    """ 
    Classe respons�vel pela configura��o da p�gina e desenho de elementos
    fixos de cada p�gina. 
    """
    header_height = 10 * mm
    footer_height = 7 * mm
    def __init__(self, filename, report_name, timestamp=0, do_header=1, 
                 do_footer=1, **kwargs):
        """
        Classe respons�vel pela configura��o/desenho b�sico de cada p�gina.
        Seus par�metros s�o:

            - filename: o nome do arquivo onde o relat�rio deve ser
            desenhado. Esse nome de arquivo � passado como primeiro
            par�metro para a classe do usu�rio atrav�s da fun��o
            build_report().
            - report_name: o nome do relat�rio, utilizado, basicamente, na
            constru��o do rodap� da p�gina.
            - timestamp: define se a hora de cria��o do relat�rio deve ser
            especificada no rodap�.
            - do_header: se definido como True, chama o m�todo draw_header()
            da classe do usu�rio para o desenho do cabe�alho do relat�rio.
            Esse m�todo � chamado para cada p�gina criada.
            - do_footer: se definido como True, insere um rodap� em cada
            p�gina criada.
        """
        self.timestamp = timestamp
        BaseReportTemplate.__init__(self, filename, report_name,
                                    do_header=do_header, do_footer=do_footer,
                                    **kwargs)

    def draw_header(self, canvas):
        """
        Definido para fins de compatibilidade. Quando o usu�rio especificar um
        argumento True para o par�metro do_header, o m�todo draw_header() da
        classe do usu�rio � chamado. Se este m�todo n�o existir, o m�todo
        desta classe � chamado para evitar o levantamento de excess�o.
        """
        return
       
    def draw_footer(self, canvas):
        """
        M�todo chamado para o desenho do rodap� de p�ginas. Esse m�todo �
        chamado para cada p�gina criada se o par�metro 'do_footer' da classe  
        esteja definido como TRUE (valor padr�o assumido caso o usu�rio n�o o
        especifique). O rodap� � constitu�do basicamente do nome do relat�rio
        (par�metro report_class da classe), a data de gera��o, a hora (caso o
        par�metro time_stamp da classe seja definido como TRUE) e o n�mero da
        p�gina atual.
        """
        if not self.do_footer:
            return

        ts = datetime.datetime.now()
        if self.timestamp:
            date_string = ts.strftime('%d/%m/%Y   %H:%M:%S')
        else:
            date_string = ts.strftime('%d/%m/%Y')

        page_number = "P�gina: % 2d" % self.get_page_number()

        # Let's start drawing
        
        canvas.setFillColor(HIGHLIGHT_COLOR)
        canvas.rect(self.leftMargin, self.bottomMargin, self.width,
                    self.footer_height, stroke=0, fill=1)
        text_y = self.bottomMargin + 0.5 * SPACING
        canvas.setFillColor(TEXT_COLOR)
        canvas.setFont(*SMALL_FONT)
        canvas.drawString(self.leftMargin + 0.5 * SPACING, text_y,
                          self.report_name)
        canvas.drawRightString(self._rightMargin - 75, text_y, date_string)
        canvas.drawRightString(self._rightMargin - 0.5 * SPACING, text_y,
                               page_number)

