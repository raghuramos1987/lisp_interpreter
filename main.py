import pdb
import s_exp as s_expf
import parse
import re
from error import AnyError
###################################################################### 
#Since eval and some other names are keywords in python. I have replaced 
#them as follows:
#
#    eval = seval
#    apply = sapply
#    s expressions = s_exp
###################################################################### 


class Main:

   ###################################################################### 
   #Constructor:
   #
   #    defunflag keeps track of whether defun has been already used at 
   #    the current level.
   #
   #    root_done is a flag which is set when the first level of seval 
   #    call is executed.
   ###################################################################### 

    def __init__(self):
        self.dlist = []
        self.parser = parse.ParseLisp()
        self.defunflag = 0
        self.root_done = 0
        self.standard_lst = ['car', 'cdr', 'plus', 'minus', 'plus', 
                'minus', 'times', 'quotient', 'remainder', 'less', 
                'greater', 'atom', 'quote', 'cons', 'eq', 'null', 
                'cond', 'defun', 't', 'nil']

   ###################################################################### 
   # Checks if s_exp is a part of the standard list of names defined in 
   # the constructor
   ###################################################################### 
    def isdefined(self, s_exp):
        if s_exp.main_l in self.standard_lst:
            return True
        else:
            return False

   ###################################################################### 
   #Validates that the atom passed to it is not a number
   ###################################################################### 
    def isimpossible(self, s_exp):
        self.regex = re.compile("^[0-9]+$")
        if self.regex.search(s_exp.main_l):
            return True
        else:
            return False
    
   ###################################################################### 
   # Find the length of the s_exp list lst and keep track in self.count
   ###################################################################### 
    def find_len(self, lst):
        if isinstance(lst.main_l, str):
            return
        self.count += 1
        if lst.cdr().main_l == 'nil':
            return
        self.find_len(lst.cdr())

   ###################################################################### 
   # eval
   ###################################################################### 
    def seval(self, s_exp, alist):
        #check if this s_exp is just the initial string
        if isinstance(s_exp, str):
            #if yes then convert it to a list of lists
            s_exp = s_expf.SExp(self.parser.read_inp(s_exp))
        self.root_done += 1
        if s_exp.atom().main_l != 'nil':
            if s_exp.isint():
                return s_exp
            elif s_exp.eq('t').main_l == 't':
                return s_expf.SExp('t')
            elif s_exp.eq('nil').main_l == 't':
                return s_expf.SExp('nil')
            elif self.isin(s_exp, alist):
                return self.getval(s_exp, alist, 0)
            else:
                raise AnyError("unbound variable")
        elif s_exp.car().atom().main_l == 't':
            self.count = 0
            self.find_len(s_exp.cdr())
            if s_exp.car().eq('quote').main_l == 't':
                #error checking
                if self.count != 1:
                    raise AnyError("Wrong number of args to quote")
                return s_exp.cdr().quote()
            elif s_exp.car().eq('cond').main_l == 't':
                return self.evcon(s_exp.cdr(), alist)
            elif s_exp.car().eq('defun').main_l == 't':
                self.check_defun(s_exp.cdr())
                #error checking
                if self.count != 3:
                    raise AnyError("Wrong number of args to defun")
                self.count = 0
                if self.root_done > 1:
                    raise AnyError("DEFUN used inside body")
                elif self.defunflag:
                    raise AnyError("defun at inner level")
                elif self.isdefined(s_exp.cdr().car()):
                    raise AnyError("cannot have function name same "+\
                            "as that of a keyword/standard function")
                elif self.isimpossible(s_exp.cdr().car()):
                    raise AnyError(s_exp.cdr().car().main_l+\
                            " is not a valid function name!!!")
                self.defunflag = 1
                self.dlist.append(s_exp.cdr())
                return s_exp.cdr().car()
            else:
                return self.sapply(s_exp.car(), self.evlis(s_exp.cdr(), 
                                                    alist), alist)
        else:
            raise AnyError("eval")

   ###################################################################### 
   # Error checking for defun
   ###################################################################### 
    def check_defun(self, s_exp):
        from out import Out
        myout = Out()
        if s_exp.car().atom().main_l != 't':
            raise AnyError("Funcion name should be an atom")
        if not myout.islist(s_exp.cdr().main_l) or \
                not myout.islist(s_exp.cdr().cdr().main_l):
            raise AnyError("Parameter list/body has to be a list")

   ###################################################################### 
   # Same as 'in' in slides
   ###################################################################### 
    def isin(self, s_exp, lst):
        for i in lst:
            if s_exp.main_l == i.car().main_l:
                return True
        return False

   ###################################################################### 
   # Same as getval in slides
   ###################################################################### 
    def getval(self, s_exp, lst, isdlist):
        lst.reverse()
        temp = lst[:]
        lst.reverse()
        if isdlist:
            for sl in temp:
                if sl.main_l[0] == s_exp.main_l:
                    return sl.cdr()
        else:
            for sl in temp:
                if sl.main_l[0] == s_exp.main_l:
                    return s_expf.SExp(sl.main_l[1])
        raise AnyError("error!!! getval")

   ###################################################################### 
   #apply
   ###################################################################### 
    def sapply(self, f, x, alist):
        err_fun = ""
        self.count = 0
        self.find_len(x)
        if f.atom().main_l != 't':
            raise AnyError("error!!! function name should be an atom")
        if f.eq('car').main_l == 't':
            if x.atom().main_l == 't':
                raise AnyError("CAR cannot operate on atom")
            if self.count == 1:
                self.count = 0
                return x.car().car()
            err_fun = "car"
        elif f.eq('cdr').main_l == 't':
            if x.atom().main_l == 't':
                raise AnyError("CDR cannot operate on atom")
            if self.count == 1:
                self.count = 0
                return x.car().cdr()
            err_fun = "cdr"
        elif f.eq('cons').main_l == 't':
            if x.atom().main_l == 't':
                raise AnyError("CAR cannot operate on atom")
            if self.count == 2:
                self.count = 0
                return f.cons(x.car(), x.cdr().car())
            err_fun = "cons"
        elif f.eq('atom').main_l == 't':
            if self.count == 1:
                self.count = 0
                return x.car().atom()
            err_fun = "atom"
        elif f.eq('int').main_l == 't':
            if self.count == 1:
                self.count = 0
                return x.car().fint()
            err_fun = "int"
        elif f.eq('null').main_l == 't':
            if self.count == 1:
                self.count = 0
                return x.car().null()
            err_fun = "null"
        elif f.eq('eq').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.car().eq(x.cdr().car())
            err_fun = "eq"
        elif f.eq('plus').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.add()
            err_fun = "eq"
        elif f.eq('minus').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.sub()
            err_fun = "minus"
        elif f.eq('times').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.times()
            err_fun = "times"
        elif f.eq('remainder').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.remainder()
            err_fun = "remainder"
        elif f.eq('quotient').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.quotient()
            err_fun = "quotient"
        elif f.eq('less').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.less()
            err_fun = "less"
        elif f.eq('greater').main_l == 't':
            if self.count == 2:
                self.count = 0
                return x.greater()
            err_fun = "greater"
        else:
            try:
                if self.isin(f, self.dlist):
                    self.addpairs(self.getval(f,\
                                            self.dlist, 1).car(),\
                                            x, alist)
                else:
                    raise AnyError("Function '"+f.main_l+\
                            "' not defined!!!")
            except AttributeError:
                raise AnyError("error!!! could not get parameters")
            temp = self.seval(self.getval(f, self.dlist, 1).cdr().\
                    car(), alist)
            self.count = 0
            self.find_len(x)
            while (self.count != 0):
                self.count -= 1 
                alist.pop()
            self.count = 0
            return temp

        raise AnyError("Wrong number of parameters to "+\
                "function '"+err_fun+"'")


   ###################################################################### 
   # Same as addpairs in slides 
   #
   # alist structure is as follows 
   # [['a', '1'], ['b', '2'], ...] 
   # where a, b are the parameter names and 1 and 2 are their respective 
   # values
   ###################################################################### 
    def addpairs(self, s_exp, x, alist):
        if x.main_l != 'nil' and s_exp.main_l != 'nil':
            alist.append(s_expf.SExp([s_exp.main_l[0], x.main_l[0]]))
        else:
            if x.main_l == s_exp.main_l:
                return
            else:
                raise AnyError("Parameter mismatch!")
        if isinstance(x.main_l, list) and len(x.main_l) == 2:
            self.addpairs(s_exp.cdr(), x.cdr(), alist)


   ###################################################################### 
   # Same as evcon in slides 
   ###################################################################### 
    def evcon(self, be, alist):
        if be.null().main_l == 't':
            raise AnyError("Atleast one condition should eval to T")
        elif self.seval(be.car().car(), alist).main_l != 'nil':
            return self.seval(be.car().cdr().car(), alist)
        else:
            return self.evcon(be.cdr(), alist)

   ###################################################################### 
   # Same as evlis in slides 
   ###################################################################### 
    def evlis(self, in_list, alist):
        if in_list.main_l == "nil":
            return s_expf.SExp("nil")
        else:
            return in_list.cons(self.seval(in_list.car(), alist), 
                    self.evlis(in_list.cdr(), alist))
