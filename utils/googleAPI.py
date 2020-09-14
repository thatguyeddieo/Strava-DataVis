""" ---------------------------------------------------------------------- """
import os
import requests
""" ---------------------------------------------------------------------- """

def get_map(zm,sc,cent,api_key,img_name,widxhght=[500,500],
            img_ext='.png',out_dirc='.',check=False):
    """
    Parameters:
    -----------
    zm: int
        Zoom level of the region desired

    sc: int
        Scale parameter. It affects the number of pixels that are returned. 
        scale=2 returns twice as many pixels as scale=1 while retaining the 
        same coverage area and level of detail (i.e. the contents of the map
        don't change)

    cent: ndarray or list
        Center coordinates in list or numpy array form
        Must be in degree units
        [lat_coord,long_coord] 
    
    api_key: str
        API key parameter needed to connect to Google Maps Static platform
        Google requires a unique API key to authenticate requests.
        Get an API key here: 
        https://developers.google.com/maps/documentation/maps-static/get-api-key

    img_name: str
        Filename for image generated

    widxhght: list or ndarray
        Defines the rectangular dimensions of the map image in pixels. The 
        parameter takes a list of integers where the first value is the width 
        size and second is the height size.
        By default set to 500x500 pixels

    img_ext: str
        Saved image extension
        * .png (default)
        * .txt

    out_dirc: str
        Directory path in which image is saved into

    check: bool
        If True, this function will check to see if image file name as defined
        by img_name exisits in directory out_dirc.

    Returns:
    --------
    img_out: str
        Returns path to image generated

    Notes:
    ------
        For more information about using Google Maps Static API visit:
        https://developers.google.com/maps/documentation/maps-static/start#Zoomlevels

        Setting check=True can be useful if the user wishs to reduce their
        requests from the Google Maps Static API site. Instead of repeatily 
        creating the same center, zoom, and scale static map, the user can 
        save time and efforts by reusing already created map images.

    """

    google_url = "https://maps.googleapis.com/maps/api/staticmap?"
    out_dirc = os.getcwd()  if out_dirc == '.' else out_dirc

    if check == True and os.path.exists(os.path.join(out_dirc,(img_name+img_ext))):
        str_out = "User set check==True and it was found that\n" +\
                  "{} already exists.\n".format(os.path.join(out_dirc,(img_name+img_ext))) +\
                  "No request to Google Maps Static API was made.\n\n"
        print(str_out)
        return None

    request_url = "{}center={}&zoom={}&size={}&scale={}&key={}"

    cent_unpacked = ','.join(str(i) for i in cent)
    size_unpacked = 'x'.join(str(i) for i in widxhght)
    
    request_url = request_url.format(google_url,cent_unpacked,zm,size_unpacked,sc,api_key)    
    response = requests.get(request_url)

    # save out
    img_out = os.path.join(out_dirc,(img_name+img_ext))
    with open(img_out,'wb') as img:
        img.write(response.content)
    
    return img_out