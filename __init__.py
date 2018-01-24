# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Measure3d
                                 A QGIS plugin
 Measure3d
                             -------------------
        begin                : 2017-12-22
        copyright            : (C) 2017 by s
        email                : s
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Measure3d class from file Measure3d.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .measure_3d import Measure3d
    return Measure3d(iface)
