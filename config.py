import json
import sys

CONFIG_PATH = '../basilbot_config.json'
DEFAULT_PATH = 'template.basilbot_config.json'

config = {}

try:
    with open(CONFIG_PATH,'r') as f:
        config = json.load(f)
        if not config['auto_measure']['active']:
            sys.exit(0)
except FileNotFoundError:
    print('No config file found at %s. Using defaults...' % CONFIG_PATH)
    try:
        with open(CONFIG_PATH,'r') as f:
            config = json.load(f)
            if not cfg['auto_measure']['active']:
                sys.exit(0)
    except FileNotFoundError:
        print('No defualt config file found at %s either. Giving up.' % DEFAULT_PATH)

def ask_bool(msg,dflt=True):
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

def generate():
    print('Generating new config file... (Ctrl-D to exit)')
    print('Automatic measurement')
    config['auto_measure'] = {}
    config['auto_measure']['active'] = ask_bool('Enable automatic (hourly) moisture logging?')
    config['auto_measure']['num_samples'] = ask_num('Enter number of readings to take in each hourly measurement',10)

    print('Automatic watering')
    config['auto_water']={}
    config['auto_water']['active'] = ask_bool('Enable automatic (hourly) watering?', False)
    t = ask_num('Enter target moisture percentage', 75,float)
    # if the user really feels strongly about these, they can change them their damn self
    config['auto_water']['thresholds'] = {"high": t+10,"target": t,"low": t-15,"critical": t-30}
    config['webhooks']=[input('Enter a webhook for reminders to be sent to: ')]
    with open(CONFIG_PATH,'w') as f:
        json.dump(config, f)
    print('Done!')
