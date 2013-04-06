import re
import s_exp
import syntax
import main
import pyparsing
from error import AnyError

###################################################################### 
# This class is used to convert the s-expression string to a binary 
# tree
###################################################################### 
class ParseLisp:

    def __init__(self):
        self.replace_list = {'\( ':'(', ' \)':')', ' {1,}': ' ',
                             ' *\. *': '.'}
        self.syn = syntax.SyntaxCheck()



    def read_inp(self, i):
        if self.syn.check_brack(i):
            i = i.lower()
            for j, k in self.replace_list.iteritems():
                i = re.sub(j, k, i)
            i = i.strip('\n').replace(".", " . ")
            i = i.replace("()", "nil")
            main_l = pyparsing.nestedExpr('(',')').\
                    parseString(i).asList()[0]
            print main_l
            final_l = []
            #recursively construct the tree
            self.final_rec(main_l)
            return main_l 

    
    def final_rec(self, lst):
        if isinstance(lst, list):
            if "." not in lst:
                self.final_rec(lst[0])
                if len(lst) == 1:
                    lst.append('nil')
                    return
                lst[1] = lst[1:]
                lst[2:] = []
                if len(lst[1]) == 1:
                    lst[1].append("nil")
                    if isinstance(lst[1][0], list):
                        self.final_rec(lst[1][0])
                else:
                    self.final_rec(lst[1])
            else:
                lst.pop(lst.index("."))
                if "." in lst or len(lst) != 2:
                    raise AnyError("Invalid SExpression !")
                self.final_rec(lst[0])
                self.final_rec(lst[1])

if __name__ == '__main__':
    temp = ParseLisp('test.lisp')
    temp.read_inp()
