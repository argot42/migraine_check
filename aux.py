import sys

def do_you_want_to_continue_bb(fun, prompt='Otra?'):
    ''' High order function to ask if you want to continue to execute the given function '''

    if sys.stdin.isatty():
        pt = {'continue': "{} [y/n]: ".format(prompt)}
    else:
        pt = {'continue': ''}

    while True:
        fun()
        if input(pt['continue']) in ['y', 'yes']: continue
        exit() 
