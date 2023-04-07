import os
import glob
import re
import argparse

def uselessFile(entryName):
    return entryName in ['@eaDir', '.DS_Store', '.@__thumb']

def rename_dirs_with_tmdb_info(root_dir):
    for index, dirname in enumerate(os.listdir(root_dir)):
        if uselessFile(dirname):
            continue

        dirpath = os.path.join(root_dir, dirname)
        if os.path.isdir(dirpath):
            for subfile in os.listdir(dirpath):
                if subfile.endswith('.nfo'):
                    nfo_path = os.path.join(dirpath, subfile)
                    with open(nfo_path, 'r') as f:
                        nfo_content = f.read()
                    match = re.search(r'<uniqueid.*type="tmdb">([0-9]+)</uniqueid>', nfo_content)
                    if match:
                        tmdb_id = match.group(1)
                        original_dirname = os.path.basename(dirpath)
                        new_dirname = f"{original_dirname} {{tmdb-{tmdb_id}}}"
                        new_dirpath = os.path.join(os.path.dirname(dirpath), new_dirname)
                        os.rename(dirpath, new_dirpath)


def loadArgs():
    global ARGS
    parser = argparse.ArgumentParser(description='rename folder with tmdbid.')
    parser.add_argument('dir', help='folder path.')
    ARGS = parser.parse_args()
    ARGS.dir = os.path.expanduser(ARGS.dir)


def main():
    loadArgs()
    rename_dirs_with_tmdb_info(ARGS.dir)


if __name__ == '__main__':
    main()