from error import AnyError

######################################################################
# Class to mainly check brackets 
######################################################################
class SyntaxCheck:

    def __init__(self):
        pass

    ######################################################################
    # Keeps track of number of brackets seen till now
    ######################################################################
    def cont_check(self, line):
        brack_cnt = 0
        for char in line:
            if char == '(':
                brack_cnt += 1
            elif char == ')':
                brack_cnt -= 1
        if brack_cnt > 0:
            return False
        elif brack_cnt < 0:
            raise AnyError("Unmatched parantheses!!!")
        else:
            return True

    ######################################################################
    # Checks if all brackets are balanced
    ######################################################################
    def check_brack(self, line):
        brack_cnt = 0
        for char in line:
            if char == '(':
                brack_cnt += 1
            elif char == ')':
                brack_cnt -= 1
        if brack_cnt:
            raise AnyError("Unmatched parantheses!!!")
        else:
            return 1
