import json

import requests
from schemas import PagesResponseModel, InstagramIDResponseModel, MediaResponseModel, MediaModel
from settings import ACCESS_TOKEN


def fetch(method: str, url: str, params: dict) -> dict:
    """
    Функция для отправки POST и GET запросов
    """

    if method == 'GET':
        response = requests.get(url=url, params=params)
        return response.json()
    elif method == 'POST':
        response = requests.post(url=url, params=params)
        return response.json()


def get_api_pages(access_token: str) -> PagesResponseModel:
    """
    Функция для получения страниц, к которым имеем доступ по API
    """

    method = 'GET'
    url = f'https://graph.facebook.com/v20.0/me/accounts'
    params = {'access_token': access_token}
    response = fetch(method=method, url=url, params=params)
    pages = PagesResponseModel(**response)
    return pages


def get_instagram_pages(page_id: str, access_token: str):
    method = 'GET'
    url = f'https://graph.facebook.com/v20.0/{page_id}'
    params = {'access_token': access_token, 'fields': 'instagram_business_account'}
    response = fetch(method=method, url=url, params=params)
    instagram_page = InstagramIDResponseModel(**response)
    return instagram_page


def get_instagram_posts(instagram_account_id: str, access_token: str) -> list[MediaModel]:
    method = 'GET'
    url = f'https://graph.facebook.com/v20.0/{instagram_account_id}/media'
    params = {
        'access_token': access_token,
        "fields": "id,permalink,timestamp,comments_count",
        'limit': 100
    }
    response = fetch(method=method, url=url, params=params)
    validate_response = MediaResponseModel(**response)
    return validate_response.data


def get_instagram_reviews(instagram_media_id: str, access_token: str):
    method = 'GET'
    url = f'https://graph.facebook.com/v20.0/{instagram_media_id}/comments'
    params = {
        'access_token': access_token,
        'fields': 'id,text,timestamp,username,replies{id,text,timestamp,username},permalink',
        'limit': 100
    }
    response = fetch(method=method, url=url, params=params)
    return response


def main():
    token = ACCESS_TOKEN
    pages = get_api_pages(access_token=token)
    instagram_pages = []
    for page in pages.data:
        inst_page = get_instagram_pages(page_id=page.id, access_token=token)
        instagram_pages.append(inst_page.instagram_business_account.id)
    all_posts = []
    for i, inst_page in enumerate(instagram_pages):
        posts = get_instagram_posts(instagram_account_id=inst_page, access_token=token)
        all_posts.extend(posts)
        print(f'Получил посты № {i}')
    all_reviews = []
    for post in all_posts:
        if post.comments_count > 0:
            reviews = get_instagram_reviews(instagram_media_id=post.id, access_token=token)
            all_reviews.extend(reviews)


if __name__ == '__main__':
    main()
