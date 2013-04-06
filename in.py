#!/usr/bin/python
import parse
import traceback
import syntax
import main
import s_exp
from error import AnyError
import out
import pyparsing
global debug
#to print stack trace on error, set this
debug = 0

######################################################################
# Input class
######################################################################
class In:

    def __init__(self):
        self.out = out.Out()
        self.syn = syntax.SyntaxCheck()
        self.main = main.Main()
        tot = ""
        print "Hit Ctrl+C to quit !!!"
        flag = 1
        while(1):
            try:
                if tot == "" and flag:
                    print "ONTI_LISP>",
                    flag = 0
                i = sys.stdin.readline()
                i = str(i)
                if i != "\n" and not i.isspace() and not i == "":
                    i = i.strip("\n")
                    tot += i
                    if not self.syn.cont_check(tot):
                        tot += " "
                        continue
                    if tot.startswith(';'):
                        continue
                    import re
                    temp = re.compile("^[0-9]+$")
                    i = i.lower()
                    if temp.search(i) or i in ['t', 'nil']:
                        print i
                        flag = 1
                        tot = ""
                        continue
                    temp = self.main.seval(str(tot), [])
                    if isinstance(temp, s_exp.SExp):
                        if not self.main.defunflag:
                            print self.out.final_get(temp.main_l)
                        else:
                            print temp.main_l
                    else:
                        print temp, "error in in"
            except (AnyError, RuntimeError), e:
                if debug:
                    print traceback.format_exc()
                print e
            except KeyboardInterrupt:
                print "Bye!"
                break
            except IndexError:
                if debug:
                    print traceback.format_exc()
                print "Error!!! CDR/CAR on atom"
            except EOFError:
                break
            except pyparsing.ParseException:
                print "Unmatched Parantheses!!!"
            except ZeroDivisionError:
                print "Please dont try to divide by 0"

            flag = 1
            tot = ""
            self.main.defunflag = 0
            self.main.root_done = 0
            
            

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(2500)
    temp = In()
