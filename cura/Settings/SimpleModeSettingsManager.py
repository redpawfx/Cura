# Copyright (c) 2017 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty

from UM.Application import Application


class SimpleModeSettingsManager(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)

        self._machine_manager = Application.getInstance().getMachineManager()
        self._is_profile_customized = False

        self._machine_manager.activeStackValueChanged.connect(self._updateIsProfileCustomized)

    isProfileCustomizedChanged = pyqtSignal()

    @pyqtProperty(bool, notify = isProfileCustomizedChanged)
    def isProfileCustomized(self):
        return self._is_profile_customized

    def _updateIsProfileCustomized(self):
        user_setting_keys = set()

        if not self._machine_manager.activeMachine:
            return False

        global_stack = self._machine_manager.activeMachine

        # check user settings in the global stack
        user_setting_keys.update(set(global_stack.userChanges.getAllKeys()))
        # check user settings in the extruder stacks
        if global_stack.extruders:
            for extruder_stack in global_stack.extruders.values():
                user_setting_keys.update(set(extruder_stack.userChanges.getAllKeys()))

        for skip_key in self.__ignored_custom_setting_keys:
            if skip_key in user_setting_keys:
                user_setting_keys.remove(skip_key)

        has_customized_user_settings = len(user_setting_keys) > 0

        if has_customized_user_settings != self._is_profile_customized:
            self._is_profile_customized = has_customized_user_settings
            self.isProfileCustomizedChanged.emit()

    # A list of settings that will be ignored when check whether there is any custom settings.
    __ignored_custom_setting_keys = ["support_enable",
                                     "infill_sparse_density",
                                     "gradual_infill_steps",
                                     "adhesion_type",
                                     "support_extruder_nr"]
