import tkinter as tk
import pointHandling as ph

class PointGui:
  def __init__(self):
    # ------------------ GUI ------------------
    self.master = tk.Tk()
    self.master.title("Robot calibration")
    self.master.geometry("1000x300")
    self.master.resizable(False, False)
    self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
    # Make 10x10 grid
    self.cntColumns = 7
    self.cntRows = 7
    for i in range(self.cntColumns):
      if i%2 == 0:
        # make smaller columns
        self.master.columnconfigure(i, weight=1)
      else:
        # make equal columns
        self.master.columnconfigure(i, weight=2)
    
    # make cntRows equal rows
    for i in range(self.cntRows):
      self.master.rowconfigure(i, weight=1)

    # # draw grid lines
    # for i in range(self.cntColumns):
    #   tk.Frame(self.master, height=1, width=1, bg="blue").grid(row=0, column=i, rowspan=12, sticky="ns")
    # for i in range(self.cntRows):
    #   tk.Frame(self.master, height=1, width=1, bg="red").grid(row=i, column=0, columnspan=12, sticky="we")

    # ------------------ Labels ------------------
    self.coordRow = 2 # +1 is reserved for coord values
    self.chooseRow = 1
    self.buttonRow = 0
    self.buttonColumn = 3

    self.label1 = tk.Label(self.master, text="Point name:")
    self.label1.grid(row=0, column=0, sticky="nsew")
    self.label4 = tk.Label(self.master, text="X/1")
    self.label4.grid(row=self.coordRow, column=0, sticky="nsew")
    self.label5 = tk.Label(self.master, text="Y/2	")
    self.label5.grid(row=self.coordRow, column=1, sticky="nsew")
    self.label6 = tk.Label(self.master, text="Z/3")
    self.label6.grid(row=self.coordRow, column=2, sticky="nsew")
    self.label7 = tk.Label(self.master, text="Roll/4")
    self.label7.grid(row=self.coordRow, column=3, sticky="nsew")
    self.label8 = tk.Label(self.master, text="Pitch/5")
    self.label8.grid(row=self.coordRow, column=4, sticky="nsew")
    self.label9 = tk.Label(self.master, text="Yaw/6")
    self.label9.grid(row=self.coordRow, column=5, sticky="nsew")
    self.label2 = tk.Label(self.master, text="Point type:")
    self.label2.grid(row=self.coordRow, column=6, sticky="nsew")

    self.points = ph.pointHandler()

    # make drpdown menu for point names
    self.updateOptionMenu()

    # make empty entry for point position
    self.pointPosition = []
    for i in range(7):
      self.pointPosition.append(tk.StringVar(self.master))
      self.pointPosition[i].set(self.points.points.iloc[0, i+1])
    
    self.entryHeight = 5
    self.entryWidth = 18

    self.pointX = tk.Entry(self.master, textvariable=self.pointPosition[0], width=self.entryWidth)
    self.pointX.grid(row=self.coordRow+1, column=0, sticky="w")
    self.pointY = tk.Entry(self.master, textvariable=self.pointPosition[1], width=self.entryWidth)
    self.pointY.grid(row=self.coordRow+1, column=1, sticky="w")
    self.pointZ = tk.Entry(self.master, textvariable=self.pointPosition[2], width=self.entryWidth)
    self.pointZ.grid(row=self.coordRow+1, column=2, sticky="w")
    self.pointRoll = tk.Entry(self.master, textvariable=self.pointPosition[3], width=self.entryWidth)
    self.pointRoll.grid(row=self.coordRow+1, column=3, sticky="w")
    self.pointPitch = tk.Entry(self.master, textvariable=self.pointPosition[4], width=self.entryWidth)
    self.pointPitch.grid(row=self.coordRow+1, column=4, sticky="w")
    self.pointYaw = tk.Entry(self.master, textvariable=self.pointPosition[5], width=self.entryWidth)
    self.pointYaw.grid(row=self.coordRow+1, column=5, sticky="w")
    self.pointType = tk.Entry(self.master, textvariable=self.pointPosition[6], width=self.entryWidth)
    self.pointType.grid(row=self.coordRow+1, column=6, sticky="w")

    # add small + and - buttons to change point position near each entry
    self.pointXplus = tk.Button(self.master, text="+", command=lambda: self.changePointPosition('x', '+'), width=1, height=1)
    self.pointXplus.grid(row=self.coordRow+1, column=0, sticky="ne", padx=3)
    self.pointXminus = tk.Button(self.master, text="-", command=lambda: self.changePointPosition('x', '-'), width=1, height=1)
    self.pointXminus.grid(row=self.coordRow+1, column=0, sticky="se", padx=3)
    

      
    # make buttons
    self.addButton =    tk.Button(self.master, text="Add", command=self.addPoint)
    self.addButton.grid(row=self.buttonRow, column=self.buttonColumn, sticky="nsew")
    self.addButton =    tk.Button(self.master, text="Edit", command=self.editPoint)
    self.addButton.grid(row=self.buttonRow, column=self.buttonColumn+1, sticky="nsew")
    self.removeButton = tk.Button(self.master, text="Remove", command=self.removePoint)
    self.removeButton.grid(row=self.buttonRow, column=self.buttonColumn+2, sticky="nsew")
    self.saveButton =   tk.Button(self.master, text="Save", command=self.savePoints)
    self.saveButton.grid(row=self.buttonRow, column=self.buttonColumn+3, sticky="nsew")

  def updateOptionMenu(self):
    self.pointName = tk.StringVar(self.master)
    self.pointName.set(self.points.points['name'].values[0])
    self.pointNameMenu = tk.OptionMenu(self.master, self.pointName, 
                                       *self.points.points['name'].values, command=self.updatePointPosition)
    self.pointNameMenu.grid(row=0, column=1, sticky="nsew")

  def updatePointPosition(self, pointName):
    print(self.pointName)
    self.pointPosition = []
    for i in range(7):
      self.pointPosition.append(tk.StringVar(self.master))
      # get point position of pointName
      self.pointPosition[i].set(self.points.points[self.points.points['name'] == pointName].iloc[0, i+1])
      
    self.pointX.config(textvariable=self.pointPosition[0])
    self.pointY.config(textvariable=self.pointPosition[1])
    self.pointZ.config(textvariable=self.pointPosition[2])
    self.pointRoll.config(textvariable=self.pointPosition[3])
    self.pointPitch.config(textvariable=self.pointPosition[4])
    self.pointYaw.config(textvariable=self.pointPosition[5])
    self.pointType.config(textvariable=self.pointPosition[6])

  def changePointPosition(self, whichCoord, operation):
    self.coordValue = 0
    if whichCoord == 'x':
      # get current value of x
      self.coordValue = float(self.pointX.get())
      
      # add or subtract 0.1
      self.coordValue = round(self.doMath(operation, self.coordValue), 2)

      # set new value of x
      self.pointX.delete(0, tk.END)
      self.pointX.insert(0, self.coordValue)

  def doMath(self, operation, value):
    self.coordValue = value
    if operation == '+':
      self.coordValue += 0.1
    elif operation == '-':
      self.coordValue -= 0.1

    return self.coordValue

  def addPoint(self):
    # make new window to enter point name and type
    self.addWindow = tk.Toplevel(self.master)
    self.addWindow.title("Add Point")
    
    # set size of window
    self.addWindow.geometry("250x80")

    #set grid layout
    self.addWindow.grid_columnconfigure(0, weight=1)
    self.addWindow.grid_columnconfigure(1, weight=1)
    self.addWindow.grid_rowconfigure(0, weight=1)
    self.addWindow.grid_rowconfigure(1, weight=1)

    # make entry for point name
    self.addPointName = tk.StringVar(self.addWindow)
    self.addPointName.set("point name")

    self.addPointNameEntry = tk.Entry(self.addWindow, textvariable=self.addPointName, width=20)
    self.addPointNameEntry.grid(row=0, column=0, sticky="")

    # make dropdown menu for point type
    self.addPointType = tk.StringVar(self.addWindow)
    self.addPointType.set("point type")

    self.addPointTypeMenu = tk.OptionMenu(self.addWindow, self.addPointType, *['coordinate', 'angle'])
    self.addPointTypeMenu.grid(row=0, column=1, sticky="")

    # make button to add point
    self.addPointButton = tk.Button(self.addWindow, text="Add Point", command=lambda: self.addPointToPoints(self.addWindow, self.addPointName.get(), self.addPointType.get()))
    self.addPointButton.grid(row=1, column=0, sticky="")

  def addPointToPoints(self, newWindow, pointName, pointType):
    # check if point type is valid
    print(pointType)
    if pointType != 'point type':
      # check if point name is already in points
      if pointName in self.points.points['name'].values:
        # change color of entry to red
        self.addPointNameEntry.config(bg="red")

      else:
        # add point to points
        self.points.addPoint(pointName, pointType, [self.pointX.get(), self.pointY.get(),
                             self.pointZ.get(), self.pointRoll.get(), self.pointPitch.get(),
                             self.pointYaw.get()])
        
        # update point dropdown menu
        self.updateOptionMenu()

        # close window
        newWindow.destroy()
    
    else :
      # change color of entry to red
      self.addPointTypeMenu.config(bg="red")

  def editPoint(self):
    self.points.editPoint(self.pointName.get(), [self.pointX.get(), self.pointY.get(),
                              self.pointZ.get(), self.pointRoll.get(), self.pointPitch.get(),
                              self.pointYaw.get()])

    pass

  def removePoint(self):
    try:
      self.points.removePoint(self.pointName.get())
      self.updateOptionMenu()
    except:
      print("No point exists to remove")

  def savePoints(self):
    self.points.savePoints()





  



def main():
  gui = PointGui()

  gui.master.mainloop()

if __name__ == "__main__":
  main()