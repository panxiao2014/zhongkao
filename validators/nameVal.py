from prompt_toolkit.validation import Validator, ValidationError

class NameValidator(Validator):
    def validate(self, document):
        ok = (len(document.text) > 0 and len(document.text) < 6)
        if not ok:
            raise ValidationError(
                message = '请输入有效的姓名',
                cursor_position=len(document.text)
                )