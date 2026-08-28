# PANG-KAT: A Dedicated Tokenizer for the Tagalog Language
import re

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
    def __init__(self):
        # Initialize the lists for both the short and longer unit tokens and their corresponding labels
        self.tokenList = []
        self.labelList = []
        self.longerTokenList = []
        self.longerLabelList = []

        # self.trueTokenList = []
        # self.trueLabelList = []
        # self.longTrueTokenList = []
        # self.longTrueLabelList = []

        # fileReaderTrueLabels = open('Input/Data/External Validation/NewsPh/labelled-short-units.txt', 'r', encoding="utf-8")
        # trueLabels = fileReaderTrueLabels.readlines()

        # fileReaderLongTrueLabels = open('Input/Data/External Validation/NewsPh/labelled-longer-units.txt', 'r', encoding="utf-8")
        # longTrueLabels = fileReaderLongTrueLabels.readlines()
        
        # setupTrueLabels(trueLabels, self.trueTokenList, self.trueLabelList)
        # setupTrueLabels(longTrueLabels, self.longTrueTokenList, self.longTrueLabelList)

        print("PANGKAT is loaded!")
        # print(__file__)

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
    def labelTokens(self, fileName):

        # Open selected file for reading and store data per lines
        fileReader = open(fileName, 'r', encoding="utf-8")
        lines = fileReader.readlines()

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
        fileReaderTitlesStart = open('Dictionary/daglat-titles-start.txt', 'r', encoding="utf-8")
        fileReaderTitlesEnd = open('Dictionary/daglat-titles-end.txt', 'r', encoding="utf-8")
        fileReaderBeModelVers = open('Dictionary/be-modal-verbs.txt', 'r', encoding="utf-8")
        fileReaderMonths = open('Dictionary/daglat-months.txt', 'r', encoding="utf-8")
        personNEDict = open('Dictionary/NE-PER-sorted.txt', 'r', encoding="utf-8")
        locationNEDict = open('Dictionary/NE-LOC-sorted.txt', 'r', encoding="utf-8")
        organizationNEDict = open('Dictionary/NE-ORG-sorted.txt', 'r', encoding="utf-8")
        MWEDict = open('Dictionary/MWE-sorted.txt', 'r', encoding="utf-8")

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

        return self.tokenList, self.labelList, self.longerTokenList, self.longerLabelList