#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Dataexplore2 table app
    Created May 2017
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from __future__ import absolute_import, division, print_function
import sys,os,platform
from collections import OrderedDict
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import pandas as pd
from .core import TableModel, DataFrameTable, DataFrameWidget
from .plotting import PlotViewer
from . import util

class Application(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("pandas qt example")
        self.setWindowIcon(QIcon('logo.png'))
        self.createMenu()
        self.main = QTabWidget(self)
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width()*0.7, screen_resolution.height()*.7
        self.setGeometry(QtCore.QRect(150, 150, width, height))
        center = QDesktopWidget().availableGeometry().center()
        self.newProject()

        self.main.setFocus()
        self.setCentralWidget(self.main)
        self.statusBar().showMessage("Welcome", 3000)
        return

    def createMenu(self):

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&New', self.newProject,
                QtCore.Qt.CTRL + QtCore.Qt.Key_N)
        self.file_menu.addAction('&Save', self.fileQuit,
                QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Quit', self.fileQuit,
                QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.sheet_menu = QMenu('&Sheet', self)
        self.menuBar().addMenu(self.sheet_menu)
        self.sheet_menu.addAction('&Add', self.addSheet)

        self.tools_menu = QMenu('&Tools', self)
        self.tools_menu.addAction('&Table Info', self.info,
                QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        self.menuBar().addMenu(self.tools_menu)

        self.dataset_menu = QMenu('&Datasets', self)
        self.menuBar().addMenu(self.dataset_menu)
        self.dataset_menu.addAction('&Sample', self.sampleData)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction('&About', self.about)
        return

    def newProject(self):
        """New project"""

        self.main.clear()
        self.sheets = OrderedDict()
        self.addSheet()
        self.filename = None
        self.projopen = True
        return

    def closeProject(self):
        """Close"""

        return

    def addSheet(self, name=None, df=None):
        """Add a new sheet"""

        names = self.sheets.keys()
        if name is None:
            name = 'sheet'+str(len(self.sheets)+1)

        sheet = QSplitter(self.main)
        idx = self.main.addTab(sheet, name)

        l = QHBoxLayout(sheet)
        dfw = DataFrameWidget(sheet, dataframe=df)
        l.addWidget(dfw)
        self.sheets[idx] = dfw
        self.currenttable = dfw
        pf = dfw.createPlotViewer(sheet)
        l.addWidget(pf)
        sheet.setSizes((600,200))

        return

    def removeSheet(self, name):
        del self.sheets[name]
        return

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def sampleData(self):
        rows, ok = QInputDialog.getInt(self, 'Rows', 'Rows:', 100)
        if ok:
            df = util.getSampleData(rows,5)
            self.addSheet(None,df)
        return

    def getCurrentTable(self):
        idx = self.main.currentIndex()
        table = self.sheets[idx]
        return table

    def info(self):
        table = self.getCurrentTable()
        table.info()
        return

    def about(self):
        from . import __version__
        import matplotlib
        import PySide2
        pandasver = pd.__version__
        pythonver = platform.python_version()
        mplver = matplotlib.__version__
        qtver = PySide2.QtCore.__version__

        text='DataExplore2 Application\n'\
                +'Version '+__version__+'\n'\
                +'Copyright (C) Damien Farrell 2018-\n'\
                +'This program is free software; you can redistribute it and/or\n'\
                +'modify it under the terms of the GNU General Public License '\
                +'as published by the Free Software Foundation; either version 3 '\
                +'of the License, or (at your option) any later version.\n'\
                +'Using Python v%s, PySide2 v%s\n' %(pythonver, qtver)\
                +'pandas v%s, matplotlib v%s' %(pandasver,mplver)

        msg = QMessageBox.about(self, "About", text)
        return

def main():
    app = QApplication(sys.argv)
    aw = Application()
    aw.show()
    app.exec_()

if __name__ == '__main__':
    main()