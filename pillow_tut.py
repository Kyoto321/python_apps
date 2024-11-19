from PIL import Image, ImageFilter, ImageEnhance

with Image.open("image.webp") as pic:
    #pic.show()
    
    black_white = pic.convert("L")
    #black_white.save("image2.webp")
    
    mirror = pic.transpose(Image.FLIP_LEFT_RIGHT)
    #mirror.save("image3.webp")
    
    blur = pic.filter(ImageFilter.BLUR)
    #blur.save("image4.webp")
    
    # imaheEnhance
    contrast = ImageEnhance.Contrast(pic)
    contrast = contrast.enhance(2.4)
    #contrast.save("image5.webp")
    # or
    color = ImageEnhance.Color(pic).enhance(1.2)
    #color.save("image6.webp")
    
    
