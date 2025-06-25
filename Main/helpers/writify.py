
import import_libary as import_libary

def writify_method(thing):
    with open("html_checker", "w") as f:
        
        # If thing is a list
        if (type(thing) is list):
            for i in thing:
                string_of = str(i[0][1]) + ", "
                f.write(string_of)
        else:
            f.write(thing)
            
