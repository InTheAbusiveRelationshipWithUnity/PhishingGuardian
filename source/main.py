import os
from dotenv import load_dotenv

from url_checker import Checker
import asyncio
from aiohttp import ClientSession
from typing import Union, Any


load_dotenv()
TOKEN = os.getenv("TOKEN")


async def get_updates(session: ClientSession,
                      offset: Union[Any, None] = None)\
                      -> list[dict[str, Any]]:
    """
    Получение обновлений
    """
    paramets = {"timeout": 30}
    if offset:
        paramets["offset"] = offset
    if TOKEN:
        async with session.get("https://api.telegram.org/bot"
                               + TOKEN + "/getUpdates", params=paramets)\
                                as reply:
            json = await reply.json()
            result = json.get("result", [])
            if isinstance(result, list):
                return result
    return []


async def send_message(session: ClientSession, chat_id: int, text: str) -> None:
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    if TOKEN:
        async with session.post("https://api.telegram.org/bot" +
                                TOKEN + "/sendMessage", json=payload):
            print("Message sent")


async def main() -> None:
    checker = Checker()

    offset = None
    
    async with ClientSession() as session:
        while True:
            updates = await get_updates(session, offset)
            
            if not updates:
                continue
            
            for update in updates:
                update_id = update.get("update_id")
                message = update.get("message")
                
                if not isinstance(update_id, int) or not message:
                    continue
                
                chat_id = message["chat"]["id"]
                text = message["text"]
                user_id = message["from"]["id"]
                
                if text == "/start":
                    await send_message(session, chat_id,
                                           "Отправьте ссылку для анализа"
                                           )
                else:
                    result = await asyncio.to_thread(checker.analyse, text)
                    
                    if result:
                        await send_message(session, chat_id, f"Вердикт: {result.verdict}")
                        await send_message(session, chat_id, f"Уверенность: {result.confidence_lvl}%")
                        await send_message(session, chat_id, f"{result.explanation}")
                    else:
                        await send_message(session, chat_id,
                                           f"Не удалось получить информацию. Проверьте правильно написания ссылки"
                                           )
                    
                offset = update_id + 1    


if __name__ == "__main__":
    checker = Checker()
    
    print(checker._get_probability("https://github.com/InTheAbusiveRelationshipWithUnity/CV/blob/main/README.md"))
    
    #result = checker.analyse("https://www.youtube.com/")
    #print(result.verdict)
    #print(result.confidence_lvl)
    #print(result.explanation)

    # asyncio.run(main())
