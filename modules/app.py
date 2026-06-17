import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import sys

widget.QApplication.setAttribute(core.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
app = widget.QApplication(sys.argv)