from easysettings import EasySettings


def set(name, object=None):
    global settings
    settings.set(name, object)
    settings.save()


def get(name):
    global settings
    global defaults
    s = settings.get(name)
    if s == '' and name in defaults:
        return defaults[name]
    return s


settings = EasySettings("settings.conf")

defaults = {
    'recents': []
}


def checkDefaults():
    global settings
    global defaults
    for i in defaults:
        s = settings.get(i)
        if s == '':
            settings.set(i, defaults[i])

    settings.save()


checkDefaults()
