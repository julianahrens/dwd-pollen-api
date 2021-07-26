import logging
from dataclasses import dataclass

from aiohttp import ClientSession

VALUE_MAPPING = {
    '0': {
        'value': 0,
        'desc': 'Keine Belastung',
    },
    '0-1': {
        'value': 1,
        'desc': 'Keine bis geringe Belastung',
    },
    '1': {
        'value': 2,
        'desc': 'Geringe Belastung',
    },
    '1-2': {
        'value': 3,
        'desc': 'Geringe bis mittlere Belastung',
    },
    '2': {
        'value': 4,
        'desc': 'Mittlere Belastung',
    },
    '2-3': {
        'value': 5,
        'desc': 'Mittlere bis hohe Belastung',
    },
    '3': {
        'value': 6,
        'desc': 'Hohe Belastung',
    },
}


@dataclass
class DwdPollenInfo:
    name: str
    today: int
    today_raw: str
    today_desc: str
    tomorrow: int
    tomorrow_raw: str
    tomorrow_desc: str

    @staticmethod
    def from_json(item: dict):
        results = []
        for key in item:
            info = DwdPollenInfo(
                name=key,
                today_raw=item[key]['today'],
                today=VALUE_MAPPING[item[key]['today']]['value'],
                today_desc=VALUE_MAPPING[item[key]['today']]['desc'],
                tomorrow_raw=item[key]['tomorrow'],
                tomorrow=VALUE_MAPPING[item[key]['tomorrow']]['value'],
                tomorrow_desc=VALUE_MAPPING[item[key]['tomorrow']]['desc'],
            )
            results.append(info)
        return results


@dataclass
class DwdPollen:
    URL = 'https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json'

    sender: str
    name: str
    last_update: str
    next_update: str
    region_id: str
    region_name: str
    partregion_id: str
    partregion_name: str
    pollen: [DwdPollenInfo]

    @staticmethod
    def from_json(item: dict, sender: str, name: str, last_update: str, next_update: str):
        return DwdPollen(
            sender=sender,
            name=name,
            last_update=last_update,
            next_update=next_update,
            region_id=item['region_id'],
            region_name=item['region_name'],
            partregion_id=item['partregion_id'],
            partregion_name=item['partregion_name'],
            pollen=DwdPollenInfo.from_json(item['Pollen']),
        )


DEFAULT_SOURCE = DwdPollen


async def get_data(session: ClientSession, *, source=DEFAULT_SOURCE):
    """Fetch DWD pollen info."""
    resp = await session.get(source.URL)
    data = await resp.json(content_type=None)

    results = []

    for item in data['content']:
        try:
            results.append(
                source.from_json(item, data['sender'], data['name'], data['last_update'], data['next_update']))
        except KeyError:
            logging.getLogger(__name__).warning('Got wrong data: %s', item)

    return results
