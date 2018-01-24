# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Measure3d
                                 A QGIS plugin
 Measure3d
                              -------------------
        begin                : 2017-12-22
        git sha              : $Format:%H$
        copyright            : (C) 2017 by s
        email                : s
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
import resources
# Import the code for the dialog
from measure_3d_dialog import Measure3dDialog
import os.path
from qgis.core import QgsMessageLog
from PyQt4.QtGui import QMessageBox
from qgis.core import *
import math

class Measure3d:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Measure3d_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Measure3d')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Measure3d')
        self.toolbar.setObjectName(u'Measure3d')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Measure3d', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = Measure3dDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        #import os
        #icon_path = os.path.join(os.path.realpath(__file__), 'icon.png')
        icon_path = ':/plugins/measure3d/icon.png'

        self.add_action(
            icon_path,
            text=self.tr(u'Measure3d'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Measure3d'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            q_field = self.dlg.lineEdit.text()#.toPlainText()
            #layer = layers[selectedLayerIndex]
            layer = self.iface.activeLayer()
            try:
                features = layer.selectedFeatures()
            except AttributeError:
                QMessageBox.information(self.iface.mainWindow(), "Error", "Select a layer")
                return

            if len(features)!=2:
                QMessageBox.information(self.iface.mainWindow(), "Error", "Select two points")
                return


            #Create a measure object
            #d = QgsDistanceArea()
            #crs = layer.crs()
            #print crs.ellipsoidAcronym()
            #d.setEllipsoid(crs.ellipsoidAcronym())
            #d.setEllipsoidalMode(True)
            #Measure the distance
            #m = d.measureLine(point1, point2)
            #m = math.sqrt( m**2 + (float(features[0][q_field]) - float(features[1][q_field]) )**2 )

            # Use geometry Z value
            if self.dlg.checkBox.isChecked():
                try:
                    point1 = QgsPointV2()
                    point2 = QgsPointV2()
                    point1.fromWkt(features[0].geometry().exportToWkt())
                    point2.fromWkt(features[1].geometry().exportToWkt())
                    z1 = point1.z()
                    z2 = point2.z()
                    #print(z1, z2)
                except Exception, e:
                    #print(str(e))
                    QMessageBox.information(self.iface.mainWindow(), "Error", "I can't use geometry z value. Check your data.")
                    return
            else:#Use Z field value

                # Find z field name
                if not q_field or q_field == '':
                        q_field = 'z'

                try:
                    t = float(features[1][q_field])
                except KeyError:
                    QMessageBox.information(self.iface.mainWindow(), "Error", "The field '%s' does not exists in your layer" % q_field)
                    return
                except ValueError:
                    QMessageBox.information(self.iface.mainWindow(), "Error", "I can't use the field '%s' as z value. Check your data." % q_field)
                    return
                z1 = float(features[0][q_field])
                z2 = float(features[1][q_field])
                #print(z1, z2)

            point1 = features[0].geometry().asPoint()
            point2 = features[1].geometry().asPoint()

            res = math.sqrt( ( point1[0]-point2[0] )**2 +
                       ( point1[1]-point2[1] )**2 +
                       ( z1 - z2 )**2
                      )
            print res
            QMessageBox.information(self.iface.mainWindow(), "Distance", str(res) )
