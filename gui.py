# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testgui1.ui'
#
# Created: Sun Jun 15 16:20:32 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

    def input_equation(self):        
        text, ok = QtGui.QInputDialog.getText(None, 'Input equation', 'Enter equation:')
        item = QtGui.QStandardItem(text)
        self.reactionslistmodel.appendRow(item)
        self.reactionslist.setModel(self.reactionslistmodel)

    def remove_reaction(self):
        self.reactionslist.removeChild(self.reactionslist.selectedItem())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(706, 511)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 706, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuShow = QtGui.QMenu(self.menuBar)
        self.menuShow.setObjectName(_fromUtf8("menuShow"))
        MainWindow.setMenuBar(self.menuBar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.reactionslist = QtGui.QListView(self.dockWidgetContents)
        self.reactionslist.setObjectName(_fromUtf8("reactionslist"))
        self.reactionslistmodel = QtGui.QStandardItemModel(self.reactionslist)
        self.verticalLayout_2.addWidget(self.reactionslist)
        self.newreaction = QtGui.QPushButton(self.dockWidgetContents)
        self.newreaction.setObjectName(_fromUtf8("newreaction"))
        self.verticalLayout_2.addWidget(self.newreaction)
        self.removereaction = QtGui.QPushButton(self.dockWidgetContents)
        self.removereaction.setObjectName(_fromUtf8("removereaction"))
        self.verticalLayout_2.addWidget(self.removereaction)
        self.clearreactions = QtGui.QPushButton(self.dockWidgetContents)
        self.clearreactions.setObjectName(_fromUtf8("clearreactions"))
        self.verticalLayout_2.addWidget(self.clearreactions)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.actionAdd_new_node = QtGui.QAction(MainWindow)
        self.actionAdd_new_node.setObjectName(_fromUtf8("actionAdd_new_node"))
        self.actionGenerate_random_topology = QtGui.QAction(MainWindow)
        self.actionGenerate_random_topology.setObjectName(_fromUtf8("actionGenerate_random_topology"))
        self.actionCreate_new_random_network = QtGui.QAction(MainWindow)
        self.actionCreate_new_random_network.setObjectName(_fromUtf8("actionCreate_new_random_network"))
        self.actionReactions = QtGui.QAction(MainWindow)
        self.actionReactions.setObjectName(_fromUtf8("actionReactions"))
        self.toolBar.addAction(self.actionAdd_new_node)
        self.toolBar.addAction(self.actionGenerate_random_topology)
        self.toolBar.addAction(self.actionCreate_new_random_network)
        self.menuShow.addAction(self.actionReactions)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuShow.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.newreaction.clicked.connect(self.input_equation)
        self.removereaction.clicked.connect(self.remove_reaction)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "DNAtwork", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuShow.setTitle(_translate("MainWindow", "Show", None))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Expressions", None))
        self.newreaction.setText(_translate("MainWindow", "Add new...", None))
        self.removereaction.setText(_translate("MainWindow", "Remove", None))
        self.clearreactions.setText(_translate("MainWindow", "Clear all", None))
        self.actionAdd_new_node.setText(_translate("MainWindow", "Add new node", None))
        self.actionAdd_new_node.setToolTip(_translate("MainWindow", "Add a new node to the network", None))
        self.actionGenerate_random_topology.setText(_translate("MainWindow", "Generate random topology", None))
        self.actionGenerate_random_topology.setToolTip(_translate("MainWindow", "Use current nodes to generate a new random network", None))
        self.actionCreate_new_random_network.setText(_translate("MainWindow", "Create new random network...", None))
        self.actionCreate_new_random_network.setToolTip(_translate("MainWindow", "Creates a brand new random network ", None))
        self.actionReactions.setText(_translate("MainWindow", "Reactions", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

