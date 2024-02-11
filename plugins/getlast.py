from utils import *
def main(connection,args):
    results=query(connection,f"SELECT * FROM chat ORDER BY id DESC LIMIT {args};")
    results.reverse()
    for msg in results:
        print(format_message(msg))
plugin={
    "name":"getlast",
    "info":"Get the last n messages from the database",
    "required_version":(1,0,0),
    "main":main
}