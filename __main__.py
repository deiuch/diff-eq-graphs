import modules_inst

# Install all required modules if they are not installed
modules_inst.install('PyQt5', 'pyqtgraph')

from main import main

main()
