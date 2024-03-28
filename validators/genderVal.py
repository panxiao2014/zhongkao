from prompt_toolkit.validation import Validator, ValidationError

class GenderValidator(Validator):
    def validate(self, document):
        ok = (document.text == '男' or document.text == '女')
        if not ok:
            raise ValidationError(
                message = '请输入正确的性别',
                cursor_position=len(document.text)
                )