# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RoutePrototype
                                 A QGIS plugin
 This is a prototype for Paulo's plugin.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-04-21
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Paulo
        email                : pmanal1@students.towson.edu
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
import processing

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .route_prototype_dialog import RoutePrototypeDialog
import os.path


class RoutePrototype:
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
            'RoutePrototype_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Route Prototype')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

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
        return QCoreApplication.translate('RoutePrototype', message)


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

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/route_prototype/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Route prototype'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Route Prototype'),
                action)
            self.iface.removeToolBarIcon(action)

    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
        self.dlg, "Select   output file ","", '*.shp')
        self.dlg.fileLocation.setText(filename)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = RoutePrototypeDialog()
            self.dlg.pushButton.clicked.connect(self.select_output_file)

        # show the dialog
        self.dlg.show()

        self.dlg.distanceInterval.setMaximum(5000)
        self.dlg.startOffset.setMaximum(5000)
        self.dlg.endOffset.setMaximum(5000)
        

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed

        # Accessing layer option: self.dlg.mapLayerBox.currentLayer().name()
        # Accessing coordinate X: self.dlg.spinBox_X.value()

        # Place a point:
        # newPoint = QgsFeature(newPoint ID)
        # newPoint.setAttributes(array of attributes)
        # newPoint.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(xy-coordinate location)))

        # Place a line:
        # newLine = QgsFeature(newLine ID)
        # newLine.setAttributes(array of attributes)
        # newLine.setGeometry(QgsGeometry.fromPolyLineXY([array of QgsPointXY objects to connect to create a line]))

        #

        if result:
            # print(self.dlg.mapLayerBox.currentLayer().name())
            layer = self.dlg.mapLayerBox.currentLayer()
            interval = self.dlg.distanceInterval.value()
            startOffset = self.dlg.startOffset.value()
            endOffset = self.dlg.endOffset.value()
            fileName = self.dlg.fileLocation.text()

            parameters = {
                'INPUT': layer,
                'DISTANCE': interval,
                'START_OFFSET': startOffset,
                'END_OFFSET': endOffset,
                'OUTPUT': fileName
            }

            # required input: layer, distance interval, start offset, end offset, where to put output 
            newLayer = processing.run("native:pointsalonglines", parameters)

