from re import search
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class ca_imaging():
    def __init__(self, file = None):
        if not file:
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            self.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        else:
            self.filename = file
        self.import_data()

    def isalsym(self, word):
        return search(r"[A-Za-z#\(\)/]+", word)

    def addValues(self, sheet, values):
        temp_vals = []
        for i in values:
            if i != "":
                temp_vals.append(i)
        if len(sheet) != len(temp_vals):
            print("error: mismatching lengths")
            print(sheet)
            print(temp_vals)
        else:
            for i in range(0,len(temp_vals)):
                sheet[i].append(float(temp_vals[i]))

    def import_data(self):
        self.time = []
        self.sheet = []
        with open(self.filename) as f:
            for line in f.readlines():
                items = line.strip().split("\t")
                if self.isalsym(items[0]):
                    for item in items:
                        if search("[A-Za-z]+",item) and not search("Time", item):
                            self.sheet.append([])                    
                elif items[0] != "":
                    self.time.append(float(items[0]))
                    self.addValues(self.sheet, items[1:])

    def __str__(self):
        length = len(self.time)
        width = len(self.sheet)
        out = ""
        for i in range(0, length):
            out += "{}".format(self.time[i])
            for j in range(0, width):
                out += "\t{}".format(self.sheet[j][i])
            out += "\n"
        return out

    def mean(self, vals):
        sum = 0.0
        for i in vals:
            sum += float(i)
        return sum/len(vals)

    def analysis(self):
        baselines = []
        peaks = []
        decays = []
        for roi in self.sheet:
            for avgTime in range(20, len(roi)):
                avg = self.mean(roi[avgTime - 20:avgTime - 1])
                if roi[avgTime] >= avg * 1.05:
                    baselines.append(avg)
                    peaks.append(max(roi))
                    break
            peak = max(roi)
            peakTime = roi.index(peak)
            for time in range(peakTime, len(roi)):
                if roi[time] <= .4*(peak-avg) + avg:
                    decays.append(self.time[time] - self.time[peakTime])
                    break
        print(baselines)
        print(

            
        for baseline, peak, decay in zip(baselines, peaks, decays):
            print("Baseline: {}\nPeak: {}\nAmplitude: {}\nTime to decay: {}\n".format(baseline, peak, peak - baseline, decay))
                    
                    
                
                
            
                

a = ca_imaging("C:/Users/M113455/Desktop/ca.txt")
a.analysis()
    
