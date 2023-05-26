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
from std_msgs.msg import String, Int8

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

        # For updating the labels     
        self.init_subscriber()
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update_data)
        self._timer.start(1)  # Update every second

    def init_subscriber(self):
        self.temperature_list = []
        self.pressure_list = []
        self.altitude_list = []
        rospy.Subscriber('/robot_process', Int8, self.callback)  # subscribe to the topic you are looking for
        
    def callback(self, data):
        self.topicData = data 
        
    def update_data(self):
        # self._widget.inputFeedDataLabel_2.adjustSize()
        # self._widget.inputFeedDataLabel_2.setText(str(self.topicData))

        if self.topicData == 23: #driving mode #for now does nothing
            self._widget.labelForOngoingPhase.adjustSize()
            # self._widget.labelForOngoingPhase.setText(f"Driving Phase: {someting}")
            
        # if self.topicData == 21: #digging phase
        #     self._widget.inputSettingPhase.adjustSize()
        #     # self._widget.inputSettingPhase.setText("enterconfighere") #may not even be used..
        #     # self._widget.labelForOngoingPhase.setText(f"Digging Phase: {rospy.get_param("/ongoingDigPhase")}")
        #     self._widget.labelForOngoingPhase.setText(rospy.get_param("/ongoingDigPhase"))

        # if self.topicData == 23: #drive phase
        #     self._widget.inputSettingPhase.adjustSize()
        #     # self._widget.inputSettingPhase.setText("enterconfighere") #may not even be used..
        #     # self._widget.labelForOngoingPhase.setText(f"Digging Phase: {rospy.get_param("/ongoingDigPhase")}")
        #     self._widget.labelForOngoingPhase.setText(rospy.get_param("/ongoingDigPhase"))

        # Do i even need to look at the values from robot_process? The parameters from the config file change, but as a direct result of a button click..

        # Sol 1 : with 3 labels always present
        #self._widget.inputOngoingPhase.setText("Dig phase: {}". format(str(rospy.get_param("/ongoingDigPhase"))))

        # Sol 2 : only the label that is currently true will show, otherwise nothing

        # #Setting Phases- may or may not need:
        # if rospy.get_param("/settingDigPhase") == True:
        #     self._widget.inputSettingPhase.adjustSize()
        #     self._widget.inputSettingPhase.setText("Setting Dig mode phase: {}". format(str(rospy.get_param("/settingDigPhase"))))
        # elif rospy.get_param("/settingDepositPhase") == True:
        #     self._widget.inputSettingPhase.adjustSize()
        #     self._widget.inputSettingPhase.setText("Setting Deposit mode phase: {}". format(str(rospy.get_param("/settingDepositPhase"))))
        # elif rospy.get_param("/settingDriveModePhase") == True:
        #     self._widget.inputSettingPhase.adjustSize()
        #     self._widget.inputSettingPhase.setText("Setting Drive mode phase: {}". format(str(rospy.get_param("/settingDriveModePhase"))))
        # elif rospy.get_param("/settingNavigationDepositPhase") == True:
        #     self._widget.inputSettingPhase.adjustSize()
        #     self._widget.inputSettingPhase.setText("Setting Navigation to Deposit mode phase: {}". format(str(rospy.get_param("/settingNavigationDepositPhase"))))
        # elif rospy.get_param("/settingNavigationDigPhase") == True:
        #     self._widget.inputSettingPhase.adjustSize()
        #     self._widget.inputSettingPhase.setText("Setting Navigation to Dig mode phase: {}". format(str(rospy.get_param("/settingNavigationDigPhase"))))



        # #Ongoing Phases:
        # if rospy.get_param("/ongoingDigPhase") == True:
        #     self._widget.inputOngoingPhase.adjustSize()
        #     self._widget.inputOngoingPhase.setText("Dig mode phase: {}". format(str(rospy.get_param("/ongoingDigPhase"))))
        # elif rospy.get_param("/ongoingDriveModePhase") == True:
        #     self._widget.inputOngoingPhase.adjustSize()
        #     self._widget.inputOngoingPhase.setText("Drive mode phase: {}". format(str(rospy.get_param("/ongoingDriveModePhase"))))
        # elif rospy.get_param("/ongoingDepositPhase") == True:
        #     self._widget.inputOngoingPhase.adjustSize()
        #     self._widget.inputOngoingPhase.setText("Deposit mode phase: {}". format(str(rospy.get_param("/ongoingDepositPhase"))))

        # # Maybe's
        # # Localization
        # elif rospy.get_param("/localizationPhase") == True:
        #     self._widget.inputOngoingPhase.adjustSize()
        #     self._widget.inputOngoingPhase.setText("Localization mode phase: {}". format(str(rospy.get_param("/localizationPhase"))))
        # # Traversal to Deposit zone
        # elif rospy.get_param("/ongoingNavigationDepositPhase") == True:
        #     self._widget.inputOngoingPhase.adjustSize()
        #     self._widget.inputOngoingPhase.setText("Navigation to Deposit mode phase: {}". format(str(rospy.get_param("/ongoingNavigationDepositPhase"))))
        # # Traversal to Dig zone
        # elif rospy.get_param("/ongoingNavigationDigPhase") == True:
        #     self._widget.inputOngoingPhase.adjustSize()
        #     self._widget.inputOngoingPhase.setText("Navigation to Dig mode phase: {}". format(str(rospy.get_param("/ongoingNavigationDigPhase"))))
        
        # Info for manual mode
        self._widget.inputManualMode.adjustSize()
        self._widget.inputManualMode.setText(str(rospy.get_param("/manualMode")))

        
        #Info for Ballscrew parameter outputs
        #Speed output
        self._widget.inputBscrewVelocity.adjustSize()
        self._widget.inputBscrewVelocity.setText(str(rospy.get_param("/bscrew_cfg/motionCruiseVelocity")))
        self._widget.inputBscrewDownVelocity.adjustSize()
        #self._widget.inputBscrewDownVelocity.setText(str(rospy.get_param("/bscrew_cfg/motionCruiseVelocityDown")))

        #Percent output
        self._widget.inputBscrewPercent.adjustSize()
        self._widget.inputBscrewPercent.setText(str(rospy.get_param("/bscrew_cfg/percentOutput")))


        #Info for Linear Actuator parameter outputs
        #Speed output
        self._widget.inputLinActVelocity.adjustSize()
        self._widget.inputLinActVelocity.setText(str(rospy.get_param("/linact_cfg/motionCruiseVelocity")))

        #Percent output
        self._widget.inputLinActPercent.adjustSize()
        self._widget.inputLinActPercent.setText(str(rospy.get_param("/linact_cfg/percentOutput")))


        #Info for Trencher parameter outputs
        #Speed output
        self._widget.inputTrencherVelocity.adjustSize()
        self._widget.inputTrencherVelocity.setText(str(rospy.get_param("/trencher_cfg/motionCruiseVelocity")))

        #Percent output
        self._widget.inputTrencherPercent.adjustSize()
        self._widget.inputTrencherPercent.setText(str(rospy.get_param("/trencher_cfg/percentOutput")))


        #Info for Bucket parameter outputs
        #Speed output
        self._widget.inputBucketVelocity.adjustSize()
        self._widget.inputBucketVelocity.setText(str(rospy.get_param("/bucket_cfg/motionCruiseVelocity")))

        #Percent output
        self._widget.inputBucketPercent.adjustSize()
        self._widget.inputBucketPercent.setText(str(rospy.get_param("/bucket_cfg/percentOutput")))


        #Info for Wheel parameter outputs
        #Speed output
        self._widget.inputWheelVelocity.adjustSize()
        self._widget.inputWheelVelocity.setText(str(rospy.get_param("/wheel_cfg/motionCruiseVelocity")))

        #Percent output
        self._widget.inputWheelPercent.adjustSize()
        self._widget.inputWheelPercent.setText(str(rospy.get_param("/wheel_cfg/percentOutput")))



        # @TODO: Notes.. Ignore if not relevant
        # @TODO: get the labels updated with the parameters, see if the params are even being updated - done - they should be
        # @TODO: where is the params even changing?? May need to edit a param to add the driving thing - the params change - looks like only 3 do for now (ongoing Dig,Dep, and manualMode..)
        # @TODO: Can go a few ways, we can just show the current phase that is true, show all the phases and show if true or false - currently only shows the phase running

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

