import requests

from web.core import settings


class Bitrix24APIService:
    def __init__(
            self,
            api_url: str = settings.BITRIX24_API_URL
    ):
        self.__api_url = api_url


    def crm_get_deal(self, deal_id: int) -> dict:
        method = 'crm.deal.get'
        url = f'{self.__api_url}{method}'
        response = requests.get(url, params={'ID': deal_id})
        response.raise_for_status()
        return response.json()['result']



bitrix24_api_service = Bitrix24APIService()
