from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, scan_videos
from sys import argv
import os
import subprocess
from shutil import move

def save_and_merge(video_to_sub_dict):
    """
    The function will save the subtitles from the video_to_sub_dict and merge them with the videos 
    :param video_to_sub_dict: dictionary with Video class as keys and subtitle list as values (defaultdict)
    """
    for video, subs in video_to_sub_dict.items():
        save_subtitles(video, subs)
        name, ext = os.path.splitext(video.name)
        tmp_name = name + 'TorrentDownloaderMerged' + ext

        # Calling to "mkvmerge" command line tool in order to merge the subtitle with the video
        subprocess.call([
            'mkvmerge',
            '-o',
            tmp_name,  # Temp name for the video file, becuase "mkvmerge" need new name for output file
            '-S',
            video.name,
            name + '.he.srt',
        ])

        os.remove(video.name) 
        os.remove(name + '.he.srt')
        os.rename(tmp_name, video.name)


def main(folder_dir):
    print(folder_dir)
    videos = scan_videos(folder_dir)
    subs = download_best_subtitles(videos, {Language('heb')})
    print(videos, subs)
    save_and_merge(subs)

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
