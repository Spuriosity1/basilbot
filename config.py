import json
import sys
import os.path
import os

CONFIG_PATH = '/home/pi/basilbot_config.json'
DEFAULT_PATH = '/home/pi/basilbot/template.basilbot_config.json'

config = {}

try:
    with open(CONFIG_PATH,'r') as f:
        config = json.load(f)
        if not config['auto_measure']['active']:
            sys.exit(0)
except FileNotFoundError:
    print('No config file found at %s. Using defaults file at %s...' % (CONFIG_PATH, DEFAULT_PATH))
    try:
        with open(DEFAULT_PATH,'r') as f:
            config = json.load(f)
            if not cfg['auto_measure']['active']:
                sys.exit(0)
    except FileNotFoundError:
        print('No defualt config file found at %s either. Giving up.' % DEFAULT_PATH)
        sys.exit(1)

def ask_bool(msg, dflt=True):
    msg += ' (y) :' if dflt else ' (n) :'
    res = input(msg)
    return True if len(res) == 0 or res.lower()[0]=='y' else False

def ask_num(msg, dflt=0,typ=int):
    retval = None
    while retval is None:
        res = input(msg+ ' ({}) :'.format(dflt))
        if len(res) == 0:
            return dflt
        try:
            retval = typ(res)
        except ValueError:
            print("Invalid number specification.")
    return retval

def dinput(msg, dflt):
    ans = input(msg)
    return ans if len(ans)>0 else dflt

def generate():
    raise NotImplementedError
    print('Generating new config file... (Ctrl-D to exit)')

    # Automatic measurement
    config['auto_measure'] = {}
    config['auto_measure']['active'] = ask_bool('Enable automatic (hourly) moisture logging?')
    config['auto_measure']['num_samples'] = ask_num('Enter number of readings to take in each hourly measurement',10)

    # Automatic watering
    config['auto_water']={}
    config['auto_water']['active'] = ask_bool('Enable automatic (hourly) watering?', False)
    t = ask_num('Enter target moisture percentage', 70, float)
    # if the user really feels strongly about these, they can change them their damn self in the JSON
    config['auto_water']['thresholds'] = {"high": t+10,"target": t,"low": t-15,"critical": t-30}
    config['webhooks']=[input('Enter a webhook for reminders to be sent to: ')]

    config['man_water']={}
    config['man_water']['max_moisture'] = t+10
    config['man_water']['max_runtime'] = 60

    config['messages'] = {}
    config['messages']['low_moisture'] = "Soil's moisture content is low."
    save()
    print('Done!')

def save():
    with open(CONFIG_PATH,'w') as f:
        json.dump(config, f)

def traverse():
    return(r_traverse(config)+'\n')

def r_traverse(x, depth=0):
    s = ''
    if type(x) is dict:
        for entry in x:
            s += '\n'+'  '*depth + entry + ': ' + r_traverse(x[entry], depth + 1)
    elif type(x) is list:
        for entry in x:
            s += '\n'+'  '*depth + r_traverse(entry, depth + 1)
    else:
        return str(x)
    return s
