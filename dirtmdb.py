import os
import glob
import re
import argparse
import xml.etree.ElementTree as ET


def uselessFile(entryName):
    return entryName in ['@eaDir', '.DS_Store', '.@__thumb']


def rename_dirs_with_tmdb(root_dir):
    for index, dirname in enumerate(os.listdir(root_dir)):
        if uselessFile(dirname):
            continue

        dirpath = os.path.join(root_dir, dirname)
        if os.path.isdir(dirpath):
            nfo_found = False
            for subfile in os.listdir(dirpath):
                if os.path.isdir(os.path.join(dirpath, subfile)):
                    # print(f"{subfile} skip")
                    continue

                if subfile.endswith('.nfo'):
                    nfo_path = os.path.join(dirpath, subfile)

                    tree = ET.parse(nfo_path)
                    root = tree.getroot()

                    # 查找根节点中的 <tmdb> 标识
                    tmdb_elem = root.find('tmdbid')
                    if tmdb_elem is not None:
                        nfo_found = True
                        tmdb_id = tmdb_elem.text
                        original_dirname = os.path.basename(dirpath)
                        if not re.search(r'tmdb-\d+', original_dirname, re.I):
                            new_dirname = f"{original_dirname} {{tmdb-{tmdb_id}}}"
                            new_dirpath = os.path.join(
                                os.path.dirname(dirpath), new_dirname)
                            print(f"{index} : {original_dirname} ==> {new_dirname}")
                            os.rename(dirpath, new_dirpath)
                        else:
                            print(f"{index} : {original_dirname} skip")
                        break
            if not nfo_found:
                thedirname = os.path.basename(dirpath)
                print(f"{index} : {thedirname} .nfo file not found")


def rename_movie_dirs_with_tmdb(root_dir):
    for index, dirname in enumerate(os.listdir(root_dir)):
        if uselessFile(dirname):
            continue

        dirpath = os.path.join(root_dir, dirname)
        if os.path.isdir(dirpath):
            nfo_found = False
            for subfile in os.listdir(dirpath):
                if os.path.isdir(os.path.join(dirpath, subfile)):
                    # print(f"{subfile} skip")
                    continue

                if subfile.endswith('.nfo'):
                    nfo_path = os.path.join(dirpath, subfile)
                    with open(nfo_path, 'r') as f:
                        nfo_content = f.read()
                    match = re.search(
                        r'<uniqueid.*type="tmdb".*>([0-9]+)</uniqueid>', nfo_content)
                    if match:
                        nfo_found = True
                        tmdb_id = match.group(1)
                        original_dirname = os.path.basename(dirpath)
                        if not re.search(r'tmdb-\d+', original_dirname, re.I):
                            new_dirname = f"{original_dirname} {{tmdb-{tmdb_id}}}"
                            new_dirpath = os.path.join(
                                os.path.dirname(dirpath), new_dirname)
                            print(f"{index} : {original_dirname} ==> {new_dirname}")
                            os.rename(dirpath, new_dirpath)
                        else:
                            print(f"{index} : {original_dirname} skip")
                        break
            if not nfo_found:
                thedirname = os.path.basename(dirpath)
                print(f"{index} : {thedirname} .nfo file not found")


def loadArgs():
    global ARGS
    parser = argparse.ArgumentParser(description='rename folder with tmdbid.')
    parser.add_argument('dir', help='folder path.')
    ARGS = parser.parse_args()
    ARGS.dir = os.path.expanduser(ARGS.dir)


def main():
    loadArgs()
    rename_dirs_with_tmdb(ARGS.dir)


if __name__ == '__main__':
    main()
