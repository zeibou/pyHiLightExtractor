from dataclasses import dataclass
from datetime import timedelta
import os
from pyHiLightExtractor import HiLightFinder
from moviepy.editor import VideoFileClip

@dataclass
class HiLightDescriptor:
    path: str
    local_time: timedelta
    global_time: timedelta


@dataclass
class VideoDescriptor:
    name : str
    path: str
    previous_name : str
    total_time: timedelta


def get_all_hilights(folder, startswith='G', endswith='.mp4'):
    global_time = timedelta(0)
    for filepath in sorted(os.listdir(folder)):
        if filepath.lower().startswith(startswith.lower()) and filepath.lower().endswith(endswith.lower()):
            full_path = os.path.join(folder, filepath)
            duration = VideoFileClip(full_path).duration
            hilights = HiLightFinder.find_hilights(full_path)
            for h in hilights:
                local_time = timedelta(milliseconds=h)
                yield HiLightDescriptor(filepath, local_time, local_time + global_time)
            global_time += timedelta(seconds=duration)


def get_all_videos(folder, startswith='G', endswith='.mp4'):
    previous_name = None
    for file_name in sorted(os.listdir(folder)):
        if file_name.lower().startswith(startswith.lower()) and file_name.lower().endswith(endswith.lower()):
            full_path = os.path.join(folder, file_name)
            duration = VideoFileClip(full_path).duration
            yield VideoDescriptor(file_name, full_path, previous_name, duration)
            previous_name = file_name


if __name__ == '__main__':
    path = "/Users/nicolas.seibert/Documents/foot/2019-01-14/"
    for d in get_all_videos(path, endswith='.MP4'):
        print(d)
    for d in get_all_hilights(path, endswith='.MP4'):
        print(d.path, d.local_time, d.global_time)