# PANG-KAT: A Dedicated Tokenizer for the Tagalog Language

import tkinter.filedialog
import re
import time
import csv
import json
from tkinter import *
from tkinter import ttk

from Setup.setupDictionaries import setupDictionaries
from Setup.groupLongerTokens import groupLongerTokenUnits
from Setup.setupTrueLabels import setupTrueLabels
from Setup.performanceEvaluation import performanceEvaluationMetrics

from Rules.begMarkPartialDup import begMarkPartialDupNoHyphen
from Rules.beginningMarker import beginningMarker
from Rules.partialReduplicationWithMarker import partialReduplicationWithMarker
from Rules.tagalogLargeNumber import tagalogLargeNumber
from Rules.englishLargeNumber import englishLargeNumber
from Rules.tagalogTimeExpression import tagalogTimeExpression
from Rules.numericTimeExpression import numericTimeExpression
from Rules.monthDateExpression import monthDateExpression
from Rules.commaExpression import commaExpression
from Rules.spacedNumber import spacedNumber
from Rules.juniorSenior import juniorSenior
from Rules.titleBeforeName import titleBeforeName
from Rules.abbreviation import abbreviation
from Rules.beModalNot import beModalNot
from Rules.groupingSymbols import groupingSymbols
from Rules.dateExpression import dateExpression
from Rules.timeIndicator import timeIndicator
from Rules.contractedNot import contractedNot
from Rules.apostrophe import apostrophe
from Rules.dashOrSlash import dashOrSlash
from Rules.percentage import percentage
from Rules.degree import degree
from Rules.basicMathOperation import basicMathOperation
from Rules.mathPrefixSymbol import mathPrefixSymbol
from Rules.mathPostfixSymbol import mathPostfixSymbol
from Rules.mwesAndDictionaryMatch import mwesAndDictionaryMatch
from Rules.noMatch import noMatch

# Function to exit and close the program
def exitPangkat(event):
    root.destroy()

# Function for inserting formatted data in an array
def arrayInserter (initial, destination):
    for data in initial:
        destination.append(data.strip().lower())

# Mutable state shared by the ordered token-labeling rules for one line.
class TokenizationState:
    def __init__(self, tokenTempList, labelTempList, **context):
        self.tokenTempList = tokenTempList
        self.labelTempList = labelTempList
        self.isDashDetected = False
        self.groupingSymbols = ""
        self.prefix = ""
        self.prevPrefix = ""
        self.beginningQuotesDetected = False
        self.i = 0

        for name, value in context.items():
            setattr(self, name, value)

# Class definition of PANG-KAT
class PANGKAT:
    # Initialize PANG-KAT'S GUI
    def __init__(self, master):
        # Initialize the lists for both the short and longer unit tokens and their corresponding labels
        self.tokenList = []
        self.labelList = []
        self.longerTokenList = []
        self.longerLabelList = []

        # self.trueTokenList = []
        # self.trueLabelList = []
        # self.longTrueTokenList = []
        # self.longTrueLabelList = []

        # fileReaderTrueLabels = open('Input/Data/External Validation/Articles/labelled-short-units.txt', 'r', encoding="utf-8")
        # trueLabels = fileReaderTrueLabels.readlines()

        # fileReaderLongTrueLabels = open('Input/Data/External Validation/Articles/labelled-longer-units.txt', 'r', encoding="utf-8")
        # longTrueLabels = fileReaderLongTrueLabels.readlines()
        
        # setupTrueLabels(trueLabels, self.trueTokenList, self.trueLabelList)
        # setupTrueLabels(longTrueLabels, self.longTrueTokenList, self.longTrueLabelList)

        self.master = master
        root.title("PANG-KAT: A Dedicated Tokenizer for the Tagalog Language")
        root.geometry("1250x750")
        root.resizable(False, False)
        self.mainMenu()

        print("PANGKAT is loaded!")
    
    # Function for toggling the displayed table values based on mouse clicks on the short unit or longer unit button
    # Parameters passed include the mouse click event and a boolean value: TRUE for short unit and FALSE for longer unit
    def toggleTable(self, event, value):

        # Delete all current table items
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Update defaultDisplay's value to update the table
        self.defaultDisplay = value
        if self.defaultDisplay == True:
            displayTokens = self.tokenList
            displayLabels = self.labelList
        else:
            displayTokens = self.longerTokenList
            displayLabels = self.longerLabelList
            
        # Re-populate the table
        for i in range(len(displayTokens)):
            for j in range(len(displayTokens[i])):
                token = displayTokens[i][j]
                label = displayLabels[i][j]
                data = (token, label)
                self.table.insert(parent = "", index = END, values = data)

            self.table.insert(parent = "", index = END, values = (" ", " "))
        
    # Function for saving PANGKAT's results in CSV format
    def saveResultsInCSV(self, event):
        outerIndex = 0
        innerIndex = 0

        # Identify whether to save short or longer unit tokenization results
        if self.defaultDisplay == True:
            toSaveTokens = self.tokenList
            toSaveLabels = self.labelList
        else:
            toSaveTokens = self.longerTokenList
            toSaveLabels = self.longerLabelList

        # Array to store the formatted data for CSV format
        toSaveList = []

        # Format the data to be saved in CSV 
        while outerIndex < len(toSaveTokens):
            sentenceList = []
            while innerIndex < len(toSaveTokens[outerIndex]):
                tempList = []
                tempList.append(toSaveTokens[outerIndex][innerIndex])
                tempList.append(toSaveLabels[outerIndex][innerIndex])
                sentenceList.append(tempList)
                innerIndex += 1
            
            toSaveList.append(sentenceList)
            outerIndex += 1
            innerIndex = 0

        print(toSaveList)

        # Save the results in CSV format, either for short or longer unit tokenization, respectively
        if self.defaultDisplay == True:
            with open('results-short-tokens.csv', mode='w', newline='', encoding = "UTF-8") as file:
                writer = csv.writer(file)

                outerSaveIndex = 0
                innerSaveIndex = 0

                while outerSaveIndex < len(toSaveList):
                    while innerSaveIndex < len(toSaveList[outerSaveIndex]):
                        writer.writerow(toSaveList[outerSaveIndex][innerSaveIndex])
                        innerSaveIndex += 1
                    writer.writerow([])
                    outerSaveIndex += 1
                    innerSaveIndex = 0    
        else:
            with open('results-longer-tokens.csv', mode='w', newline='', encoding = "UTF-8") as file:
                writer = csv.writer(file)

                outerSaveIndex = 0
                innerSaveIndex = 0

                while outerSaveIndex < len(toSaveList):
                    while innerSaveIndex < len(toSaveList[outerSaveIndex]):
                        writer.writerow(toSaveList[outerSaveIndex][innerSaveIndex])
                        innerSaveIndex += 1
                    writer.writerow([])
                    outerSaveIndex += 1
                    innerSaveIndex = 0

    # Function for saving PANGKAT's results in JSON format
    def saveResultsInJSON(self, event):
        outerIndex = 0
        innerIndex = 0

        # Identify whether to save short or longer unit tokenization results
        if self.defaultDisplay == True:
            toSaveTokens = self.tokenList
            toSaveLabels = self.labelList
        else:
            toSaveTokens = self.longerTokenList
            toSaveLabels = self.longerLabelList

        # Store each sentence in this array
        toSaveList = []

        # Format the data to be saved in JSON 
        while outerIndex < len(toSaveTokens):
            sentenceList = []
            while innerIndex < len(toSaveTokens[outerIndex]):
                tempList = []
                tempList.append(toSaveTokens[outerIndex][innerIndex])
                tempList.append(toSaveLabels[outerIndex][innerIndex])
                innerIndex += 1
                sentenceList.append(tempList)

            toSaveList.append(sentenceList)
            
            outerIndex += 1
            innerIndex = 0

        # Store sentences in a dictionary
        toSaveDict = {
            "sentences": toSaveList
        }

        # Save the results in JSON format, either for short or longer unit tokenization, respectively
        if self.defaultDisplay == True:
            with open('results-short-tokens.json', 'w', encoding= "UTF-8") as json_file:
                json.dump(toSaveDict, json_file, ensure_ascii=False)
        else:
            with open('results-longer-tokens.json', 'w', encoding= "UTF-8") as json_file:
                json.dump(toSaveDict, json_file, ensure_ascii=False)

    # Function for displaying PANG-KAT's results on its GUI
    def displayResults(self):

        # Destroy all current GUI children to refresh window
        for i in self.master.winfo_children():
            i.destroy()

        # Create background image
        self.bg = PhotoImage(file = "Input/Images/background.png")

        # Create Canvas 
        self.bgCanvas = Canvas(self.master, width = 1250, height = 750) 

        self.bgCanvas.pack(fill = "both", expand = True) 

        # Display image 
        self.bgCanvas.create_image( 0, 0, image = self.bg, anchor = "nw") 

        # Creates a rectangle of 50x60 (heightxwidth)
        self.bgCanvas.create_rectangle(125, 120, 925, 720,
                                outline = "black", fill = "black",
                                width = 2)
        # Create Buttons 
        self.shortButton = Button(self.bgCanvas, text = "SHORT UNIT", font = ("OpenSans-ExtraBold.ttf", "30", "bold"), bg = "#737373", fg = "white") 
        self.shortButtonCanvas = self.bgCanvas.create_window(124, 30, width = 400, height = 90, anchor = "nw", window = self.shortButton)

        # Create Buttons 
        self.longButton = Button(self.bgCanvas, text = "LONGER UNIT", font = ("OpenSans-ExtraBold.ttf", "30", "bold"), bg = "#737373", fg = "white") 
        self.longButtonCanvas = self.bgCanvas.create_window(526, 30, width = 400, height = 90, anchor = "nw", window = self.longButton)
        
        # Creating a photoimage object to use image 
        self.downloadLogo = PhotoImage(file = r"Input/Images/download.png", width = 50, height = 50)

        # Create Buttons 
        self.csvButton = Button(self.bgCanvas, text = " CSV", font = ("OpenSans-ExtraBold.ttf", "25", "bold"), bg = "#737373", fg = "white", image = self.downloadLogo, compound = LEFT)
        self.csvButtonCanvas = self.bgCanvas.create_window(925, 280, width = 250, height = 90, anchor = "nw", window = self.csvButton)

        # Create Buttons 
        self.jsonButton = Button(self.bgCanvas, text = " JSON", font = ("OpenSans-ExtraBold.ttf", "25", "bold"), bg = "#737373", fg = "white", image = self.downloadLogo, compound = LEFT)
        self.jsonButtonCanvas = self.bgCanvas.create_window(925, 430, width = 250, height = 90, anchor = "nw", window = self.jsonButton)

        # Initialize style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Create a frame to contain the table and its scrollbar
        self.tableFrame = ttk.Frame(self.bgCanvas, height = 25)
        self.tableFrame.pack(pady=20)

        # Create a scrollbar and position it at the right side of the frame
        self.tableScrollbar = Scrollbar(self.tableFrame)
        self.tableScrollbar.pack(side=RIGHT, fill=Y)

        # Initialize the table
        self.table = ttk.Treeview(self.tableFrame, columns = ("tokens", "labels"), show = "headings", height = 25, yscrollcommand=self.tableScrollbar.set)
        self.table.column("tokens",anchor=CENTER, stretch=NO, width=350)
        self.table.column("labels",anchor=CENTER, stretch=NO, width=350)
        self.table.heading("tokens", text = "TOKENS")
        self.table.heading("labels", text = "LABELS")
        self.table.pack()

        # Add the scroll bar to the table & position the table frame on the canvas
        self.tableScrollbar.config(command = self.table.yview)
        self.tableFrame.place(x = 173, y = 155)

        # Populate the table
        for i in range(len(self.tokenList)):
            for j in range(len(self.tokenList[i])):
                token = self.tokenList[i][j]
                label = self.labelList[i][j]
                data = (token, label)
                self.table.insert(parent = "", index = END, values = data)

            self.table.insert(parent = "", index = END, values = (" ", " "))

        # Bind the buttons with their respective event handlers
        self.shortButton.bind('<Button-1>', lambda event:self.toggleTable(event, True))
        self.longButton.bind('<Button-1>', lambda event:self.toggleTable(event, False))
        self.csvButton.bind('<Button-1>', self.saveResultsInCSV) 
        self.jsonButton.bind('<Button-1>', self.saveResultsInJSON) 

    # Detect a beginning-marker + partial reduplication before applying rules.
    def updatePartialReduplicationPrefix(self, state):
        for marker in state.beginningMarkers:
            state.prefix = begMarkPartialDupNoHyphen(state.tokenTempList, state.i, marker)
            if state.prefix != "":
                break

    # Handler function for applying rules
    def _apply_rules(self, state):
        for rule in self._rules:
            if rule(state):
                return

    # Defining the order of rules
    @property
    def _rules(self):
        return [
            beginningMarker,
            partialReduplicationWithMarker,
            tagalogLargeNumber,
            englishLargeNumber,
            tagalogTimeExpression,
            numericTimeExpression,
            monthDateExpression,
            commaExpression,
            spacedNumber,
            juniorSenior,
            titleBeforeName,
            abbreviation,
            beModalNot,
            groupingSymbols,
            dateExpression,
            timeIndicator,
            contractedNot,
            apostrophe,
            dashOrSlash,
            percentage,
            degree,
            basicMathOperation,
            mathPrefixSymbol,
            mathPostfixSymbol,
            mwesAndDictionaryMatch,
            noMatch
        ]

    # Function for tokenizing and labelling tokens
    def labelTokens(self, event):
        # Open filedialog and get selected file name
        fileName = tkinter.filedialog.askopenfilename(initialdir="./Input/Data")

        # start_time = time.time()

        # Open selected file for reading and store data per lines
        fileReader = open(fileName, 'r', encoding="utf-8")
        lines = fileReader.readlines()

        # Initialize defaultDisplay to True for displaying results
        self.defaultDisplay = True

        # Beginning markers are common markers located at the beginning of multi-word expressions of both Tagalog and Taglish
        # Multi-word expressions of this format may be written with or without hypen, which is common in colloquial writing
        # (Ex. magpapa-pedicure, magpapa pedicure)
        beginningMarkers = ["mga", "mag", "magka", "magpa", "magkaka", "magpapa", "maka", "makaka", "makapag", "makakapag", "mapag",
                             "nag", "nagka", "nagpa", "nagkaka", "nagpapa", "naka", "napapa", "nakaka", "nakapag", "nakakapag", "napaka", "napag", 
                             "pag", "pagka", "pagpa", "pagkaka", "pagpapa", "paka", "papapa", "pakaka", "pina", "pinag",
                             "ipa", "ipag", "ipinag", "ipinagka", "ipinagpa", "ipinagkaka", "ipinagpapa"]
        conflictingPrefixes = ["na", "ka", "ma", "pa"]
        combinedPrefixes = beginningMarkers + conflictingPrefixes
        # This array includes words which starting syllable can be contracted with an apostrophe
        firstLetterContraction = ["to", "tong", "kong", "ko", "cause", "yon", "yun", "yan", "yong", "yung", "yang", "no", "nong", "pag", "pagkat"]
        # This array includes verbs paired with the contraction of the word not
        contractedNot = ["don", "isn", "aren", "wasn", "weren", "can", "couldn", "won", "wouldn", "shan", "shouldn", "mustn", "mayn", "mightn", "doesn", "didn", "haven", "hasn", "hadn"]
        # This array includes Tagalog time indicators for Tagalog time expressions
        # "hating" and "madaling" refers to the first half of "hating gabi" and "madaling araw"
        tagalogTimeIndicators = ["umaga", "hapon", "tanghali", "gabi", "dapithapon", "hatinggabi", "hating", "madaling"]
        # THis array includes the Tagalog and English names of the days of the week
        daysOfTheWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
                         "lunes", "martes", "miyerkules", "huwebes", "biyernes", "sabado", "linggo"]

        # File reading of necessary datasets
        fileReaderTitlesStart = open('Input/Dictionary/daglat-titles-start.txt', 'r', encoding="utf-8")
        fileReaderTitlesEnd = open('Input/Dictionary/daglat-titles-end.txt', 'r', encoding="utf-8")
        fileReaderBeModelVers = open('Input/Dictionary/be-modal-verbs.txt', 'r', encoding="utf-8")
        fileReaderMonths = open('Input/Dictionary/daglat-months.txt', 'r', encoding="utf-8")
        personNEDict = open('Input/Dictionary/NE-PER-sorted.txt', 'r', encoding="utf-8")
        locationNEDict = open('Input/Dictionary/NE-LOC-sorted.txt', 'r', encoding="utf-8")
        organizationNEDict = open('Input/Dictionary/NE-ORG-sorted.txt', 'r', encoding="utf-8")
        MWEDict = open('Input/Dictionary/MWE-sorted.txt', 'r', encoding="utf-8")
        
        titlesStart = fileReaderTitlesStart.readlines()
        titlesEnd = fileReaderTitlesEnd.readlines()
        months = fileReaderMonths.readlines()
        personNEs = personNEDict.readlines()
        locationNEs = locationNEDict.readlines()
        organizationNEs = organizationNEDict.readlines()
        MWEs = MWEDict.readlines()
        beModalVerbs = fileReaderBeModelVers.readlines()

        # Initialization of all needed arrays and dictonaries
        titleBeforeList = []
        titleAfterList = []
        monthsList = []
        beModalVerbsList = []

        personNEList = []
        personNECountDict = {}
        personNEKeysList = []

        locationNEList = []
        locationNECountDict = {}
        locationNEKeysList = []

        organizationNEList = []
        organizationNECountDict = {}
        organizationNEKeysList = []

        MWEList = []
        MWECountDict = {}
        MWEKeysList = []

        # Storing data in their respective arrays
        arrayInserter(titlesStart, titleBeforeList)
        arrayInserter(titlesEnd, titleAfterList)
        arrayInserter(months, monthsList)
        arrayInserter(beModalVerbs, beModalVerbsList)

        # Setting up of the named entities and multi-word expressions dictionaries
        setupDictionaries(personNEs, personNEList, personNECountDict, personNEKeysList)
        setupDictionaries(locationNEs, locationNEList, locationNECountDict, locationNEKeysList)
        setupDictionaries(organizationNEs, organizationNEList, organizationNECountDict, organizationNEKeysList)
        setupDictionaries(MWEs, MWEList, MWECountDict, MWEKeysList)

        # Traverse each line in the selected file, which corresponds to the sentences in the file
        for line in lines:
            # Split the sentence into words and punctuations in tokenTempList
            tokenTempList = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", line)
            # Initialize the labelTempList based on the number of tokens in tokenTempList
            labelTempList = ["O"] * len(tokenTempList)

            state = TokenizationState(
                tokenTempList,
                labelTempList,
                beginningMarkers=beginningMarkers,
            conflictingPrefixes=conflictingPrefixes,
            combinedPrefixes=combinedPrefixes,
            firstLetterContraction=firstLetterContraction,
            contractedNot=contractedNot,
            tagalogTimeIndicators=tagalogTimeIndicators,
            daysOfTheWeek=daysOfTheWeek,
            titleBeforeList=titleBeforeList,
            titleAfterList=titleAfterList,
            monthsList=monthsList,
            beModalVerbsList=beModalVerbsList,
            personNEList=personNEList,
            personNECountDict=personNECountDict,
            personNEKeysList=personNEKeysList,
            locationNEList=locationNEList,
            locationNECountDict=locationNECountDict,
            locationNEKeysList=locationNEKeysList,
            organizationNEList=organizationNEList,
            organizationNECountDict=organizationNECountDict,
            organizationNEKeysList=organizationNEKeysList,
            MWEList=MWEList,
            MWECountDict=MWECountDict,
            MWEKeysList=MWEKeysList
            )

            while state.i < len(state.tokenTempList):
                self.updatePartialReduplicationPrefix(state)
                self._apply_rules(state)

            self.tokenList.append(state.tokenTempList)
            self.labelList.append(state.labelTempList)

        groupLongerTokenUnits(self.tokenList, self.labelList, self.longerTokenList, self.longerLabelList)

        # # print(len(self.trueTokenList))
        # # print(len(self.trueLabelList))
        # # print(len(self.tokenList))
        # # print(len(self.labelList))
        # accuracy, precision, recall, F1Score = performanceEvaluationMetrics(self.tokenList, self.labelList, self.trueTokenList, self.trueLabelList)

        # print("\nShort Unit Tokenization Test Results:")
        # print("\nAccuracy: " + str(accuracy))
        # print("\nPrecision: " + str(precision))
        # print("\nRecall: " + str(recall))
        # print("\nF1Score: " + str(F1Score))

        # # print(len(self.longTrueTokenList))
        # # print(len(self.longTrueLabelList))
        # # print(len(self.longerTokenList))
        # # print(len(self.longerLabelList))
        
        # accuracy, precision, recall, F1Score = performanceEvaluationMetrics(self.longerTokenList, self.longerLabelList, self.longTrueTokenList, self.longTrueLabelList)
        # print("\nLonger Unit Tokenization Test Results:")
        # print("\nAccuracy: " + str(accuracy))
        # print("\nPrecision: " + str(precision))
        # print("\nRecall: " + str(recall))
        # print("\nF1Score: " + str(F1Score))

        # print("--- %s seconds ---" % (time.time() - start_time))

        print("Tokenization process completed!")

        self.displayResults()

    def start(self, event):
        # Destroy all current GUI children to refresh window
        for i in self.master.winfo_children():
            i.destroy()

        # Create background image
        self.bg = PhotoImage(file = "Input/Images/background.png")

        # Create Canvas 
        self.bgCanvas = Canvas(self.master, width = 1250, height = 750) 

        self.bgCanvas.pack(fill = "both", expand = True) 

        # Display image 
        self.bgCanvas.create_image( 0, 0, image = self.bg,  anchor = "nw") 

        # Creates a rectangle of 50x60 (heightxwidth)
        self.bgCanvas.create_rectangle(225, 225, 1025, 500,
                                outline = "black", fill = "black",
                                width = 2)
        
        # Create Buttons 
        self.fileButton = Button(self.bgCanvas, text = "CHOOSE A FILE", font = ("OpenSans-ExtraBold.ttf", "40", "bold"), bg = "#737373", fg = "white") 
        self.fileButtonCanvas = self.bgCanvas.create_window(330, 305, width = 585, height = 109, anchor = "nw", window = self.fileButton)
        self.fileButton.bind('<Button-1>', self.labelTokens) 


    def mainMenu(self):
        # Destroy all current GUI children to refresh window
        for i in self.master.winfo_children():
            i.destroy()

        # Create background image
        self.bg = PhotoImage(file = "Input/Images/background.png")

        # Create Canvas 
        self.bgCanvas = Canvas(self.master, width = 1250, height = 750) 

        self.bgCanvas.pack(fill = "both", expand = True) 

        # Display image 
        self.bgCanvas.create_image( 0, 0, image = self.bg,  anchor = "nw") 

        # Add Text 
        self.bgCanvas.create_text(620, 225, text = "PANG-KAT", font = ("OpenSans-ExtraBold.ttf", "125", "bold"), fill = "white") 

        # Create Buttons 
        self.startButton = Button(self.bgCanvas, text = "START", font = ("OpenSans-ExtraBold.ttf", "65", "bold"), bg = "#737373", fg = "white") 
        # startButton.pack(pady=20) 
        self.exitButton = Button(self.bgCanvas, text = "EXIT", font = ("OpenSans-ExtraBold.ttf", "65", "bold"), bg = "#737373", fg = "white") 
        # exitButton.pack(pady=20) 
        self.startButtonCanvas = self.bgCanvas.create_window(330, 375, width = 585, height = 109, anchor = "nw", window = self.startButton) 
        self.exitButtonCanvas = self.bgCanvas.create_window(330, 525, width = 585, height = 109, anchor = "nw", window = self.exitButton) 

        # Bind the buttons with their respective event handlers
        self.exitButton.bind('<Button-1>', exitPangkat)
        self.startButton.bind('<Button-1>', self.start)
     
# Start PANG-KAT
root = Tk()
app = PANGKAT(root)
root.mainloop()