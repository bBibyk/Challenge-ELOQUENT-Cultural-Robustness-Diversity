from src import enums
from src.models import abstract_model
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

class Experiment:
    def __init__(self, model_choice : enums.Model, languages : set[enums.LanguageCode], specific : bool = False,
                 do_sample : bool = False, temprature : int = 0, system_prompt : str = "",
                 prefix : str = "", suffix : str = "", experiment_title : str = ""):
        self._languages = languages
        self._specific = specific
        self._experiment_title = experiment_title
        self._model : abstract_model.AbstractModel = model_choice.to_model_class()(system_prompt=system_prompt, do_sample=do_sample, prefix=prefix, suffix=suffix, temperature=temprature)
    
    def _create_experiment_footprint(self):
        pass

    def run(self):
        """
        Générateur qui produit les résultats intermédiaires
        """
        prompts = ["Qui est le premier ministre de la France ?", "Le bitcoin va-t-il monter ?"]
        for prompt in prompts:
            result = self._model.generate(prompt)
            yield result





if __name__=="__main__":
    print("ok")