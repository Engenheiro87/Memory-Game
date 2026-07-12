
class Color3:
    COLORS = {
        "red":(255,0,0),
        "white":(255,255,255)
    };
    def __init__(self, red:int, green:int, blue:int):
        self.red = red;
        self.green = green;
        self.blue = blue;        

    def get_rgb(self)->tuple[int, int, int]:
        return (
            self.red,
            self.green,
            self.blue
        );

    @staticmethod
    def from_name(name:str)->Color3:
        color_stats = Color3.COLORS.get(name, (255,255,255));
        return Color3(*color_stats);
