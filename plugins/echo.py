from utils import *
def main(connection,args):
    print(args)

plugin={
    "name":"echo",
    "info":"Echoes the input",
    "required_version":(1,0,0),
    "main":main
}