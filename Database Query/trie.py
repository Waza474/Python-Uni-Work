def query(filename, id_prefix, last_name_prefix):
    '''
    Gets a file with a data base including Index/ID/FirstName/Surname/Phone/Email and returns which indexes match the
    id prefix requirement and last name prefix requirement
    Time complexity: Best: O(T + NM + k + l + n_k + n_l) No early cutoffs or special cases to improve time complexity
                    Worst: O(T + NM + k + l + n_k + n_l)
    Space complexity: Best: O(T + NM)
                     Worst: O(T + NM)
    Error handle: filename must be a valid file name
    Return: A list with all indexes with users that follow the 2 prefix requirements
    Parameter:
        Filename: Name of file with the database/information
        id_prefix: i set of integers for which id must include as a prefix
        laste_name_prefix: a string where the surname must include as the prefix
    Precondition: The file with the database must be in the correct format or this may not work
    '''

    # Open and Write File
    try:
        txtfile = open(filename)
    except:
        return

    # Write file to a list
    # Time Complexity and Space Complexity: O(nm)
    DatabaseList = []
    for line in txtfile:
        TempLine = line.split()
        TempLine[0] = int(TempLine[0])
        DatabaseList.append(TempLine)

    # Return Early if list is empty
    if len(DatabaseList) == 0:
        return
    elif len(DatabaseList[0]) != 6:
        return

    # Creating the Trie
    #   ord('a') = 97
    #   ord('A') = 65
    #   ord('$') = 36
    # First level on Trie
    SurnameTrie = [None] * 53
    idNumberTrie = [None] * 11

    #Test data base list
    #DatabaseList = [[11,'132',1,'dab'],[2,'101',2,'cab'],[31,'100',3,'dad'],[42,'102',4,'dad'],[54,'133',5,'dog']]

    # Loop for each record in the Database
    for CurrentRecord in DatabaseList:

        # SurnameTrie
        CurrentLevel = SurnameTrie
        RecordSurname = CurrentRecord[3]
        # Loop for each letter in the surname + $
        for letter in RecordSurname:
            if ord(letter) < 91:
                position = ord(letter) - 65
            else:
                position = ord(letter) - 65 - 6
            if CurrentLevel[position] is None:
                CurrentLevel[position] = [None] * 53
            CurrentLevel = CurrentLevel[position]
            # If it is at '$', append the record index
            if CurrentLevel[-1] is None:
                CurrentLevel[-1] = []
            CurrentLevel[-1].append(CurrentRecord[0])

        #IddentificationTrie
        CurrentLevel = idNumberTrie
        RecordID = str(CurrentRecord[1])
        for number in RecordID:
            if CurrentLevel[int(number)] is None:
                CurrentLevel[int(number)] = [None] * 11
            CurrentLevel = CurrentLevel[int(number)]
            # If it is at '$', append the record index
            if CurrentLevel[-1] is None:
                CurrentLevel[-1] = []
            CurrentLevel[-1].append(CurrentRecord[0])

    # Trace back through Trie's with prefixs
    SurnameQuery = [] # Space Complexity O(n_l)
    idQuery = [] # Space Complexity O(n_k)

    # Finding Last Name Prefix
    SurnamePrefixFound = True
    CurrentLevel = SurnameTrie
    i = 0

    #Prefix used for testing
    #last_name_prefix = 'd'

    # Time Complexity O(l)
    while SurnamePrefixFound == True and i < len(last_name_prefix):
        if ord(last_name_prefix[i]) < 91:
            position = ord(last_name_prefix[i]) - 65
        else:
            position = ord(last_name_prefix[i]) - 65 - 6
        if CurrentLevel[position] is not None:
            CurrentLevel = CurrentLevel[position]
            i += 1
        else:
            SurnamePrefixFound = False
    # Returning List of Record Indexes with last_name_prefix as the prefix
    if SurnamePrefixFound == True:
        SurnameQuery = CurrentLevel[-1]

    # Finding id Prefix
    SurnameidFound = True
    CurrentLevel = idNumberTrie
    i = 0

    # Time Complexity O(k)
    while SurnameidFound == True and i < len(id_prefix):
        if CurrentLevel[int(id_prefix[i])] is not None:
            CurrentLevel = CurrentLevel[int(id_prefix[i])]
            i += 1
        else:
            SurnameidFound = False
    # Returning List of Record Indexes with this prefix (id_prefix)
    if SurnameidFound == True:
        idQuery = CurrentLevel[-1]

    # Output a Final Result
    if last_name_prefix == '':
        return idQuery
    elif id_prefix == '':
        return SurnameQuery
    else:
        if idQuery == [] or SurnameQuery == []:
            return
        else:
            # Using a count sort method to find over lap in appropriate time complexity

            # Finding max of idQuery is time complexity of O(n_k)
            # Finding max of idQuery is time complexity of O(n_l)
            # Finding the max of these 2 is O(1), 1 comparison
            CountList = [0] * (max(max(idQuery), max(SurnameQuery)) + 1)

            # Occurs n_k times
            for numb in idQuery:
                CountList[numb] += 1
            # Occurs n_l times
            for numb in SurnameQuery:
                CountList[numb] += 1

            # Combing Overlaps to 1 List
            OutList = []
            i = 0
            while i < len(CountList):
                if CountList[i] == 2:
                    OutList.append(i)
                i += 1
            return OutList

def reverseSubstrings(filename):
    '''
    Gets a string from a file, finds substrings that are also in the reverse of the string, using a suffix tree
    Time complexity: Best: O(K*K) No substrings occur in reverse
                    Worst: O(K*K + P)
    Space complexity: Best: O(K*K + P)
                     Worst: O(K*K + P)
    Error handle: A valid file name must be used
    Return: OutputList: a list where each element is a list with 2 elements, the substring and where it occurs (index)
    Parameter: Filename: Name of the File with the string
    Precondition: N/A
    '''

    # Open and Write File
    try:
        txtfile = open(filename)
    except:
        return

    for line in txtfile:
        OriginalText = line

    # Generating a suffix Trie
    # Time Complexity O(K*K)
    SuffixTrie = [None] * 27
    i = 0
    while i < len(OriginalText):
        CurrentLevel = SuffixTrie
        CurrentWord = OriginalText[i:]
        for character in CurrentWord:
            if CurrentLevel[ord(character) - 97] is None:
                CurrentLevel[ord(character) - 97] = [None] * 27
            CurrentLevel = CurrentLevel[ord(character) - 97]
        i += 1

    # Generate all Substrings
    # Time Complexity: O(K*K) ... K being length of original string
    possibleSubstrings = [] # Eventually O(K*K) space complexity
    i = 0
    while i < len(OriginalText):
        j = i + 1
        while j < len(OriginalText) + 1:
            if len(OriginalText[i:j]) != 1: # Ensure no 1 length string
                possibleSubstrings.append([OriginalText[i:j],i])
            j += 1
        i += 1

    # Searching The Substrings within the Suffix Trie
    OutputList = []
    for substring in possibleSubstrings:
        reversed = substring[0][::-1]
        CurrentLevel = SuffixTrie
        i = 0

        while CurrentLevel is not None and i < len(reversed):
            CurrentLevel = CurrentLevel[ord(reversed[i])-97]
            i += 1
        if CurrentLevel is not None:
            OutputList.append(substring)

    return OutputList


def main():
    # function for main output/input
    print('TASK-1:')
    print('---------------------------------------------------------------------')
    InputFile = input('Enter the file name of the query database :')
    InputId = input('Enter the prefix of the identification number:')
    InputSur = input('Enter the prefix of the last name :')
    ReturnedList = query(InputFile, InputId, InputSur)
    if ReturnedList is not None:
        print(len(ReturnedList),'record found')
        for item in ReturnedList:
            print('Index number :',item)
    print('---------------------------------------------------------------------')
    print('TASK-2:')
    InputFile2 = input('Enter the file name for searching reverse substring: ')
    ReturnedList = reverseSubstrings(InputFile2)
    print('---------------------------------------------------------------------')
    i = 0
    for item in ReturnedList:
        if i == len(ReturnedList)-1:
            print(str(item[0]) + '(' + str(item[1]) + ')')
        else:
            print(str(item[0])+'('+str(item[1])+'),',end = ' ')
        i += 1

if __name__ == '__main__':
    main()
