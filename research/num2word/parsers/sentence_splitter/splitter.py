from typing import Any
import stanza
from utils.decorators import free_cache

class SyntaxAnalyzer:
    @free_cache
    def __init__(self) -> None:
        self.pipeline = stanza.Pipeline(
            lang='ru', 
            use_gpu=True,
            package='syntagrus'
        ) 

    def __call__(self, text: str) -> list[str] | None:
        sentences = None
        try:
            sentences = self.get_sentences(self.get_doc(text), normalize=False)
        except:
            print(f'[ERROR] [SA] [{text}]')

        return sentences

    def get_doc(self, text: str) -> stanza.Document:
        """Сегментация и синтаксический анализ текста

        Args:
            text (str): Входной текст

        Raises:
            AssertionError: при некорректных входных данных
            ValueError: при ошибке обработки текста

        Returns:
            stanza.Document: Список предложений с метками
        """
        assert type(text) is str
        assert len(text) != 0

        doc = self.pipeline(text)
        if doc is None:
            raise ValueError
        
        return doc

    @staticmethod
    def get_sentences(
        doc: stanza.Document,
        normalize: bool = False,
        upos: list[str] = []) -> list[str]:
        if normalize:
            attribute = 'lemma'
        else:
            attribute = 'text'

        sentences = []
        for sentence in doc.sentences:
            words = []
            for token in sentence.words:
                if attribute in dir(token):
                    cur_attr = attribute
                else:
                    cur_attr = 'text'

                if ('upos' in dir(token) and token.upos in upos) or upos == []:
                    words.append(getattr(token, cur_attr))

            sentences.append(' '.join(words))
        
        return sentences