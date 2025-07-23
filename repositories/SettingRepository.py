from models.Setting import Setting
from database import db

class SettingRepository:

    # GETTERS
    @staticmethod
    def get_debug():
        setting = Setting.query.filter(Setting.data=="debug").first()
        return setting.state if setting else None

    @staticmethod
    def get_offset_a():
        setting = Setting.query.filter(Setting.data=="offset_a").first()
        return setting.state if setting else None

    @staticmethod
    def get_offset_b():
        setting = Setting.query.filter(Setting.data=="offset_b").first()
        return setting.state if setting else None

    @staticmethod
    def get_offset_c():
        setting = Setting.query.filter(Setting.data=="offset_c").first()
        return setting.state if setting else None

    @staticmethod
    def get_number_scratch_m():
        setting = Setting.query.filter(Setting.data=="number_scratch_m").first()
        return setting.state if setting else None

    @staticmethod
    def get_number_scratch_f():
        setting = Setting.query.filter(Setting.data=="number_scratch_f").first()
        return setting.state if setting else None

    @staticmethod
    def get_debug_channel():
        setting = Setting.query.filter(Setting.data=="debug_channel").first()
        return setting.state if setting else None

    # SETTERS
    @staticmethod
    def set_debug(number):
        setting = Setting.query.filter(Setting.data=="debug").first()
        if setting:
            setting.state = number
        else:
            setting = Setting("debug", number)
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def set_offset_a(number):
        setting = Setting.query.filter(Setting.data=="offset_a").first()
        if setting:
            setting.state = number
        else:
            setting = Setting("offset_a", number)
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def set_offset_b(number):
        setting = Setting.query.filter(Setting.data=="offset_b").first()
        if setting:
            setting.state = number
        else:
            setting = Setting("offset_b", number)
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def set_offset_c(number):
        setting = Setting.query.filter(Setting.data=="offset_c").first()
        if setting:
            setting.state = number
        else:
            setting = Setting("offset_c", number)
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def set_number_scratch_m(number):
        setting = Setting.query.filter(Setting.data=="number_scratch_m").first()
        if setting:
            setting.state = number
        else:
            setting = Setting("number_scratch_m", number)
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def set_number_scratch_f(number):
        setting = Setting.query.filter(Setting.data=="number_scratch_f").first()
        if setting:
            setting.state = number
        else:
            setting = Setting("number_scratch_f", number)
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def set_debug_channel(value):
        setting = Setting.query.filter(Setting.data=="debug_channel").first()
        if setting:
            setting.state = value
        else:
            setting = Setting("debug_channel", value)
        db.session.add(setting)
        db.session.commit()