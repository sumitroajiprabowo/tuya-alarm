"""
Constants and Presets for Tuya Alarm Control
"""

class VolumeLevel:
    """Alarm volume levels"""
    MUTE = 'mute'
    LOW = 'low'
    MIDDLE = 'middle'
    HIGH = 'high'

    @classmethod
    def all(cls):
        """Return all available volume levels"""
        return [cls.MUTE, cls.LOW, cls.MIDDLE, cls.HIGH]


class BrightnessLevel:
    """Brightness levels"""
    LOW = 'low'
    MIDDLE = 'middle'
    HIGH = 'high'
    STRONG = 'strong'

    @classmethod
    def all(cls):
        """Return all available brightness levels"""
        return [cls.LOW, cls.MIDDLE, cls.HIGH, cls.STRONG]


class MasterMode:
    """Master mode options"""
    DISARMED = 'disarmed'
    ARM = 'arm'
    HOME = 'home'
    SOS = 'sos'
    WORK = 'work'
    PLAY = 'play'

    @classmethod
    def all(cls):
        """Return all available master modes"""
        return [cls.DISARMED, cls.ARM, cls.HOME, cls.SOS, cls.WORK, cls.PLAY]


class AlarmState:
    """Alarm state options"""
    NORMAL = 'normal'
    ALARM_SOUND = 'alarm_sound'
    ALARM_LIGHT = 'alarm_light'
    ALARM_SOUND_LIGHT = 'alarm_sound_light'


class CommandCode:
    """Tuya command codes"""
    ALARM_SWITCH = 'alarm_switch'
    ALERT_STATE = 'alert_state'
    ALARM_STATE = 'alarm_state'
    ALARM_VOLUME = 'alarm_volume'
    BRIGHT_STATE = 'bright_state'
    MASTER_MODE = 'master_mode'
    ALARM_TIME = 'alarm_time'
    
    # Read-only status codes
    BATTERY_PERCENTAGE = 'battery_percentage'
    BATTERY_VALUE = 'battery_value'
    BATTERY_STATE = 'battery_state'
    CHARGE_STATE = 'charge_state'
    CHECKING_RESULT = 'checking_result'
    PREHEAT = 'preheat'
    LIFECYCLE = 'lifecycle'
    TEMPER_ALARM = 'temper_alarm'


# Predefined alarm presets
ALARM_PRESETS = {
    'home': [
        {'code': CommandCode.MASTER_MODE, 'value': MasterMode.HOME},
        {'code': CommandCode.ALERT_STATE, 'value': True},
        {'code': CommandCode.ALARM_VOLUME, 'value': VolumeLevel.MIDDLE},
        {'code': CommandCode.BRIGHT_STATE, 'value': BrightnessLevel.MIDDLE}
    ],
    'away': [
        {'code': CommandCode.MASTER_MODE, 'value': MasterMode.ARM},
        {'code': CommandCode.ALERT_STATE, 'value': True},
        {'code': CommandCode.ALARM_SWITCH, 'value': True},
        {'code': CommandCode.ALARM_VOLUME, 'value': VolumeLevel.HIGH},
        {'code': CommandCode.BRIGHT_STATE, 'value': BrightnessLevel.STRONG}
    ],
    'night': [
        {'code': CommandCode.MASTER_MODE, 'value': MasterMode.HOME},
        {'code': CommandCode.ALARM_VOLUME, 'value': VolumeLevel.LOW},
        {'code': CommandCode.BRIGHT_STATE, 'value': BrightnessLevel.LOW}
    ],
    'silent': [
        {'code': CommandCode.ALARM_VOLUME, 'value': VolumeLevel.MUTE},
        {'code': CommandCode.ALARM_STATE, 'value': AlarmState.ALARM_LIGHT},
        {'code': CommandCode.BRIGHT_STATE, 'value': BrightnessLevel.MIDDLE}
    ],
    'test': [
        {'code': CommandCode.ALARM_STATE, 'value': AlarmState.ALARM_SOUND},
        {'code': CommandCode.ALARM_VOLUME, 'value': VolumeLevel.LOW},
        {'code': CommandCode.ALARM_TIME, 'value': 5}
    ]
}


# Emergency alarm activation commands
EMERGENCY_ALARM_COMMANDS = [
    {'code': CommandCode.ALARM_SWITCH, 'value': True},
    {'code': CommandCode.ALERT_STATE, 'value': True},
    {'code': CommandCode.ALARM_STATE, 'value': AlarmState.ALARM_SOUND_LIGHT},
    {'code': CommandCode.ALARM_VOLUME, 'value': VolumeLevel.HIGH},
    {'code': CommandCode.BRIGHT_STATE, 'value': BrightnessLevel.STRONG},
    {'code': CommandCode.MASTER_MODE, 'value': MasterMode.SOS}
]

# Time to work alarm
TIME_TO_WORK_COMMANDS = [
    {'code': CommandCode.ALARM_SWITCH, 'value': True},
    {'code': CommandCode.ALERT_STATE, 'value': True},
    {'code': CommandCode.ALARM_STATE, 'value': AlarmState.ALARM_SOUND_LIGHT},
    {'code': CommandCode.ALARM_VOLUME, 'value': VolumeLevel.MIDDLE},
    {'code': CommandCode.ALARM_TIME, 'value': 3},
    {'code': CommandCode.BRIGHT_STATE, 'value': BrightnessLevel.STRONG},
    {'code': CommandCode.MASTER_MODE, 'value': MasterMode.SOS}
]


# Alarm deactivation commands
DEACTIVATE_ALARM_COMMANDS = [
    {'code': CommandCode.ALARM_SWITCH, 'value': False},
    {'code': CommandCode.ALERT_STATE, 'value': False},
    {'code': CommandCode.ALARM_STATE, 'value': AlarmState.NORMAL},
    {'code': CommandCode.MASTER_MODE, 'value': MasterMode.DISARMED}
]