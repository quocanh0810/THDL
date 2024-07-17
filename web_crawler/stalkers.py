import json
from dataclasses import asdict, dataclass

from unidecode import unidecode


class Stalker:
    def __init__(self, data: str=""):
        data = ' '.join(data.split()).strip()
        self.data = unidecode(data)

    def skipTo(self, token: str="") -> 'Stalker':
        token_index = self.data.index(token)
        return Stalker(self.data[token_index+len(token):])

    def skipToAmount(self, token: str="", amount: int=1) -> 'Stalker':
        _stalker = self
        for _ in range(amount):
            _stalker = _stalker.skipTo(token)
        
        return _stalker

    def backTo(self, token: str="") -> 'Stalker':
        token_index = self.data.index(token)
        return Stalker(self.data[:token_index])

    def __repr__(self) -> str:
        return self.data

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

    def asdict(self) -> dict:
        return asdict(self)

    def isEmpty(self):
        return not all(self.asdict().values())

def process_hacom(data: str):
    stalker = Stalker(data)
    stats = stalker\
            .skipTo('<div class="pd-summary-group" id="js-pd-summary">')\
            .skipTo('</p>')\
            .backTo('<a href="javascript:void(0)"')
    size = stats.skipTo("Kich thuoc:").backTo("</div>").data
    reso = stats.skipTo("Do phan giai:").backTo("</div>").data
    lcd_type = stats.skipTo("Tam nen:").backTo("</div>").data
    freq = stats.skipTo("Tan so quet:").backTo("</div>").data
    rsp_rate = stats.skipTo("Thoi gian phan hoi:").backTo("</div>").data
    lumi = stats.skipTo("Do sang:").backTo("</div>").data
    constr_rate = stats.skipTo("Ti le tuong phan:").backTo("</div>").data
    port = stats.skipTo("Cong ket noi:").backTo("</div>").data

    b = json.loads(stalker.skipTo('<script type="application/ld+json">').backTo('</script>').data)
    price = b["offers"]["price"]
    url = b["offers"]["url"]
    brand = b["brand"]["name"]

    return Monitor(size, reso, lcd_type, freq, rsp_rate, lumi, constr_rate, port, price, url, brand)    

def process_phongvu(data: str):
    stalker = Stalker(data)
    stats = stalker\
            .skipToAmount('"application/ld+json">', 4)\
            .backTo('</script>')
    monitor = Monitor()
    stats = json.loads(stats.data)

    monitor.price = stats["offers"]["price"]
    monitor.url = stats["offers"]["url"]
    monitor.brand = stats["brand"]["name"]

    for p in stats["additionalProperty"]:
        n = p["name"]
        v = p["value"]
        if n == "Kich thuoc":
            monitor.size = v
        elif n == "Do phan giai":
            monitor.reso = v
        elif n == "Tam nen":
            monitor.lcd_type = v
        elif n == "Tan so quet":
            monitor.freq = v
        elif n == "Thoi gian phan hoi":
            monitor.rsp_rate = v
        elif n == "Do sang":
            monitor.lumi = v
        elif n == "Do tuong phan tinh":
            monitor.constr_rate = v
        elif n == "Cong xuat hinh":
            monitor.port = v
        else:
            # print(f"{n} is not supported!" )
            continue

    return monitor

def process_phucanh(data: str):
    stalker = Stalker(data)
    stats = stalker.skipTo('<div id="fancybox-spec" class="js-spec-holder" style="display: none">').backTo('<div style="position: fixed')
    
    size = stats.skipTo("Kich thuoc man hinh").skipTo(":").backTo("</td>").data

    reso = stats.skipTo("Do phan giai").skipTo(":").backTo("</td>").data
    if "</a>" in reso.data:
        reso = reso.skipTo(">").backTo("</a>").data

    lcd_type = stats.skipTo("Tam nen").skipTo(":").skipTo(">").backTo("</a>").data
    freq = stats.skipTo("Tan so quet").skipTo(":").skipTo(">").backTo("</a>").data
    rsp_rate = stats.skipTo("Thoi gian dap ung").skipTo(":").skipTo(">").backTo("</a>").data
    lumi = stats.skipTo("Do sang").skipTo(":").backTo("</td>").data
    constr_rate = stats.skipTo("Ty le tuong phan").skipTo(":").backTo("</td>").data
    port = stats.skipTo("Cong giao tiep").skipTo(":").backTo("</td>").data

    b = json.loads(stalker.skipToAmount('<script type="application/ld+json">', 2).backTo('</script>').data)
    price = b["offers"]["price"]
    url = b["offers"]["url"]
    brand = stalker.skipTo("item_brand:").backTo(",").data

    return Monitor(size, reso, lcd_type, freq, rsp_rate, lumi, constr_rate, port, price, url, brand)   

if __name__ == "__main__":
    # with open("./web/hacom/sample.html", "r") as f:
    with open("./web/hacom/sample2.html", "r") as f:
        data = f.read().replace("\n", "")
        print(process_hacom(data))

    # with open("./web/phongvu/acer-23-8-inch-k243y-e-um-qx3sv-e01--s230302879.html", "r") as f:
    # with open("./logs/extract_pipeline/error/phongvu/man-hinh-lcd-msi-24-5-g255f-1920-x-1080-ips-180hz-1ms-gtg--s240100228.html", "r") as f:
    #     data = f.read().replace("\n", "")
    #     print(process_phongvu(data))

    # with open("./web/phucanh/sample2.html", "r") as f:
    #     data = f.read().replace("\n", "")
    #     print(process_phucanh(data))
