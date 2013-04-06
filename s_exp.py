import main
from error import AnyError

###################################################################### 
# This class is pretty self explanatory. All operations which can be 
# done directly on s-expressions are defined here
###################################################################### 
class SExp:


    def __init__(self, atom_l):
        self.main_l = atom_l

    def add(self):
        try:
            return SExp(str(int(self.car().main_l) +\
                    int(self.cdr().car().main_l)))
        except (ValueError, TypeError):
            raise AnyError("Addition can be only between integer atoms")

    def sub(self):
        try:
            return SExp(str(int(self.car().main_l) -\
                    int(self.cdr().car().main_l)))
        except (ValueError, TypeError):
            raise AnyError("Minus can be only between integer atoms")

    def times(self):
        try:
            return SExp(str(int(self.car().main_l) *\
                    int(self.cdr().car().main_l)))
        except (ValueError, TypeError):
            raise AnyError("Times can be only between integer atoms")

    def quotient(self):
        try:
            return SExp(str(int(self.car().main_l) /\
                    int(self.cdr().car().main_l)))
        except (ValueError, TypeError):
            raise AnyError("Quotient can be only between integer atoms")

    def remainder(self):
        try:
            return SExp(str(int(self.car().main_l) %\
                    int(self.cdr().car().main_l)))
        except (ValueError, TypeError):
            raise AnyError("Remainder can be only between integer atoms")

    def less(self):
        try:
            if (int(self.car().main_l) < int(self.cdr().car().main_l)):
                temp = 't'
            else:
                temp = 'nil'
            return SExp(temp)
        except (ValueError, TypeError):
            raise AnyError("Less can be only between integer atoms")

    def greater(self):
        try:
            if (int(self.car().main_l) > int(self.cdr().car().main_l)):
                temp = 't'
            else:
                temp = 'nil'
            return SExp(temp)
        except (ValueError, TypeError):
            raise AnyError("Greater can be only between integer atoms")

    def car(self):
        if isinstance(self.main_l, list) and len(self.main_l) == 2:
            return SExp(self.main_l[0])
        else:
            raise AnyError("CAR can operate only on non-atom")

    def cdr(self):
        if isinstance(self.main_l, list) and len(self.main_l) == 2:
            return SExp(self.main_l[1])
        else:
            raise AnyError("CDR can operate only on non-atom")

    def atom(self):
        if isinstance(self.main_l, list):
            return SExp('nil')
        else:
            return SExp('t')

    def quote(self):
        return SExp(self.main_l[0])

    def cons(self, s1, s2):
        if isinstance(s1, SExp):
            return SExp([s1.main_l[:], s2.main_l[:]])
        else:
            return SExp([s1, s2])

    def isint(self):
        if isinstance(self.main_l, list):
            return False
        try:
            int(self.main_l)
            return True
        except (ValueError, TypeError):
            return False

    def eq(self, inp):
        if isinstance(inp, SExp):
            if isinstance(self.main_l, list) or \
                    isinstance(inp.main_l, list):
                raise AnyError("eq cannot have non atom as arg")
            if (self.main_l == inp.main_l):
                return SExp('t')
            else:
                return SExp('nil')
        else:
            if (self.main_l == inp):
                return SExp('t')
            else:
                return SExp('nil')

    def fint(self):
        if isinstance(self.main_l, list):
            return SExp('nil')
        try:
            int(self.main_l)
            return SExp('t')
        except (ValueError, TypeError):
            return SExp('nil')

    def null(self):
        if self.main_l == "nil":
            return SExp('t')
        else:
            return SExp('nil')

    def myint(self):
        if isinstance(self.main_l, list):
            return SExp('nil')
        try:
            int(self.main_l)
            return SExp('t')
        except (ValueError, TypeError):
            return SExp('nil')



