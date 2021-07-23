import os
import sys
import time
import datetime
import mimetypes
import chardet

help = '\nHELP: lss --help\n\nlss:\n    Syntax:\n        "lss" : finds and lists the files and dirs on the current working dir\n                Example:\n                    ""C:/current/dir"\n                      name:           \ttype:           \tmodified:       \tsize:           \tmimetype:       \tencoding:\n                      .\test          \td--             \t2021-07-21-10:09\t4096            \t-               \t-\n                      .\test.json       -f-             \t2021-07-21-10:09\t1               \tapplication/json  ?\n                      .\file          \t--u             \t2021-07-21-10:09\t0               \t-               \t-\n        "lss", "--help" : sends the user this message and returns main()\n                Example:\n                    HELP: lss --help...\n\n        "lss", "--n" : does the same thing but uses newlines to narrow the print (best for small consoles)\n                Example:\n                    "C:/current/dir"\n                    name:        .\\Python\n                    type:        d--\n                    modified:    2021-07-21-10:09\n                    size:        4096\n                    mimetype:    -\n                    encoding:\t   -\n\n        "lss", "--info" : (at its presence "--n" is ignored) gives not so noob friendly information about the current file/dir\n                Example:\n                    .\test\n                    os.stat_result(st_mode=0000, st_ino=0000, st_dev=0000, st_nlink=0000, st_uid=0000, st_gid=0000, st_size=0000, st_atime=0000, st_mtime=0000, st_ctime=0000)\n\n        "lss", "C:another\\dir" | "--n" : finds and lists the files and dirs on the given dir using the given commands\n                Example:\n                    "C:/given/dir"\n                    name:           \ttype:           \tmodified:       \tsize:           \tmimetype:       \tencoding:\n                    .\test          \td--             \t2021-07-21-10:09\t0               \t-               \t-\n\n    Errors:\n        raise SyntaxError(\'"{dir}" is not a valid directory...\') is the only error raised, stick to the syntax and you should be fine\n\n    Output Syntax:\n        "lss" | "--n" | "C:another\\dir" :\n\n            name : gives the file or dir\'s name\n                    Example:\n                        name:        .\test\n\n            type : gives the type of the object:\n                    Example:\n                        type:        d--\n\n                d-- : object is a dir\n\n                -f- : object is a file\n\n                --u : object is unknown (sign that something terrible happend)\n\n            modified : gives the date the object was last modified\n                    Example:\n                        modified:    2021-07-21-10:09\n\n            size : gives the size of the object in bytes\n                    Example:\n                        size:        4096\n\n            mimetype : gives the file (extension | mime) if the extension was found, else \'?\'\n                    Example: extension\n                        mimetype:       .json\n                    Example 1: mime\n                        mimetype:       application/json\n                    Example 2: extension was not found\n                        mimetype:       ?\n                    Example 3: is dir\n                        mimetype:       -\n\n            encoding : gives the files encoding if it finds it\n                    Example: encoding\n                        encoding:       utf-8\n                    Example 1: encoding not found\n                        encoding:       ?\n                    Example 2: is dir\n                        encoding:       -\n\n        "lss", "--info" : good luck\n\n            ST_MODE : Inode protection mode.\n\n            ST_INO : Inode number.\n\n            ST_DEV : Device inode resides on.\n\n            ST_NLINK : Number of links to the inode.\n\n            ST_UID : User id of the owner.\n\n            ST_GID : Group id of the owner.\n\n            ST_SIZE : Size in bytes of a plain file; amount of data waiting on some special files.\n\n            ST_ATIME : Time of last access.\n\n            ST_MTIME : Time of last modification.\n\n            ST_CTIME : The “ctime” as reported by the operating system. On some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time (see platform documentation for details).\n'
class Lss:
    def __init__(self, path) -> None:
        attributes = self.get_attributes(path)
        self.type = attributes[0]
        self.name = attributes[1]
        self.size = str(attributes[2])
        self.modified = attributes[3]
        self.mimetype = attributes[4]
        self.encoding = attributes[5]
        self.info = attributes[6]
    def __str__(self):
        return 

    def predict_encoding(self, file_path, n_lines=20):
        # predicts file encoding and returns a p if PermissionError 
        try:
            with open(file_path, 'rb') as f:
                rawdata = b''.join([f.readline() for _ in range(n_lines)])
        except PermissionError:
            return ('?', 'p')
        except:
            return ('?', '-')
        return (chardet.detect(rawdata)['encoding'], '-') if (chardet.detect(rawdata)['encoding'], '-') != None else ('?', '-')

    def get_dir_size(self, start_path = '.'):
        # returns directory's size
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            if dirnames:
                pass
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link 
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size

    def get_attributes(self, path):
        # return the file atributes
        if os.path.isdir(path):
            link = 'l' if os.path.islink(path) else '-'
            name = ('.\\'+path if len(path) <= 14 else '.\\'+path[:14]+'...')
            stat = os.stat(path)
            size = self.get_dir_size(path)
            modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d-%H:%M')
            mimetype = '-'
            encoding = '-'
            return (f'd-{link}--', name, size, modified, mimetype, encoding, stat)

        elif os.path.isfile(path):
            link = 'l' if os.path.islink(path) else '-'
            name = ('.\\'+path if len(path) <= 14 else '.\\'+path[:14]+'...')
            stat = os.stat(path)
            size = stat.st_size
            modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d-%H:%M')
            mimetype = '?' if (os.path.splitext(path)[1] if mimetypes.guess_type(path, strict=False)[0] == None else mimetypes.guess_type(path, strict=False)[0]) == '' else (os.path.splitext(path)[1] if mimetypes.guess_type(path, strict=False)[0] == None else mimetypes.guess_type(path, strict=False)[0])
            encoding = self.predict_encoding(path)
            return (f'-f{link}{encoding[1]}-', name, size, modified, mimetype, encoding[0], stat)
        else:
            link = 'l' if os.path.islink(path) else '-'
            name = ('.\\'+path if len(path) <= 14 else '.\\'+path[:14]+'...')
            stat = os.stat(path)
            size = stat.st_size
            modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d-%H:%M')
            try:
                mimetype = '?' if (os.path.splitext(path)[1] if mimetypes.guess_type(path, strict=False)[0] == None else mimetypes.guess_type(path, strict=False)[0]) == '' else (os.path.splitext(path)[1] if mimetypes.guess_type(path, strict=False)[0] == None else mimetypes.guess_type(path, strict=False)[0])
            except:
                mimetype = '-'
            encoding = self.predict_encoding(path)
            return (f'--{link}{encoding[1]}u', name, size, modified, mimetype, encoding[0], stat)
        return

# -----
# dflpu # d = dir, f = file, l = link, p = permission, u = unkown

def print_resolver(path, newl, info, file_, name_):
    # just use ls mate
    if name_:
        if newl:
            for f in os.listdir(path):
                obj = Lss(f)
                print(obj.name)
        else:       
            for f in os.listdir(path):
                obj = Lss(f)
                sys.stdout.flush()
                print(obj.name, end = '\t')
        return
        
    # just one file
    if file_:
        # just one file using info
        obj = Lss(path)
        if info:
            print(f'{obj.name}\n{obj.info}')
            return
        big = 16
        print('name:'.ljust(big), 'type:'.ljust(big), 'modified:'.ljust(big), 'size:'.ljust(big), 'mimetype:'.ljust(big),'encoding:'.ljust(big), sep='\t')
        print(obj.name.ljust(big), obj.type.ljust(big), obj.modified.ljust(big), obj.size.ljust(big), obj.mimetype.ljust(big), obj.encoding.ljust(big), sep='\t')
        return
    # using info
    if info:
        for f in os.listdir(path):
            obj = Lss(f)
            print('\n')
            print(obj.name, obj, sep='\n')
        return
    # using newlines 
    big = 16
    if newl:
        for f in os.listdir(path):
            obj = Lss(f)
            print('\n')
            print('name:\t\t'+obj.name, 'type:\t\t'+obj.type, 'modified:\t'+obj.modified, 'size:\t\t'+obj.size, 'mimetype:\t'+obj.mimetype,'encoding:\t'+obj.encoding, sep='\n')
        return
    # normal print
    
    print('name:'.ljust(big), 'type:'.ljust(big), 'modified:'.ljust(big), 'size:'.ljust(big), 'mimetype:'.ljust(big),'encoding:'.ljust(big), sep='\t')
    for f in os.listdir(path):
        obj = Lss(f)
        print(obj.name.ljust(big), obj.type.ljust(big), obj.modified.ljust(big), obj.size.ljust(big), obj.mimetype.ljust(big), obj.encoding.ljust(big), sep='\t')
    return


def main():
    print('')
    args = sys.argv
    newl = False
    info = False
    name_ = False
    file_ = False
    path = r''+os.getcwd()
    os.chdir(path)
    for arg in args[1::]:
        if arg == '-n':
            newl = True
        elif arg == '-name':
            name_ = True
        elif arg == '-info':
            info = True
        elif os.path.isdir(arg):
            path = arg
            os.chdir(path)
        elif os.path.isfile(arg):
            file_ = True
            path = arg
            os.chdir(path)
        else:
            raise SyntaxError(f'command syntax incorrect, error detected here: "{arg}"')
    print_resolver(path=path, newl=newl, info=info, file_=file_, name_=name_)
    return


if __name__ == '__main__':
    main()


try:
    sys.exit(0)
except SystemExit:
    os._exit(0)
