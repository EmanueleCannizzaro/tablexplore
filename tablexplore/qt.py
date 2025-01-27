
"""
    TablExplore app
    Created January 2021
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

# handle qt imports depending on the available Qt python library
# This uses * imports which are generally frowned upon but tmakes it easier
# to use the classes in all other modules

import sys

from qtpy import QtCore
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import QObject, Signal, Slot
