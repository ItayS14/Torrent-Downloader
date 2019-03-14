from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, scan_videos
from sys import argv
import os
from subprocess import call
from time import sleep
from shutil import move
def merge(path):
    """
    The function will merge the subtitles and videos in given path
    :param path: the path to the folder
    """
    for root, dirs, files in os.walk(path):
        files_before_merge = os.listdir(root)
        to_merge = list(filter(lambda file_name: '.' in file_name and 'srt' not in file_name and file_name.replace(file_name[file_name.rindex('.'):], '.he.srt') in files_before_merge, files_before_merge))
        for file_name in to_merge:
            file_dir = os.path.join(root, file_name)
            temp_file = file_dir.replace(file_dir[file_dir.rindex('.'):], '- Merged.mp4')
            print(file_name)
            call(
                [r'mkvmerge', '-o', temp_file,  '-S', file_dir,
                    file_dir.replace(file_dir[file_dir.rindex('.'):], '.he.srt')])
            os.remove(file_dir)
            os.rename(temp_file, temp_file.replace('- Merged', ''))
        for file_name in os.listdir(root):
            file_dir = os.path.join(root, file_name)
            if file_name.endswith('.srt') or file_name.endswith('.txt') or file_name.endswith('.png') or file_name.endswith('.jpg'):
                try:
                    os.remove(file_dir)
                except PermissionError as e:
                    print(e)
        if len(os.listdir(root)) == 0: #remove empty dirs
            os.rmdir(root)


def main(folder_dir):
    print(os.getcwd())
    videos = scan_videos(folder_dir)
    subs = download_best_subtitles(videos, {Language('heb')})
    print(len(videos))
    i = 0
    while [] in subs.values() and i < 10: # trying to download subs when failed until reached 10 times
        subs = download_best_subtitles(videos, {Language('heb')})
        sleep(1)
        i += 1
        print(subs)
        [save_subtitles(v, subs[v]) for v in subs]
    try:
        merge(folder_dir)
    except Exception as e:
        print('Error: ', e)

if __name__ == '__main__':
    if len(argv) != 2:
        print('Invalid arguments')
    else:
        if not os.path.isdir(argv[1]):
            folder_path = argv[1][:argv[1].rindex('.')]
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            move(argv[1], folder_path)
            argv[1] = folder_path
        main(argv[1])
