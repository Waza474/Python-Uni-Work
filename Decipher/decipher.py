'''
Functionality of the function
Time complexity:
Space complexity:
Error handle:
Return:
Parameter:
Pre-requisite:
'''

class Decipher():
    def __init__(self):
        self.message = ''

    def messageFind(self,filename):
        '''
        Gets 2 strings from an input file and finds the longest common substring
        via a dynamic programming approach
        Time complexity: All Cases O(nm)
        Space complexity: O(nm), a table of size n by m
        Error handle: Invalid filename crash prevention
        Return: N/A
        Parameter: filename: Name of file with 2 strings for decryption
        Pre-requisite: N/A
        '''

        try:
            txtfile = open(filename)
        except:
            return

        # Puts the 2 encrypted words into seperate words
        wordA = False
        wordB = False
        i = 0
        for line in txtfile:
            if i == 0:
                wordA = line[:-1]
            else:
                wordB = line
            i += 1

        # There must be 2 words with text
        if wordA == False or wordB == False:
            return

        # Initialise 'memo' table
        # Size O(n*m)
        m = len(wordB)
        memo = []
        while m >= 0:
            memo.append([0]*(len(wordA)+1))
            m -= 1

        # Use dp approach to fill memo table
        currentRow = 1
        while currentRow <= len(wordB):
            currentCol = 1
            while currentCol <= len(wordA):
                if wordB[currentRow-1] == wordA[currentCol-1]:
                    memo[currentRow][currentCol] = memo[currentRow-1][currentCol-1] + 1
                else:
                    memo[currentRow][currentCol] = max(memo[currentRow][currentCol-1],memo[currentRow-1][currentCol])
                currentCol += 1
            currentRow += 1

        # Tracing back to find longest sub sequence
        # currentRow and currentCol, can still be used as it now points to bottom right...
        # the starting point
        currentRow -= 1
        currentCol -= 1
        TempFinalWord = []
        #print(currentRow,currentCol)
        while currentCol >= 0 and currentRow >= 0:
            if memo[currentRow-1][currentCol-1] == memo[currentRow][currentCol] - 1 and wordB[currentRow-1] == wordA[currentCol-1]:
                currentRow -= 1
                currentCol -= 1
                TempFinalWord.append(wordA[currentCol])
            else:
                if memo[currentRow][currentCol-1] > memo[currentRow-1][currentCol]:
                    currentCol -= 1
                else:
                    currentRow -= 1

        # Reverse the list that was made before to the right order
        while len(TempFinalWord) != 0:
            self.message += TempFinalWord.pop()
        return

    def wordBreak(self, filename):
        '''
        Gets a string and breaks into words from given dictionary
        Time complexity: O(KM*MN) All Cases
        Space complexity: O(KM + NM), has list size K (input string) with strings possibly consisting of worst M
                        NM, being size of dictionary
        Error handle: Invalid filename crash prevention
        Return: N/A
        Parameter: Name of dictionary file
        Pre-requisite: Format of messageFind output
        '''

        try:
            txtfile = open(filename)
        except:
            return


        # Get the text file into a list for use
        i = 0
        library = []
        for line in txtfile:
            if line[-1] == '\n':
                library.append(line[:-1])
            else:
                library.append(line)
        # If the dictionary file is empty, quit early
        if len(library) == 0:
            return

        DecryptedWord = self.message

        # break the word via a DP approach
        table = [None] * len(DecryptedWord)
        i = len(DecryptedWord) - 1
        lastpoint = i
        endpoint = 0
        wordsFound = False

        # A string with all words joined togethor
        wordsCombined = '' # O(nm) Space Comlexity
        for worded in library:  # O(nm) Time Comlexity
            wordsCombined += worded + '|'

        # Iterate through the list backwards, happens K times
        while i >= 0:
            # Check the word to the end of the list is in the library of words
            if DecryptedWord[i:] in library:  # Takes O(NM) complexity
                table[i] = DecryptedWord[i:]
                lastpoint = i # Save where the word started
                endpoint = lastpoint + len(table[i])
                wordsFound = True # Save if there is a word for later

            # If that didnt work check with the word up to the last point a word was found
            elif DecryptedWord[i:lastpoint+1] in library:
                table[i] = DecryptedWord[i:lastpoint+1]
                lastpoint = i
                endpoint = lastpoint + len(table[i])
                wordsFound = True

            elif DecryptedWord[i:lastpoint+2] in library:
                table[i] = DecryptedWord[i:lastpoint+2]
                lastpoint = i
                endpoint = lastpoint + len(table[i])
                wordsFound = True

            elif DecryptedWord[i:endpoint] in library:
                table[i] = DecryptedWord[i:endpoint]
                lastpoint = i
                endpoint = lastpoint + len(table[i])
                wordsFound = True

            elif DecryptedWord[i] in library:
                table[i] = DecryptedWord[i]
                wordsFound = True

            # If it wasnt a word, check if that combination is a possible combination
            # within the words in library
            elif DecryptedWord[i:lastpoint+1] not in wordsCombined:
                lastpoint = i
            i -= 1

        # If no words are found, return early
        if wordsFound == False:
            return

        # Traverse through table to get final output
        i = 0
        j = 0
        FinalResult = ''
        while i < len(table):
            if table[i] != None:
                if i != 0 and table[j] == None:
                    FinalResult += ' '
                FinalResult += table[i] + ' '
                j = i
                i = i + len(table[i])
            else:
                FinalResult += DecryptedWord[i]
                j = i
                i += 1
        FinalResult = FinalResult[:-1]

        self.message = FinalResult

    def getMessage(self):
        '''
        returns the state of message on the class
        Time complexity: O(1)
        Space complexity: Auxilarry space complexity N/A, O(1)
        Error handle: N/A
        :return: self.message
        Parameter: N/A
        pre-requisite: N/A
        '''
        return self.message


def main():
    #initialTesting = Decipher()
    #initialTesting.messageFind('encrypted_3.txt')
    #print(initialTesting.message)
    #initialTesting.wordBreak('dictionary_3.txt')
    #print(initialTesting.message)

    Cipher = Decipher()
    CorrectIn = False
    while CorrectIn == False:
        Cipher.messageFind(input('The name of the file, contains two encrypted texts : '))
        if Cipher.message != '':
            CorrectIn = True
    DecipheredMsg = Cipher.message
    CorrectIn = False
    Cipher.wordBreak(input('The name of the dictionary file : '))
    TrueMsg = Cipher.message

    print('---------------------------------------------------------------------')
    print('Deciphered message is',DecipheredMsg)
    print('True message is',TrueMsg)
    print('---------------------------------------------------------------------')
    print('Program end')

if __name__ == '__main__':
    main()