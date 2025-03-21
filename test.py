from pprint import pprint

import requests


def test_bitrix_api(
        method: str,
        params: dict | None = None
):
    bitrix_url = 'https://avgrup.bitrix24.ru/rest/409/8trpxasc0c1mtpe3/'
    url = f'{bitrix_url}{method}'
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()
    except Exception:
        print(response.json())
    result = response.json()
    if "result" in result:
        return result
    else:
        error = result.get("error_description", "Unknown error")
        raise Exception(f"Bitrix24 API error: {error}")





deal_IDS = [7769, 7535, 7179, 7793, 7767]
# deal = test_bitrix_api('crm.deal.get', params={'ID': 7769})['result']
# pprint(deal)

# print(deal['CONTACT_ID'])
# contact = test_bitrix_api('crm.contact.get', params={'ID': deal['CONTACT_ID']})['result']
#
# pprint(contact)

# for deal_id in deal_IDS:
#     deal = test_bitrix_api('crm.deal.get', params={'ID': deal_id})['result']
#
#     print()
#     print(deal['TITLE'])
#     print(deal['STAGE_ID'])
#     print('username\n')
#     print(deal['UF_CRM_67CE99F467C8A'])
print(6 in range(6))
