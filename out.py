######################################################################
# Class to convert evaluated tree to string 
######################################################################
class Out:

    def __init__(self):
        self.main_str = ""


    ######################################################################
    # Checks if lst is a lisp list
    ######################################################################
    def islist(self, lst):
        if not isinstance(lst, list):
            if lst == 'nil':
                return True
            else:
                return False
        return self.islist(lst[1])

    ######################################################################
    # Strips one leading char
    ######################################################################
    def mystrip(self, my_str, char):
        if my_str[0] == char:
            my_str = my_str[1:]
        return my_str

    ######################################################################
    # Recursive call to traverse the tree and construct the string
    ######################################################################
    def final_get(self, lst):
        if isinstance(lst, list):
            if isinstance(lst[1], list):
                if self.islist(lst[1]):
                    temp = "("+self.final_get(lst[0])+" "+\
                            self.mystrip(self.final_get(lst[1]), "(")
                else:
                    temp = "("+self.final_get(lst[0])+"."+\
                            self.final_get(lst[1])+")"
            elif lst[1] == 'nil':
                temp = "("+self.final_get(lst[0])+")"
            else:
                temp = "("+self.final_get(lst[0])+"."+lst[1]+")"
            return temp
        else:
            return str(lst)

if __name__ == "__main__":
    a = Out()
    print "("+a.get_str(['3',['1',[['2','4'],'nil']]]).strip(" ")

