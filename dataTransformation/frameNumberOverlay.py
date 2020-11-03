import glob
import ffmpeg
import os
import numpy as np

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
for file in glob.glob('../data/*.mp4'):

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
    stream = ffmpeg.input(pathInput)
    
    stream = ffmpeg.drawtext(
        stream,
        text='%{frame_num}',
        start_number=1,
        escape_text=False, # This allows for text to be dynamically changed
        x=20,
        y=20,
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
        pathOutput,
        **{'loglevel': 0}) # Prevent any logs from ffmpeg
    stream = ffmpeg.overwrite_output(stream)

    # Run on file
    # stream.get_args() # Debug what ffmpeg does
    stream.run()
