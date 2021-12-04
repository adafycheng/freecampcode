import math

class Rectangle:
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def __str__(self):
    return f'Rectangle(width={self.width}, height={self.height})'

  def set_width(self, width):
    self.width = width

  def set_height(self, height):
    self.height = height

  def get_perimeter(self):
    return self.width * 2 + self.height * 2

  def get_area(self):
    return self.width * self.height

  def get_diagonal(self):
    return math.sqrt(self.width * self.width + self.height * self.height)

  def get_picture(self):
    picture = ""
    if self.height > 50 or self.width > 50:
      picture = "Too big for picture."
    else:
      for i in range(self.height):
        line = ""
        for j in range(self.width):
          line = line + "*"
        picture = picture + f'{line}\n'
    
    return picture

  def get_amount_inside(self, rect):
    widthNum = math.floor(self.width / rect.width)
    heightNum = math.floor(self.height / rect.height)

    return widthNum * heightNum

class Square(Rectangle):
  def __init__(self, side):
    self.side = side
    self.width = side
    self.height = side

  def __str__(self):
    return f'Square(side={self.side})'

  def set_side(self, side):
    self.side = side
    self.width = side
    self.height = side

  def set_width(self, width):
    self.side = width
    self.width = width
    self.height = width

  def set_height(self, height):
    self.side = height
    self.width = height
    self.height = height