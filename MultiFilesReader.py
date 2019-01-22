from dataclasses import dataclass
from datetime import timedelta
import os
import HiLightFinder
from moviepy.editor import VideoFileClip

@dataclass
class HiLightDescriptor:
    path: str
    local_time: timedelta
    global_time: timedelta

def parse_directory(folder, startswith='G', endswith='.mp4'):
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



if __name__ == '__main__':
    path = "/Users/nicolas.seibert/Documents/foot/2019-01-14/"
    for d in parse_directory(path, endswith='.MP4'):
        print(d.path, d.local_time, d.global_time)