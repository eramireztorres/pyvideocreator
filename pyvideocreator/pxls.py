
import requests
import os

class PexelsRequester:
    IMAGE_BASE_URL = 'https://api.pexels.com/v1/search'
    VIDEO_BASE_URL = 'https://api.pexels.com/videos/search'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_images_by_query(self, query, per_page=15, page=1):
        headers = {
            'Authorization': self.api_key
        }

        params = {
            'query': query,
            'per_page': per_page,
            'page': page
        }

        response = requests.get(self.IMAGE_BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_videos_by_query(self, query, per_page=15, page=1):
        headers = {
            'Authorization': self.api_key
        }

        params = {
            'query': query,
            'per_page': per_page,
            'page': page
        }

        response = requests.get(self.VIDEO_BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def save_content(self, url, folder_path, filename):
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(folder_path, exist_ok=True)

        with open(os.path.join(folder_path, filename), 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def save_image(self, image_url, folder_path='images', filename='downloaded_image.jpg'):
        self.save_content(image_url, folder_path, filename)

    def save_video(self, video_url, folder_path='videos', filename='downloaded_video.mp4'):
        self.save_content(video_url, folder_path, filename)
        
    def save_all_content_by_query(self, query, folder_path, per_page=15):
        """ 
        Save all images and videos related to a query in a specific folder.
        
        Args:
        - query (str): The search query.
        - folder_path (str): Destination folder.
        - per_page (int): Number of items per page to fetch. Default is 15.
        
        Returns:
        - list: A list containing two lists - saved image filenames and saved video filenames.
        """
        saved_images = []
        saved_videos = []

        # Get images and save them
        image_data = self.get_images_by_query(query, per_page)
        for photo in image_data['photos']:
            image_url = photo['src']['original']
            image_id = photo['id']
            filename = f"image_{image_id}.jpg"
            self.save_image(image_url, os.path.join(folder_path, 'images'), filename)
            saved_images.append(filename)

        # Get videos and save them
        video_data = self.get_videos_by_query(query, per_page)
        for video in video_data['videos']:
            video_url = video['video_files'][0]['link']
            video_id = video['id']
            filename = f"video_{video_id}.mp4"
            self.save_video(video_url, os.path.join(folder_path, 'videos'), filename)
            saved_videos.append(filename)

        return [saved_images, saved_videos]


def filter_by_aspect_ratio(aspect_ratio_type, data, filetype="photos"):
    """
    Filters Pexels API response items based on aspect ratio.

    Args:
    - aspect_ratio_type (str): Can be "standard" for wider-than-tall or "short" for taller-than-wide.
    - data (dict): The response data from Pexels API, containing items with 'width' and 'height'.

    Returns:
    - list: A list of filtered items from the response data.
    """
    filtered_items = []

    for item in data[filetype]:  
        width = item['width']
        height = item['height']

        if aspect_ratio_type == "standard" and width > height:
            # Add to list if the item is wider than tall
            filtered_items.append(item)
        elif aspect_ratio_type == "short" and height > width:
            # Add to list if the item is taller than wide
            filtered_items.append(item)

    return filtered_items


## Ejemplo de uso
# if __name__ == "__main__":
    # API_KEY = 'pexels_api_key'
    # pexels_requester = PexelsRequester(API_KEY)

    # image_data = pexels_requester.get_images_by_query(query='Dendrobatidae')
    # filtered_images = filter_by_aspect_ratio('standard', image_data, filetype="photos")
    # first_image_url = filtered_images[0]['src']['original']    
    # pexels_requester.save_image(first_image_url, folder_path='images', filename='nature_image.jpg')

    # video_data = pexels_requester.get_videos_by_query(query='Dendrobatidae')
    # filtered_videos = filter_by_aspect_ratio('standard', video_data, filetype="videos")
    # first_video_url = filtered_videos[0]['video_files'][0]['link']
    # # pexels_requester.save_video(first_video_url, folder_path='videos', filename='nature_video.mp4')
