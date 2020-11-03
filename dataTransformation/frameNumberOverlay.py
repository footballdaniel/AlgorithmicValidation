
import glob, os, sys

for file in glob.glob('Video/*.mp4'):
    os.system(f'ffmpeg -i {file} -vf "drawtext=fontfile=Arial.ttf: text='%{frame_num}': start_number=1: x=(w-tw)/2: y=h-(2*lh): fontcolor=black: fontsize=20: box=1: boxcolor=white: boxborderw=5" -c:a copy {file}')

    print(file)