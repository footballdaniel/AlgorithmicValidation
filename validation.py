import streamlit as st
import pandas as pd
import base64
import glob
import cv2
import SessionState




# The data
df = pd.DataFrame(
    {
        'test': [1,2,3],
        'values': [2,4,5]
    }
)

# The images
images = glob.glob('data/*.jpeg')
# https://discuss.streamlit.io/t/how-can-i-create-a-app-to-explore-the-images-in-a-folder/5458/2
# To have a persistent index, use 'number_input'
sessionState = SessionState.get(indexImage = 0)

# Start blank app
st.title('Blank template app')

if st.button('Next image'):
    sessionState.indexImage += 1


if st.button('Previous image'):
    if sessionState.indexImage > 0:
        sessionState.indexImage -= 1

st.text(f'current image index: {sessionState.indexImage}')
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
        download="{csv}"><input type="button" value="Download"></a>'

st.markdown(get_table_download_link(df), unsafe_allow_html=True)
