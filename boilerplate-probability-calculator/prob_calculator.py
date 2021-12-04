import copy
import random
# Consider using the modules imported above.

class Hat:
  def __init__(self, **args):
    self.contents = []
    for color, colorNum in args.items():
      for n in range(colorNum):
        self.contents.append(color)

  def draw(self, drawNum):
    #contentsList = self.contents.copy()
    drawnList = []
    if drawNum >= len(self.contents):
      drawnList = self.contents.copy()
    else :
      # Draw the balls
      for n in range(drawNum):
        idxMax = len(self.contents) - 1
        drawnIdx = random.randint(0, idxMax)

        # Update balls in hat
        drawnBall = self.contents.pop(drawnIdx)

        # Update list of balls drawn
        drawnList.append(drawnBall)

    return drawnList


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
  passNum = 0

  for n in range(num_experiments):
    copiedHat = copy.deepcopy(hat)
    drawnList = copiedHat.draw(num_balls_drawn)
  
    drawnDict = {}
    for n in range(len(drawnList)):
      color = drawnList[n]
      drawnCount = drawnDict.get(color)
      if drawnCount == None:
        drawnCount = 0
      drawnCount = drawnCount + 1
      drawnDict.update({color: drawnCount})

    # Check result
    colorMatchCount = 0
    for color, colorCount in expected_balls.items():
      drawnCount = drawnDict.get(color)
      if drawnCount == None:
        break
      if drawnCount >= colorCount:
        colorMatchCount = colorMatchCount + 1
    if colorMatchCount >= len(expected_balls):
      passNum = passNum + 1

  return passNum/num_experiments
