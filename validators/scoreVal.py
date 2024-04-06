from prompt_toolkit.validation import Validator, ValidationError

class ScoreValidator150(Validator):
    def validate(self, document):
        score = int(document.text)
        ok = (score <= 150 and score >= 0)
        if not ok:
            raise ValidationError(
                message = '请输入正确的分数',
                cursor_position=len(document.text)
                )
        

class ScoreValidator70(Validator):
    def validate(self, document):
        score = int(document.text)
        ok = (score <= 70 and score >= 0)
        if not ok:
            raise ValidationError(
                message = '请输入正确的分数',
                cursor_position=len(document.text)
                )
        

class ScoreValidator50(Validator):
    def validate(self, document):
        score = int(document.text)
        ok = (score <= 50 and score >= 0)
        if not ok:
            raise ValidationError(
                message = '请输入正确的分数',
                cursor_position=len(document.text)
                )
        

class ScoreValidator60(Validator):
    def validate(self, document):
        score = int(document.text)
        ok = (score <= 60 and score >= 0)
        if not ok:
            raise ValidationError(
                message = '请输入正确的分数',
                cursor_position=len(document.text)
                )
        

class ScoreValidator20(Validator):
    def validate(self, document):
        score = int(document.text)
        ok = (score == 20 or score == 16 or score == 12 or score == 8)
        if not ok:
            raise ValidationError(
                message = '请输入正确的分数',
                cursor_position=len(document.text)
                )