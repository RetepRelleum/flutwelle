cd /home/retep/shell/qgis/pluginTest/flutwelle
source ../venv/bin/activate
pyrcc5 resources.qrc -o resources.py
deactivate
rm -r -f /home/retep/.local/share/QGIS/QGIS3/profiles/default/python/plugins/flutwelle
cp -r ../flutwelle/ /home/retep/.local/share/QGIS/QGIS3/profiles/default/python/plugins/flutwelle