
import glob
import ffmpeg
import os

for file in glob.glob('../data/*.mp4'):

    # Define where to read and where to write
    pathInput = file
    pathOutput = os.path.basename(file)

    # Specify process steps
    stream = ffmpeg.input(pathInput)
    stream = ffmpeg.drawtext(
        stream,
        text="%{n}",
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
    stream = ffmpeg.output(stream, pathOutput)

    # Run on file
    # stream.get_args() # Debug what ffmpeg does
    stream.run()

    print(file)