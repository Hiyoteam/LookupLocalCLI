from utils import *
def main(connection,args):
    results=query(connection,args)
    for msg in results:
        print(format_message(msg))
plugin={
    "name":"sql",
    "info":"Execute a SQL query on the database",
    "required_version":(1,0,0),
    "main":main
}