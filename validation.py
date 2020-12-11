import streamlit as st
import pandas as pd
import base64
import glob
import cv2
import SessionState
import zipfile
import tempfile
import pathlib

# Persistent state variables
# https://discuss.streamlit.io/t/how-can-i-create-a-app-to-explore-the-images-in-a-folder/5458/2
# https://discuss.streamlit.io/t/is-there-any-working-example-for-session-state-for-streamlit-version-0-63-1/4551
# Improved: https://discuss.streamlit.io/t/alternative-implementation-of-session-state/799/21
sessionState = SessionState.get(
    indexImage = 0,
    currentAoi = 0,
    keyPassword = 0, # If the key != 0, the input field is empty/disabled. see:
    keyJump = 0,
    tempFolder = "",
    aoi = "",
    dataFrame = pd.DataFrame()) # https://github.com/streamlit/streamlit/issues/623#issuecomment-551755236

# Create a session temporary folder if none has been defined to store the extracted files from zip
if sessionState.tempFolder == "":
    # Initiate a temporary directory
    zipDir = tempfile.TemporaryDirectory()
    sessionState.tempFolder = zipDir.name

# Sidebar content:
# Logo
st.sidebar.image('logo.png')

# username
username = st.sidebar.text_input("Enter your first name")

# Password authentication
password = st.sidebar.text_input("Enter a password", type="password", key = sessionState.keyPassword)
if (password):
    # Initiate a progress bar
    progress_bar = st.sidebar.progress(0)

    for index, file in enumerate(glob.glob("data/*.zip")):
        # Update progress bar
        nfiles = len(glob.glob("data/*.zip"))
        progress_bar.progress(((index+1)/nfiles))

        z = zipfile.ZipFile(file)
        z.setpassword(pwd=bytes(password, 'utf-8'))
        z.extractall(sessionState.tempFolder)
    
    sessionState.keyPassword += 1 # Reset the input field

# Jump to trial
jumpTo = st.sidebar.text_input('Jump to Frame', key = sessionState.keyJump)
if (jumpTo):
    sessionState.indexImage = int(jumpTo)
    sessionState.keyJump += 1 # Reset the input field

# Start blank app
st.title('Validation Algorithmic Gaze Detection')
st.markdown("""
This is the validation of an algorithmic analysis for the Pupil eye-tracker. It contains a total of 1594 frames.
To start, fill in the password in the sidebar and hit `Enter`. Then, provide your first name and confirm with `Enter`.
Loading the images takes several minutes.

Please indicate for each frame, which AOI the gaze (green circle) is closest to. Use one of the eight AOI regions.
The area `Right arm` is assigned when the gaze is on the arm that is on the left side of the frame (i.e. the opponents' right arm).
The area `Other` is for frames when the gaze lies outside of the judoka's body or when there is no green gaze target.
For some frames, there are two green gaze circles visible. This is when Pupil could not identify a binocular point of view.

The choice for the current frame is saved when either the button `Next image` is clicked.
When finished, click the button `Download Results` to get the `CSV` file. 
Please save the results after every trial. If the app crashes (suddenly no frames are displayed), restart the app and 
jump to the frame where you left off.
""")

# The images
# images = glob.glob('data/*.jpeg')
images = sorted(glob.glob(sessionState.tempFolder + "/*.jpeg"))

# The UI
if images != []:

    # Get the information from the images:
    currentImage = images[int(sessionState.indexImage)]
    currentImageName = pathlib.Path(currentImage).stem

    currentFrame = currentImageName.split("_")[1]
    currentTrial = currentImageName.split("_")[0]

    # Two column buttons
    col1, col2, col3 = st.beta_columns(3)

    with (col1):
        sessionState.aoi = st.radio(
            'Chose on which AOI gaze is currently', 
            ['Head', 'Chest', 'Pelvis', 'Left arm', 'Right arm', 'Left leg', 'Right leg', 'Other'],
            index = sessionState.currentAoi)


    with (col2):
        if st.button('Previous image'):
            if sessionState.indexImage > 0:
                sessionState.indexImage -= 1

    with (col3):
        if st.button('Next image'):
            if sessionState.indexImage < len(images) -1:
                sessionState.dataFrame = sessionState.dataFrame.append(
                    {
                        'Trial': currentTrial,
                        'Frame': currentFrame,
                        'Label': sessionState.aoi,
                        'Rater': username,
                        'CurrentIndex': sessionState.indexImage
                    }, 
                    ignore_index = True)

                # Save as df
                sessionState.dataFrame.to_csv("results.csv")

                sessionState.indexImage += 1

    # Display current image
    image = cv2.imread(images[int(sessionState.indexImage)])
    st.image(image, use_column_width=True, channels = 'BGR')    

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def get_table_download_link(df):
    """Generates a link allowing the data in a pandas dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    # csv = df.to_csv(index=False)
    csv = open("results.csv", 'rb').read()
    b64 = base64.b64encode(csv).decode('UTF-8')  # strings/bytes conversions
    return f'<a href="data:file/txt;base64,{b64}" \
        download="{"Results.csv"}"><input type="button" value="Download Results"></a>'

# If there is data to download
# if (len(sessionState.dataFrame) > 0):
st.text("")
st.markdown(get_table_download_link(sessionState.dataFrame), unsafe_allow_html=True)

# Display current index
st.text(f'The last frame clicked is: {sessionState.dataFrame.index[sessionState.indexImage-1]}')

# # Debug
# st.text("Targeting currently: " + sessionState.tempFolder)