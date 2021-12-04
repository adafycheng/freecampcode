def arithmetic_arranger(problems, displayAns=False):
  if problems is None or problems=="":
    print("No Input")
    return "No input"

  finalOutput = ""
  problemDict = formatProblem(problems)
  if problemDict is None:
    print("Parse problems failed")
    return "Failed to parse problems."
  elif type(problemDict) is str:
    return problemDict
  else:
    x = len(problemDict)

    #
    # print 1st line
    #
    output = ""
    for i in range(x):
      operand1 = problemDict[i]["operand1"]
      padding = problemDict[i]["padding"]
      temp = f' {operand1 : >{padding}}'
      if output == "":
        output = temp
      else:
        output = output + "    " + temp
    finalOutput = output + "\n"

    #
    # print 2nd line
    #
    output = ""
    for i in range(x):
      operator = problemDict[i]["operator"]
      operand2 = problemDict[i]["operand2"]
      padding = problemDict[i]["padding"]
      temp = f'{operator}{operand2 : >{padding}}'
      if output == "":
        output = temp
      else:
        output = output + "    " + temp
    finalOutput = finalOutput + output + "\n"
    
    #
    # print 3rd line
    #
    output = ""
    filler = '-'
    for i in range(x):
      padding = problemDict[i]["padding"] + 1
      temp = f'{"" :{filler}<{padding}}'
      if output == "":
        output = temp
      else:
        output = output + "    " + temp
    finalOutput = finalOutput + output

    #
    # print answer line
    #
    if displayAns:
      output = ""
      for i in range(x):
        expression =  str(problemDict[i]["operand1"]) +  problemDict[i]["operator"] +  str(problemDict[i]["operand2"])
        padding = problemDict[i]["padding"] + 1
        temp = f'{eval(expression) : >{padding}}'
        if output == "":
          output = "\n" + temp
        else:
          output = output + "    " + temp
      finalOutput = finalOutput + output

  return finalOutput

#
# Find the padding
#
def findPadding(num1, num2):
  x = max(num1, num2)
  if x>1000:
    return 5
  if x>100:
    return 4
  if x>10:
    return 3
  if x>1:
    return 2

#
# Format the problems
#
def formatProblem(problems):
  problemDict = []
  dictIdx = 0
  if len(problems) > 5:
    return "Error: Too many problems."
  for problem in problems:
    idx = problem.find("+") 
    if (idx < 0):
      idx = problem.find("-")
      if (idx < 0):
        return "Error: Operator must be '+' or '-'."
    if not (problem[:idx].strip().isdigit() and not problem[idx+1].strip().isdigit()):
      return "Error: Numbers must only contain digits."
    try :
      operand1 = int(problem[:idx].strip())
      operand2 = int(problem[idx+1:].strip())
    except:
      return "Error: Numbers must only contain digits."
    if operand1 > 9999 or operand2 > 9999:
      return "Error: Numbers cannot be more than four digits."
    padding = findPadding(operand1, operand2)
    thisDict = {
      "idx": dictIdx,
      "operand1": operand1,
      "operator": problem[idx],
      "operand2": operand2,
      "padding": padding
    }
    problemDict.append(thisDict)
    dictIdx += 1
  return problemDict