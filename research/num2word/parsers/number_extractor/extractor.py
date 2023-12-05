from number_extractor.number import NUMBER
from natasha.extractors import Extractor
import re
from typing import Union

class NumberExtractor(Extractor):
    def __init__(self) -> None:
        super(NumberExtractor, self).__init__(rule=NUMBER, morph=None)
        self.change_rules = {
            1: 'первых',
            2: 'вторых',
            3: 'третьих',
            4: 'четвертых',
            5: 'пятых',
            6: 'шестых',
            7: 'седьмых',
            8: 'восьмых',
            9: 'девятых',
        }

    def replace(self, text: str) -> Union[str, None]:
        """
        Замена чисел в тексте без их группировки

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
        """
        if text:
            new_text = ""
            start = 0

            for match in self.parser.findall(text):
                if match.fact.multiplier:
                    num = match.fact.int * match.fact.multiplier
                else:
                    num = match.fact.int
                num = str(num)
                if '.' in num:
                    parts = num.split('.')
                    max_get = len(parts[1])
                    if max_get > 3:
                        max_get = 3
                    num = parts[0] + parts[1][0:max_get]

                new_text += text[start: match.span.start] + num
                start = match.span.stop
            new_text += text[start:]

            if start == 0:
                return text
            else:
                return self.fix_text(new_text)
        else:
            return None

    def fix_text(self, text: str) -> str:
        """Замена в тексте числительных вида: "во-первых"

        Args:
            text (str): текст с числительным

        Returns:
            str: текст с измененным предлогом
        """
        for key in self.change_rules.keys():
            text = re.sub(
                r'(во?-)'+str(key)+r'([^а-яёa-z])',
                r'\1'+str(self.change_rules[key])+r'\2',
                text,
                flags=re.IGNORECASE
            )

        return text
    
    def replace_groups(self, text: str) -> Union[str, None]:
        """
        Замена сгруппированных составных чисел в тексте

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
        """
        if text:
            start = 0
            matches = list(self.parser.findall(text))
            groups = []
            group_matches = []

            for i, match in enumerate(matches):
                if i == 0:
                    start = match.span.start
                if i == len(matches) - 1:
                    next_match = match
                else:
                    next_match = matches[i + 1]

                group_matches.append(match.fact)
                if text[match.span.stop: next_match.span.start].strip() or next_match == match:
                    match_start = text[match.span.start:match.span.stop]
                    if match.span.start != 0:
                        if text[match.span.start - 1] in (',', '.'):
                            if res := re.search(r'^0+', match_start):
                                start += res.span()[1]

                    groups.append((group_matches, start, match.span.stop))
                    group_matches = []
                    start = next_match.span.start
            
            new_text = ""
            start = 0

            for group in groups:
                num = 0
                nums = []
                new_text += text[start: group[1]]

                for match in group[0]:
                    curr_num = match.int * match.multiplier if match.multiplier else match.int
                    if match.multiplier:
                        num = (num + match.int) * match.multiplier
                        nums.append(num)
                        num = 0
                    elif num > curr_num or num == 0:
                        num += curr_num
                    else:
                        nums.append(num)
                        num = 0
                if num > 0:
                    nums.append(num)

                num = str(sum(nums))
                if '.' in num:
                    parts = num.split('.')
                    max_get = len(parts[1])
                    if max_get > 3:
                        max_get = 3
                    num = parts[0] + '.' + parts[1][0:max_get]
                
                new_text += num
                start = group[2]

            new_text += text[start:]

            if start == 0:
                return text
            else:
                return self.fix_text(new_text)
        else:
            return None

