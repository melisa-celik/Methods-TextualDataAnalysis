import os
from TextPreprocessingOperations.TextPreprocessor import TextPreprocessing

class Text:
    def __init__(self, input_folder, output_folder):
        self.inputFolder = input_folder
        self.outputFolder = output_folder

    def preprocessBooks(self):
        for fileName in os.listdir(self.inputFolder):
            if fileName.endswith('.txt'):
                inputPath = os.path.join(self.inputFolder, fileName)
                outputPath = os.path.join(self.outputFolder, fileName)
                with open(inputPath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    preprocessedText = TextPreprocessing().preprocessText(content)
                    preprocessedText = TextPreprocessing().removeStopwords(preprocessedText)
                    preprocessedText = TextPreprocessing().applyStemming(preprocessedText)
                    with open(outputPath, 'w', encoding='utf-8') as outputFile:
                        outputFile.write(preprocessedText)
