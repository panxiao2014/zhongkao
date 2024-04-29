from prompt_toolkit.validation import Validator, ValidationError

import config.config as GlobalConfig

class StudentNameValidator(Validator):
    def validate(self, document):
        if ((not document.text in GlobalConfig.StuNameLst) and (not document.text+"(mySelf)" in GlobalConfig.StuNameLst)):
            raise ValidationError(
                message = '查无此人，请重新输入',
                cursor_position=len(document.text)
                )