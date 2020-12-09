import glob
import ffmpeg
import os
from pathlib import Path
import numpy as np
import pyminizip

# Import the cutoffs points for the videos
cutoffs = np.genfromtxt(
    'TimeStamps.csv', 
    delimiter=',', 
    skip_header = 0,
    dtype="|S6" # To import text and ints, string of lenght 6 as maximum
    )

# Split data
cutoffTrial = cutoffs[:,0].astype(str)
cutoffStart = cutoffs[:,1].astype(int)
cutoffEnd = cutoffs[:,2].astype(int)

#  For each video file
for file in glob.glob('_input/*.mp4'):

    # Define where to read and where to write
    pathInput = file
    pathOutput = os.path.basename(file)
    fileTag = os.path.splitext(pathOutput)[0]

    # For all existing files, find corresponding file tag
    try:
        frameStart = cutoffStart[cutoffTrial == fileTag][0]
        frameEnd = cutoffEnd[cutoffTrial == fileTag][0]
    except:
        print("Start and end frame not found for: " + fileTag)
        continue

    # Specify process steps
    stream = ffmpeg.input(pathInput, r=1)
    
    # Overlay frame number
    stream = ffmpeg.drawtext(
        stream,
        text=f'Trial: {fileTag}, '+ 'Frame: %{frame_num}',
        start_number=0, # 0 index
        escape_text=False, # This allows for text to be dynamically changed
        x=20,
        y=20,
        fontfile = 'arial.ttf',
        fontcolor='black',
        fontsize=20,
        box=1,
        boxcolor='white',
        boxborderw=5
    )
    
    stream = ffmpeg.concat(
        stream.trim(
            start_frame=frameStart,
            end_frame=frameEnd
            )
    )

    stream = ffmpeg.output(
        stream, 
        # '_output/' + pathOutput, # For movie output
        '_output/' + fileTag + '_%03d.jpeg', # For image output
        **{'loglevel': 0}, # Prevent any logs from ffmpeg
        start_number = frameStart,
        r=1, # Replay rate constant
        qscale=10 # Make files lower quality. Argument takes values between [10 31]
    )

    # If the file exists, simply overwrite it (using '-y')
    stream = ffmpeg.overwrite_output(stream)

    # Run on file
    # print(stream.get_args()) # Debug what ffmpeg does as command line argument
    stream.run() # If it doesnt run, consult: https://github.com/kkroening/ffmpeg-python/issues/165

    # To zip the file manually use a subprocess with
    'zip -P PASSWORD ../data/frames.zip -r .'

# Finally, zip each file
for file in glob.glob('_output/*.jpeg'):
    basename = Path(file).stem
    targetPath = '../data/' + basename + ".zip"
    pyminizip.compress(file, None, targetPath , "david", 0)