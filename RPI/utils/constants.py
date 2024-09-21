import os

class Constants:

    @staticmethod
    def white():
        return rgba(245,245,245)
    @staticmethod
    def darkGrey():
        return rgba(25,25,25)
    @staticmethod
    def black():
        return rgba(10,10,10)
    @staticmethod
    def blue():
        return rgba(10,10,245)
    
    @staticmethod
    def font():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(current_dir, '../Font.ttf')
    

def rgba(r, g, b, a=255):
    return (r/255, g/255, b/255, a/255)
