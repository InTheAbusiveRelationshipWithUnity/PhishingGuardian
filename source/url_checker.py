from catboost import CatBoostClassifier
import pandas as pd

from dotenv import load_dotenv
import os

from api_answer_generator import LLMRespondent
import domain_analyzer
import features_extractor


load_dotenv()

API_KEY = os.getenv("API_KEY")

model = "model/catboost_phish_detector.cbm"


class Checker:
    def __init__(self):
        self.model = CatBoostClassifier()
        self.model.load_model(model)

    def _get_probability(self, url: str):

        features = features_extractor.extract_features(url)
        data = pd.DataFrame([features]).drop(columns=["url"])
        data["is_https"] = 0
        catb_prob = self.model.predict_proba(data)[:, 1].item()

        return catb_prob
    
    def analyse(self, url: str):
        domain_info = domain_analyzer.get_domain_info(url)
        probability = self._get_probability(url)

        llm = LLMRespondent(API_KEY)
        
        response = llm.check(url, probability, domain_info["age"], domain_info["owner"])

        return response
