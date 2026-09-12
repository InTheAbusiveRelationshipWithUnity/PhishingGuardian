from pydantic import BaseModel, Field
from gigachat import GigaChat


class LLMResponse(BaseModel):
    verdict: str = Field(description="Вердикт по домену")
    
    confidence_lvl: int = Field(
        description="Оценка модели"
    )
    
    explanation: str = Field(
        description="Пояснение по вердикту"
    )

class LLMRespondent:
    def __init__(self, api_key, model="GigaChat-2-Pro"):
        self.client = GigaChat(
            credentials=api_key,
            scope="GIGACHAT_API_PERS",
            verify_ssl_certs=False
        )
        
        self.model = model
        
    def check(self, url: str, ml_score: int, domain_age_days: int, domain_owner: str) -> LLMResponse:
        system_prompt = """
            Тебе необходимо оценить вероятность того, что поданная на вход ссылка является фишинговой
            на основании возраста домена, его владельца и оценки вероятности ml-модели.
        """
        
        user_prompt = f"""
            url: {url},
            оценка модели вероятности фишинга: {ml_score},
            возраст домена в днях: {domain_age_days},
            владелец домена: {domain_owner}
        """
        
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "model": self.model,
            "temperature": 0.2
        }
        
        try:
            response = self.client.chat.parse(
                payload=payload,
                response_format=LLMResponse
            )
            
            return response[1]

        except Exception as e:
            print(f"Произошла ошибка: {e}")
        