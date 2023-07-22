import httpx
import json


def get_img(access_token, url, media_type,user_id, post_id)->str:
    """Takes in access token of facebook app, url of facebook post, media type (img or video), user_id, post_id
        returns the url/src of video or image

    Args:
        access_token (str)
        url (str): url of the post containing media
        media_type (str): 'img' or 'video
        user_id ('str')
        post_id ('str')

    Raises:
        KeyError: When the provided user id or post id does not exist or cannot be obtained with current permissions
    """
    media_types = ['img', 'video']
    if media_type not in media_types:
        raise ValueError("Invalid sim type. Expected one of: %s" % media_types)
    
    if media_type == 'video':
        r = httpx.get('{}?access_token={}'.format(url, access_token))
        for thumbnail in json.loads(r.text)['data']:
            if(thumbnail['is_preferred']==True):
                return(thumbnail['uri'])
                break
    elif media_type == 'img':
        r = httpx.get('https://graph.facebook.com/{}_{}?fields=full_picture,picture&access_token={}'.format(user_id, post_id,access_token))
        try:
            image_url = (json.loads(r.text)['full_picture'])
            return image_url
        except KeyError:
            raise KeyError('Unsupported get request. Object with provided user and post ID does not exist, cannot be loaded due to missing permissions, or does not support this operation')
        
        
