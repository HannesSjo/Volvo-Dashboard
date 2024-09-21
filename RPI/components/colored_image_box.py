from components.image_box import ImageBox


class ColoredImageBox(ImageBox):
    thresh1 = 30
    thresh2 = 60
    normal_color = (0, 0.9, 0)
    thresh1_color = (0.9, 0.9, 0)
    thresh2_color = (0.9, 0, 0)

    def __init__(self, 
                 layout,
                 img_src,
                 pos=...,
                 align_left=True,
                 thresh1=thresh1,
                 thresh2=thresh2,
                 normal_color=normal_color,
                 thresh1_color=thresh1_color,
                 thresh2_color=thresh2_color,
                 **kwargs):
        super().__init__(layout, img_src, pos, align_left, **kwargs)
        self.thresh1 = thresh1
        self.thresh2 = thresh2
        self.normal_color = normal_color
        self.thresh1_color = thresh1_color
        self.thresh2_color = thresh2_color

    def Update(self, new_val, format="{:.0f}"):
        super().Update(new_val, format)
        if new_val < self.thresh1:
            self.image.color = self.thresh1_color
            self.label.color = self.thresh1_color
        elif new_val > self.thresh2:
            self.image.color = self.thresh2_color
            self.label.color = self.thresh2_color
        else:
            self.image.color = self.normal_color
            self.label.color = self.normal_color
