from PyQt5.QtCore import QStandardPaths

appdata_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)

print(appdata_dir)