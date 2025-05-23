from prompt_toolkit.validation import Validator, ValidationError

import config.config as GlobalConfig

class SchoolValidator(Validator):
    def validate(self, document):
        if not document.text in GlobalConfig.LstSchoolCode:
            raise ValidationError(
                message = '请输入有效的学校代码',
                cursor_position=len(document.text)
                )