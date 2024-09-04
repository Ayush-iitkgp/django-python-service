import os
from typing import List, Union

from deepl import Translator
from deepl.api_data import TextResult


class TranslationService:
    # create one instance of the deep translation service
    agent = Translator(auth_key=os.environ["DEEPL_API_KEY"])

    @classmethod
    def translate_text(cls, sentence: Union[str, List[str]]) -> Union[str, List[str]]:
        try:
            translations = cls.agent.translate_text(text=sentence, source_lang="en", target_lang="de")
            if isinstance(translations, TextResult):
                return translations.text
            return [translation.text for translation in translations]

        except Exception as ex:
            raise ex
