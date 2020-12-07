import streamlit as st
import pandas as pd
import base64
import glob
import cv2
import SessionState
import zipfile
import tempfile

# Persistent state variables
# https://discuss.streamlit.io/t/how-can-i-create-a-app-to-explore-the-images-in-a-folder/5458/2
# https://discuss.streamlit.io/t/is-there-any-working-example-for-session-state-for-streamlit-version-0-63-1/4551
sessionState = SessionState.get(
    indexImage = 0,
    currentAoi = 0,
    keyPassword = 0, # If the key != 0, the input field is empty/disabled. see:
    keyJump = 0,
    tempFolder = "",
    dataFrame = pd.DataFrame()) # https://github.com/streamlit/streamlit/issues/623#issuecomment-551755236

# Create a session temporary folder if none has been defined
if sessionState.tempFolder == "":
    # Initiate a temporary directory
    zipDir = tempfile.TemporaryDirectory()
    sessionState.tempFolder = zipDir.name

# Sidebar content:
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
jumpTo = st.sidebar.text_input('Jump to Trial', key = sessionState.keyJump)
if (jumpTo):
    sessionState.indexImage = int(jumpTo)
    sessionState.keyJump += 1 # Reset the input field

# Start blank app
st.title('Validation Gaze')
st.text('This is the validation of the Pupil eye-tracker. It contains a total of 1600 frames.')

# The images
# images = glob.glob('data/*.jpeg')
images = sorted(glob.glob(sessionState.tempFolder + "/*.jpeg"))

# The UI
if images != []:

    # st.text(images)
    st.text("Loaded temporarily to: " + sessionState.tempFolder)

    # Two column buttons
    col1, col2= st.beta_columns(2)

    with (col1):
        if st.button('Previous image'):
            if sessionState.indexImage > 0:
                sessionState.indexImage -= 1

    with (col2):
        if st.button('Next image'):
            sessionState.dataFrame = sessionState.dataFrame.append({'Frame': images[int(sessionState.indexImage)]}, ignore_index = True)
            sessionState.indexImage += 1

    # AOI button
    aoi = st.radio(
        'Chose on which AOI gaze is currently', 
        ['Head', 'Chest', 'Pelvis', 'Left arm', 'Right arm', 'Left leg', 'Right leg', 'Other'],
        index = sessionState.currentAoi)

    # Display current image
    image = cv2.imread(images[int(sessionState.indexImage)])
    st.image(image, use_column_width=True, channels = 'BGR')

    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
    def get_table_download_link(df):
        """Generates a link allowing the data in a pandas dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings/bytes conversions
        return f'<a href="data:file/txt;base64,{b64}" \
            download="{csv}"><input type="button" value="Download Results"></a>'

    # Index and save
    st.text(f'current image index: {sessionState.indexImage}')
    st.markdown(get_table_download_link(sessionState.dataFrame), unsafe_allow_html=True)

