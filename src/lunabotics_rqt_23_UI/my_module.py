import os
import rospy
import rospkg

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget, QLabel, QPushButton, QApplication
import datetime
import time
from python_qt_binding import QtCore
import threading

import rospy
from std_msgs.msg import String

class MyPlugin(Plugin):
    topicData = ""
    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('MyPlugin')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('lunabotics_rqt_23_UI'), 'resource', 'newPlug.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('MyPluginUi')
        # Show _widget.windowTitle on left-top of each plugin (when 
        # it's set in _widget). This is useful when you open multiple 
        # plugins at once. Also if you open multiple instances of your 
        # plugin at once, these lines add number to make it easy to 
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)

        
        # Set the label's text data, we can do this:
        # self._widget.ObjectLabelName.setText("dummy data")
        # To see the your Qlabel's created object name, open QT designer and view the obj name
        # For this simple label example, we have 2 labels and 2 input fields
        # On the first row on the left, we have "labelForSomeData" and on the right we have "inputFeedDataLabel"
        # on the second row on the left, we have "labelForSomeData_2" and on the right we have "inputFeedDataLabel"
        # With this information, we can perform different actions on objects

        # To update labels:
        self._widget.inputFeedDataLabel.setText("dataField_1")
        self._widget.inputFeedDataLabel_2.setText("dataField_2")
        # self._widget.inputFeedDataLabel_3.setText("dataField_2")

        # Now its up to you guys to get logic from various topics to input into those data fields
    
        # # Update the label every 10 seconds
        # def update_label(val):
        #     # current_time = str(datetime.datetime.now().time())
        #     # self._widget.inputFeedDataLabel_2.setText(current_time)
        #     for i in range(val):
        #         print(val)
        #         self._widget.inputFeedDataLabel_2.setText(str(i))
        #         if(i == 4):
        #             self._widget.inputFeedDataLabel_3.setText(str(i))
        #         time.sleep(3)


        # # timer = QtCore.QTimer()
        # # timer.timeout.connect(update_label)
        # # timer.start(10000)  # every 10,000 milliseconds
        # update_label(5)

        # def LongRunningTask():
        #     for i in range(4):
        #         print(i)
        #         self._widget.inputFeedDataLabel_2.setText(str(i))
        #         time.sleep(3)

        
        # thread = threading.Thread(LongRunningTask())
        # thread.start()

        # Create a QPushButton and a QLabel

        # button = QPushButton("CLICK ME")
        # label = QLabel("Hello world")

        # # Define a slot that updates the label's text when the button is clicked
        # def update_label_text():
        #     label.setText("Button clicked")

        # # Connect the button's "clicked" signal to the update_label_text slot
        # button.clicked.connect(update_label_text)

        # # Display the button and label in a window
        # button.show()
        # label.show()\

        
        # def func():
        #     for i in range(10):
        #         QApplication.processEvents()
        #         print(i)
        #         self._widget.inputFeedDataLabel_2.setText(str(i))
        #         time.sleep(3)
        #         print("func has been called!")

        # for i in range(10):
        #     print(i)
        #     self._widget.inputFeedDataLabel_2.setText(str(i))
        #     time.sleep(3)

        #     if i == 3:
        #         self._widget.inputFeedDataLabel_2.connect(func)

        
        self.init_subscriber()
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update_data)
        self._timer.start(1)  # Update every second

    def init_subscriber(self):
        self.temperature_list = []
        self.pressure_list = []
        self.altitude_list = []
        rospy.Subscriber('chatter', String, self.callback)  # subscribe to the test_topic topic
        # topicData = 0
    def callback(self, data):
        # self.temperature_list = data.temperature_list
        # self.pressure_list = data.pressure_list
        # self.altitude_list = data.altitude_list
        self.topicData = data 
        # self._widget.inputFeedDataLabel_2.setText(str(data))


    def update_data(self):
        self._widget.inputFeedDataLabel_2.adjustSize()
        self._widget.inputFeedDataLabel_2.setText(str(self.topicData))
        # self._widget.update_temperature(self.temperature_list)
    #     self._widget.update_pressure(self.pressure_list)
    #     self._widget.update_altitude(self.altitude_list)

            

        # QApplication.processEvents()
        # for i in range (1000000):
        #     if not i % 3:  # let application process events each 3 steps.
        #         QApplication.processEvents()
        #     # print("s")
        #     self._widget.inputFeedDataLabel_2.setText(str(i))


    # def shutdown_plugin(self):
    #     # TODO unregister all publishers here
    #     pass

    # def save_settings(self, plugin_settings, instance_settings):
    #     # TODO save intrinsic configuration, usually using:
    #     # instance_settings.set_value(k, v)
    #     pass

    # def restore_settings(self, plugin_settings, instance_settings):
    #     # TODO restore intrinsic configuration, usually using:
    #     # v = instance_settings.value(k)
    #     pass

    # #def trigger_configuration(self):
    #     # Comment in to signal that the plugin has a way to configure
    #     # This will enable a setting button (gear icon) in each dock widget title bar
    #     # Usually used to open a modal configuration dialog
