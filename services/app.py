from dataclasses import asdict, dataclass
from typing import Annotated

import pymongo
from litestar import Litestar, post
from litestar.enums import RequestEncodingType
from litestar.params import Body, Parameter

MONGO_URI = "mongodb://mongo:password@localhost:27017"
MONGO_DB = "items"
MONGO_COLLECTION = "scrapy_items"
mongo_client = pymongo.MongoClient(MONGO_URI)

@dataclass
class Monitor:
    size: str=""
    reso: str=""
    lcd_type: str=""
    freq: str=""
    rsp_rate: str=""
    lumi: str=""
    constr_rate: str=""
    port: str=""
    price: str=""
    url: str=""
    brand: str=""

    def asdict(self):
        return asdict(self)

@post(path="/")
async def getMonitor(
    data: Annotated[Monitor, Body(media_type=RequestEncodingType.MULTI_PART, default=Monitor())],
    limit: Annotated[str, Parameter(const=True, default=10, required=False)]
) -> Monitor:
    res = mongo_client[MONGO_DB][MONGO_COLLECTION].find(data.asdict()).limit(int(limit))
    return list(res)


app = Litestar(route_handlers=[getMonitor])