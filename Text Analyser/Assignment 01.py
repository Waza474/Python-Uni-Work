# Task 1
def preprocess(filename):
    '''
    Goes throught he filename and not needed words
    :Time-Complexity: All Cases: O(nm + k) k is all white spaces and punctuation
    :Space-Complexity: Worst Case: O(nm) if all words were same length m
                        Average: O(nm)
    :Error handling: if an invalid file is used, it will not run through the process
    :param filename:
    :return: A list with all words ready for other work
    '''

    if open(filename):
        txtfile = open(filename)
    else:
        txtfile = False

    fileLines = []
    fileWords = []

    if txtfile != False:
        # This loop will go through for each line
        for line in txtfile:
            fileLines.append(line) #O(1) complexity

            tempWord = ''

            # Goes through the line and keeps whichs letters it gets in a row, when something interrupts...
            # the letters it appends it to a list and keeps going
            # Complexity: ~O(k) if K is the number of characters in a line, overall O(NM) because...
            # the total amount of characters should be n*m + other characters not in words (e.g. ? , !)

            for character in line:
                if character in 'abcdefghijklmnopqrstuvwxyz':
                    tempWord += character
                else:
                    if tempWord is not '':
                        fileWords.append(tempWord)
                    tempWord = ''

    returnWords = []
    badWords = ['was','were','am','is','are','has','have','had','been','will','shall','may','can','would','might','could','a','an','the']

    # This Whole loop will run O(n) times, going through each word in the file that was picked up (fileWords)

    for word in fileWords:
        if word not in badWords: # This if has a O(1) complexity as the number of words in bad words does
                                #  does not depend on something and will stay at constant length
            returnWords.append(word) #O(1) complexity to append

    if len(returnWords) == 0:
        print('Unable to continue:\n1. Writing.txt is empty or\n2. There is no word remaining after preprocessing')

    print('Words are preproccesed')
    temp = 'a'
    while temp != 'y' or temp != 'n' or temp != 'yes' or temp != 'no':
        temp = input('Do i need to display the remaining words: ').lower()
        if temp == 'y' or temp == 'yes':
            for word in returnWords:
                print(word)


    return returnWords

# Task 2
def wordSort(sortedList):
    '''
    Sorts the list of words by Radix Sort
    :Time Complexity: All Cases O(nm)
    :Space Complexity: O(nm), only list of same size are made
    :Error Handling: N/A
    :param sortedList:
    :return: sortedList  List is sorted by return
    '''

    if len(sortedList) != 1 or len(sortedList) != 0:
        # Find Largest Word
        # Time Complexity O(n)
        maxLength = 1 # finding m
        for word in sortedList:
            if len(word) > maxLength:
                maxLength = len(word)

        # Make all words same length
        # Time Complexity O(nm)
        i = 0
        while i < len(sortedList):
            sortedList[i] = [sortedList[i],len(sortedList[i])]
            while len(sortedList[i][0]) < maxLength:
                sortedList[i][0] += 'a'
            i += 1

        # Time Complexity O(m)
        i = maxLength - 1
        while i >= 0:

            # Create a Count List
            # Time Complexity O(n)
            # Space Complexity (n)
            countList = []
            tempCounter = 0
            while tempCounter < 26:
                countList.append([])
                tempCounter += 1

            # Loop and count
            # Time Complexity O(n)
            for word in sortedList:
                temp = word[0]
                countList[ord(temp[i])-97].append(word)

            # Put Back into List
            # Time Complexity, O(n)
            sortedList = []
            for slot in countList:
                for word in slot:
                    sortedList.append(word)

            i -= 1

        # Time Complexity O(nm)
        i = 0
        while i < len(sortedList):
            while len(sortedList[i][0]) > sortedList[i][1]:
                sortedList[i][0] = sortedList[i][0][:-1]
            sortedList[i] = sortedList[i][0]
            i += 1

    temp = 'a'
    while temp != 'y' or temp != 'n':
        temp = input('\nThe remaining words are sorted in alphabetical order \nDo you want to see: ').lower()
        if temp == 'y' or temp == 'yes':
            for word in sortedList:
                print(word)

    return(sortedList)

# Task 3
def wordCount(sortedList):
    '''
    Gets the count of each word in a sorted list
    :Time-Complexity: All Cases O(nm), goes through the list of words once
    :Space-Complexity: O(nm), an list of similar size is created, space complexity is not increased
    :Error Handling:
    :param sortedList:
    :return: list including 2 elements, 1. the total count of words in sorted list
                                        2. Each unique word and their respective count
    '''
    wordCountList = []

    wordCounter = 1
    i = 0
    # Loops n times and inside has to do a m length comparison ... O(nm)
    while i < len(sortedList):

        # Prevent overflow
        if i + 1 != len(sortedList):
            # Check if same to next value
            if sortedList[i] == sortedList[i+1]:
                # Add to counter
                wordCounter += 1
            else:
                # If different, add the word and how many times it appeared to a list
                wordCountList.append([sortedList[i],wordCounter])
                wordCounter = 1
        else:
            # If last letter in list, append infomation
            if sortedList[i] != sortedList[i-1]:
                wordCountList.append([sortedList[i], wordCounter])
        i += 1

    # Display Output
    print('\nThe total number of words in the writing:',len(sortedList),'\nThe frequencies of each word:')
    if len(wordCountList) != 0:
        for set in wordCountList:
            print(set[0],':',set[1])

    OutputList = [len(sortedList)]
    for set in wordCountList:
        OutputList.append(set)
    return (OutputList)

# Task 4
def kTopWords(k, sortedList):
    '''
    Creates a min heap  with k size to track kth most common items
    :Time complexity: Worst case: O(nlogk)
    :Space complexity: O(nk)
    :Error Handling: Ensuring k is a valid number
    :param k:
    :param sortedList:
    :return:
    '''
    if k <= 0:
        print(k, 'top most words appear in the writing are:')
        return None

    kTopHeap = [[0,0]]
    i = 0
    kCounter = 0
    while i < len(sortedList):

        # Filling the kTopHeap until it reaches its max length
        if kCounter < k:

            # Putting the new element at the end of the heap
            kTopHeap.append((sortedList[i]))
            if i != 0:
                j = i + 1

                # A loop to move up the heap making sure the largest is at the top
                while j > 0:

                    # The parent of the item is at position k in the heap
                    parentPos = (j // 2)

                    # Swap if parent is smaller
                    if kTopHeap[j][1] < kTopHeap[parentPos][1]:
                        kTopHeap[j], kTopHeap[parentPos] = kTopHeap[parentPos], kTopHeap[j]
                        j = parentPos
                    # If it didnt swap, then its postion is fine
                    else:
                        j = 0
            kCounter += 1

        # Once heap has reached maximum size, start replacing smallest
        else:
            if sortedList[i][1] > kTopHeap[1][1]:
                j = 1
                kTopHeap[1] = sortedList[i]
                while j <= k:

                    swap = False
                    if j*2 <= k:
                        # Check against left child
                        if kTopHeap[j][1] > kTopHeap[j*2][1]:
                            kTopHeap[j],kTopHeap[j*2] = kTopHeap[j*2],kTopHeap[j]
                            j = j*2
                            swap = True
                    if j*2 + 1 <= k and swap == False:
                        # Check against right child
                        if kTopHeap[j][1] > kTopHeap[j*2 + 1][1]:
                            kTopHeap[j], kTopHeap[j*2 + 1] = kTopHeap[j*2 + 1], kTopHeap[j]
                            j = j*2 + 1
                            swap = True

                    # If neither were smaller, then it is in a good position
                    if swap == False:
                        j = 2*k + 1
        i += 1

    # A loop (O(k)) to ensure the elements are in correct alphabetical order if their occurence value is equal
    returnList = []
    while len(returnList) < k:
        returnList.append(kTopHeap.pop()) # Time complexity O(1)
        if len(returnList) != 1:
            if returnList[-1][1] == returnList[-2][1]:
                if returnList[-1][0] < returnList[-2][0]:
                    returnList[-1], returnList[-2] = returnList[-2], returnList[-1]

    print(k,'top most words appear in the writing are:')
    for set in returnList:
        print(set[0],':',set[1])

    return (returnList)

# # Testing
# Task 1
preproccesed = preprocess('Writing.txt')
# Task 2
preproccesed = wordSort(preproccesed)
# Task 3
preproccesed = wordCount(preproccesed)
# Task 4
try:
    kInput = int(input('\nHow many top-most frequent words do I display: '))
except:
    kInput = 0
kTopWords(kInput,preproccesed[1:])

