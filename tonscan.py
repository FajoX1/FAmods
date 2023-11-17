#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Tonscan
# Description: Информация о TON адресе
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/tonscan.png?raw=true
# requires: requests
# ---------------------------------------------------------------------------------

import requests

from .. import loader, utils

@loader.tds
class Tonscan(loader.Module):
    """Информация о TON адресе"""

    strings = {
        "name": "Tonscan",

        "waiting": "<b><emoji document_id=6334391057186293707>🕑</emoji> Собираю информацию...</b>",
    }

    @loader.command()
    async def tonwallet(self, message):
        """Информация о TON кошельке"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonwallet адрес_кошелька</code>")
        
        await utils.answer(message, self.strings["waiting"])

        response = requests.get(f"https://tonapi.io/v2/accounts/{address}").json()

        try:
          response['error']
          if "can't decode address" in response['error']:
            return await utils.answer(message, f"<b>❌ Это не адрес кошелька!</b>")

          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass
        
        scam = "Нет"

        if response['is_scam'] == "True":
           scam = "Да"

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton wallet

Имя: <code>{response['name']}</code>

Адрес: <code>{address}</code>
Баланс: <code>{response['balance']} TON</code>

Скам: </b><i>{scam}</i><b>
Статус: </b><i>{response['status']}</i><b>
Последння активность: </b><i>{response['last_activity']}</i><b>
Контракт: <code>{response['interfaces'][0]}</code>

<a href="https://tonscan.org/address/{address}">Tonscan</a> • <a href="{response['icon']}">Аватарка</a> • <a href="https://tonscan.org/address/{address}#transactions">История</a> • <a href="https://tonscan.org/address/{address}#nfts">NFT</a> • <a href="https://tonscan.org/address/{address}#tokens">jettons</a> • <a href="https://tonscan.org/address/{address}#source">Contract</a>
</b>""")
        
    @loader.command()
    async def tonjetton(self, message):
        """Информация о TON токене"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonjetton адрес_токена</code>")
        
        await utils.answer(message, self.strings["waiting"])

        response = requests.get(f"https://tonapi.io/v2/jettons/{address}").json()

        try:
          response['error']
          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass
        
        try:
           response['metadata']['description']
           descr = f"\n</b><i>{response['metadata']['description']}</i><b>\n"
        except:
           descr = ""

        try:
           response['metadata']['social']

           socials = """Ссылки:
"""
           for s in response['metadata']['social']:
              socials += s + "\n"
           socials += "\n"
        except:
           socials = ""

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton jetton

Имя: <code>{response['metadata']['name']}</code>
Символ: <code>{response['metadata']['symbol']}</code>
{descr}
Адрес: <code>{address}</code>
Общее предложение: <code>{response['total_supply']} TON</code>

Количество держателей: <code>{response['holders_count']}</code>

{socials}<a href="https://tonscan.org/jetton/{address}">Tonscan</a> • <a href="{response['metadata']['image']}">Лого</a> • <a href="https://tonscan.org/jetton/{address}#transactions">История</a> • <a href="https://tonscan.org/jetton/{address}#holders">Топ держателей</a> • <a href="https://tonscan.org/jetton/{address}#source">Contract</a>
</b>""")
        
    @loader.command()
    async def tonnftcol(self, message):
        """Информация о TON NFT коллекции"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonnftcol адрес_коллекции</code>")
        
        await utils.answer(message, self.strings["waiting"])

        response = requests.get(f"https://tonapi.io/v2/nfts/collections/{address}").json()

        try:
          response['error']
          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass
        
        try:
           response['metadata']['description']
           descr = f"\n</b><i>{response['metadata']['description']}</i><b>\n"
        except:
           descr = ""

        try:
           response['metadata']['external_link']
           external_link = f"\nВнешняя ссылка: {response['metadata']['external_link']}\n"
        except:
           external_link = ""

        try:
           response['metadata']['social_links']

           socials = """Ссылки:
"""
           for s in response['metadata']['social']:
              socials += s + "\n"
           socials += "\n"
        except:
           socials = ""

        try:
           response['metadata']['approved_by']

           approved_by = """Одобрено:
"""
           for s in response['metadata']['approved_by']:
              approved_by += s + "\n"
           approved_by += "\n"
        except:
           approved_by = ""

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton NFT collection

Имя: <code>{response['metadata']['name']}</code>
Адрес: <code>{address}</code>
{descr}
{external_link}
{approved_by}{socials}<a href="https://tonscan.org/nft/{address}">Tonscan</a> • <a href="https://tonscan.org/nft/{address}">Коллекция</a> • <a href="{response['metadata']['image']}">Лого</a> • <a href="{response['metadata']['cover_image']}">Баннер</a>
</b>""")
        
    @loader.command()
    async def tonnft(self, message):
        """Информация о TON NFT"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonnft адрес_nft</code>")
        
        await utils.answer(message, self.strings["waiting"])

        response = requests.get(f"https://tonapi.io/v2/nfts/{address}").json()

        try:
          response['error']
          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass
        
        try:
           response['metadata']['description']
           descr = f"\n</b><i>{response['metadata']['description']}</i><b>\n"
        except:
           descr = ""

        try:
           response['collection']['name']
           coll = f"\nКолекция: <code>{response['collection']['name']}</code>\n"
        except:
           coll = ""

        try:
           response['metadata']['external_link']
           external_link = f"\nВнешняя ссылка: {response['metadata']['external_link']}\n"
        except:
           external_link = ""

        try:
           response['metadata']['social_links']

           socials = """Ссылки:
"""
           for s in response['metadata']['social']:
              socials += s + "\n"
           socials += "\n"
        except:
           socials = ""

        try:
           response['metadata']['approved_by']

           approved_by = """Одобрено:
"""
           for s in response['metadata']['approved_by']:
              approved_by += s + "\n"
           approved_by += "\n"
        except:
           approved_by = ""

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton NFT      
{coll}
Имя: <code>{response['metadata']['name']}</code>
Адрес: <code>{address}</code>
{descr}
{external_link}
{approved_by}{socials}<a href="https://tonscan.org/nft/{address}">Tonscan</a> • <a href="{response['metadata']['image']}">NFT фото</a>
</b>""")
