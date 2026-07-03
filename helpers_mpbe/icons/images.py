#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  images.py
#
#  Copyright 2017 Martin Pablo Bellanca <mbellanca@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
'''Modulo de Imagenes

B{Created:} 01/04/18

@author: Martin Pablo Bellanca
@contact: mpbellanca@gmail.com
@license: GPL3
@organization: mpbe
'''

import wx



execute_i32 = wx.Image('./icons/exec-32.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()