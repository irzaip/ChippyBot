
def admin_eta(self) -> str:
    return f"""Assalamualaikum semua.
Nama saya {self.conv_obj.bot_name}, saya disini membantu kakak-kakak dan abang-abang semua, untuk minta
bantuan saya, tulis nama saya di depan setiap permintaan kalian.

misalnya: *{self.conv_obj.bot_name} buatkan saya pidato kepresidenan untuk menerima G20 sebagai aliansi indonesia* 

hihi, tapi ya gak gitu juga ya.. kan situ bukan presiden. :))
permintaan harus spesifik dan jelas, supaya saya bisa lebih mudah mengerjakannya. Tapi jangan susah-susah juga yaaa... saya kan cuma robot yg kecil dan imut. :))
"""

def admin_help(self) -> str:
    return f""".reset: reset to default
.who: check persona and mode
.set:
.send:
.join:
.intro:
.others:
.eta: terangkanlah
""" 

