import os
import glob
import re
import argparse
import xml.etree.ElementTree as ET


def uselessFile(entryName):
    return entryName in ['@eaDir', '.DS_Store', '.@__thumb']


def rename_dirs_with_tmdb(root_dir):
    if ARGS.success_list:
        fo = open(ARGS.success_list, "w", encoding='utf-8')
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
                    if not os.path.isfile(nfo_path):
                        continue
                    
                    tmdb_elem = None
                    try:
                        tree = ET.parse(nfo_path)
                        root = tree.getroot()
                        # 查找根节点中的 <tmdbid> 标识
                        tmdb_elem = root.find('tmdbid')
                        # 查找根节点中的 <title> 标识
                        title_elem = root.find('title')
                        # 查找根节点中的 <year> 标识
                        year_elem = root.find('year')
                    except:
                        continue

                    if tmdb_elem is not None:
                        nfo_found = True
                        tmdb_id = tmdb_elem.text
                        original_dirname = os.path.basename(dirpath)
                        original_dirname = re.sub(r'\{tmdb-\d+\}', '', original_dirname, re.I)
                        original_dirname = re.sub(r'\{imdb-tt\d+\}', '', original_dirname, re.I)
                        newdir_basename = original_dirname
                        if title_elem is not None and year_elem is not None:
                            newdir_basename = f"{title_elem.text} ({year_elem.text})"

                        new_dirname = f"{newdir_basename} {{tmdb-{tmdb_id}}}"
                        new_dirpath = os.path.join( os.path.dirname(dirpath), new_dirname)
                        print(f"{index} : {newdir_basename} ==> {new_dirname}")
                        # m = re.search(r'tmdb-\d+', original_dirname, re.I)
                        # if not m:
                        #     new_dirname = f"{newdir_basename} {{tmdb-{tmdb_id}}}"
                        #     new_dirpath = os.path.join( os.path.dirname(dirpath), new_dirname)
                        #     print(f"{index} : {newdir_basename} ==> {new_dirname}")
                        #     # os.rename(dirpath, new_dirpath)
                        # else:
                        #     # print(f"{index} : {original_dirname} origin TMDb name.")
                        #     new_dirname =  original_dirname.replace(m.group(0), f"tmdb-{tmdb_id}")
                        #     new_dirpath = os.path.join( os.path.dirname(dirpath), new_dirname)
                        #     print(f"{index} : {original_dirname} ==> {new_dirname}")
                        if os.path.exists(new_dirpath):
                            print(f"{new_dirpath} exists, skip")
                            break
                        try:
                            os.rename(dirpath, new_dirpath)
                        except:
                            print("rename exception")
                        if ARGS.success_list:
                            fo.write( new_dirname + os.linesep )

                        break
            if not nfo_found:
                thedirname = os.path.basename(dirpath)
                print(f"{index} : {thedirname} .nfo file not found")

    if ARGS.success_list:
        fo.close()


def rename_dirs_with_imdb(root_dir):
    if ARGS.success_list:
        fo = open(ARGS.success_list, "w", encoding='utf-8')
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
                    if not os.path.isfile(nfo_path):
                        continue
                    
                    imdb_elem = None
                    try:
                        tree = ET.parse(nfo_path)
                        root = tree.getroot()
                        # 查找根节点中的 <tmdbid> 标识
                        imdb_elem = root.find('imdbid')
                        # if (imdb_elem.text is None):
                        #     imdb_elem = root.find('uniqueid')
                        # 查找根节点中的 <title> 标识
                        title_elem = root.find('title')
                        # 查找根节点中的 <year> 标识
                        year_elem = root.find('year')
                    except:
                        continue

                    if imdb_elem is not None and imdb_elem.text is not None:
                        nfo_found = True
                        tmdb_id = imdb_elem.text
                        original_dirname = os.path.basename(dirpath)
                        original_dirname = re.sub(r'\{tmdb-\d+\}', '', original_dirname, re.I)
                        original_dirname = re.sub(r'\{imdb-tt\d+\}', '', original_dirname, re.I)
                        newdir_basename = original_dirname
                        if title_elem is not None and year_elem is not None:
                            newdir_basename = f"{title_elem.text} ({year_elem.text})"

                        new_dirname = f"{newdir_basename} {{tmdb-{tmdb_id}}}"
                        new_dirpath = os.path.join( os.path.dirname(dirpath), new_dirname)
                        print(f"{index} : {newdir_basename} ==> {new_dirname}")
                        # m = re.search(r'imdb-tt\d+', original_dirname, re.I)
                        # if not m:
                        #     new_dirname = f"{newdir_basename} {{imdb-{tmdb_id}}}"
                        #     new_dirpath = os.path.join( os.path.dirname(dirpath), new_dirname)
                        #     print(f"{index} : {newdir_basename} ==> {new_dirname}")
                        #     # os.rename(dirpath, new_dirpath)
                        # else:
                        #     # print(f"{index} : {original_dirname} origin TMDb name.")
                        #     new_dirname =  original_dirname.replace(m.group(0), f"imdb-{tmdb_id}")
                        #     new_dirpath = os.path.join( os.path.dirname(dirpath), new_dirname)
                        #     print(f"{index} : {original_dirname} ==> {new_dirname}")
                        if os.path.exists(new_dirpath):
                            print(f"{new_dirpath} exists, skip")
                            break
                        try:
                            os.rename(dirpath, new_dirpath)
                        except:
                            print("rename exception")
                        if ARGS.success_list:
                            fo.write( new_dirname + os.linesep )

                        break
            if not nfo_found:
                thedirname = os.path.basename(dirpath)
                print(f"{index} : {thedirname} .nfo file not found")
    if ARGS.success_list:
        fo.close()



def loadArgs():
    global ARGS
    parser = argparse.ArgumentParser(description='rename folder with tmdbid.')
    parser.add_argument('dir', help='folder path.')
    parser.add_argument('-i', '--imdb', action='store_true', help='rename folder with IMDb id.')
    parser.add_argument('-t', '--tmdb', action='store_true', help='rename folder with TMDb id.')
    parser.add_argument('-s', '--success-list',  help='output success list to a file.')
    ARGS = parser.parse_args()
    ARGS.dir = os.path.expanduser(ARGS.dir)


def main():
    loadArgs()
    if ARGS.imdb:
        rename_dirs_with_imdb(ARGS.dir)
    else:
        rename_dirs_with_tmdb(ARGS.dir)


if __name__ == '__main__':
    main()
