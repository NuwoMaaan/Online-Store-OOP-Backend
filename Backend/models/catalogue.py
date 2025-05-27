

class Catalogue:
    __instance = None
    
    def __init__(self):
        if Catalogue.__instance is not None:
            raise Exception("Singleton class cannot be instantiated more than once.")
        else:
            Catalogue.__instance = self
    
    @staticmethod
    def get_instance():
        if Catalogue.__instance is None:
            Catalogue()
        return Catalogue.__instance
    


   