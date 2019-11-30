class Graph():
    def __init__(self):
        self.VertexList = []
        self.RedLights = []
        self.TollRoads = []
        self.ServiceDetour = []

    def buildGraph(self, filename_roads):
        '''
        Builds a graph through adjancency list and no other external classes are used
        Time complexity: O(E)
        Space complexity: O(E + V)
        Error handle: File Name must be a valid file
        Return: N/A
        Parameter: filename_roads: File name for the lists of all the edges in a graph
        Precondition: N/A
        '''

        try:
            RoadFile = open(filename_roads)
        except:
            return

        for line in RoadFile:
            line = line.split()

            while len(self.VertexList) < int(line[0]) + 1:
                self.VertexList.append(None)

            if self.VertexList[int(line[0])] == None:
                self.VertexList[int(line[0])] = [[int(line[1]), float(line[2])]]
            else:
                self.VertexList[int(line[0])].append([int(line[1]), float(line[2])])


    def quickestPath(self,source,target):
        '''
        Finds the quickest path from source vertex to target vertex through dijkstras algorithm
        Time complexity: O(ElogV)
        Space complexity: O(E+V)
        Error handle: source and target must be numbers and There must be an existed graph in the class
        Return: A tuple of 2 elements, Path to target and Cost
        Parameter: Source: Which vertex to start at     Target: the destination vertex
        Precondition: VertexList must be established
        '''

        try:
            source = int(source)
            target = int(target)
        except:
            return

        if len(self.VertexList) == 0:
            return

        Vertices = [-2] * len(self.VertexList)
        Finalized = [None] * len(self.VertexList)

        Discovered = [[source,0]]
        Vertices[source] = 0

        #Starting at source vertex and using Dijkstra's Algorithm to find shortest path
        while len(Discovered) != 0:
            v = Discovered[0]
            if self.VertexList[v[0]] is not None:
                for edge in self.VertexList[v[0]]:
                    if Vertices[edge[0]] == -2:
                        Discovered.append([edge[0], v[1]+edge[1],v[0]])
                        Vertices[edge[0]] = len(Discovered) - 1

                        #Shuffling the minHeap of Discovered to be in order
                        goodSpot = False
                        i = len(Discovered) - 1
                        while goodSpot == False:
                            if Discovered[i][1] < Discovered[(i-1)//2][1]:
                                Discovered[i], Discovered[(i - 1) // 2] = Discovered[(i - 1) // 2], Discovered[i]
                                Vertices[Discovered[i][0]], Vertices[Discovered[(i - 1) // 2][0]] = Vertices[Discovered[(i - 1) // 2][0]], Vertices[Discovered[i][0]]

                                i = (i-1)//2
                            else:
                                goodSpot = True


                    elif Vertices[edge[0]] != -1:
                        if Discovered[Vertices[edge[0]]][1] > v[1]+edge[1]:
                            Discovered[Vertices[edge[0]]][1] = v[1] + edge[1]
                            Discovered[Vertices[edge[0]]][2] = v[0]

            #Updating the Used vertex to be finalized
            Finalized[Discovered[0][0]] = (Discovered[0])
            Discovered[0] = Discovered[-1]
            Discovered.pop()
            Vertices[v[0]] = -1
            if len(Discovered) != 0:
                Vertices[Discovered[0][0]] = 0
                i = 0
                j = i
                goodSpot = False
                while goodSpot == False:
                    if i*2 +2 < len(Discovered):
                        if Discovered[i*2 + 1][1] < Discovered[i*2 + 2][1]:
                            j = i*2 + 1
                        else:
                            j = i*2 + 2
                    elif i*2 + 1 < len(Discovered):
                        j = i * 2 + 1
                    else:
                        goodSpot = True

                    if i == j or Discovered[i][1] < Discovered[j][1]:
                        goodSpot = True

                    if goodSpot == False:
                        Discovered[i], Discovered[j] = Discovered[j], Discovered[i]
                        Vertices[Discovered[i][0]], Vertices[Discovered[j][0]] = Vertices[Discovered[j][0]], Vertices[Discovered[i][0]]

                    i = j

        #Tracing Back through Finallized to get the path
        Found = False
        i = 0
        Current = target
        path = []
        while i<len(Finalized) and Found == False:
            try:
                path.append(Current)
                if Current == source:
                    Found = True
                else:
                    Current = Finalized[Current][2]
            except:
                i = len(Finalized) + 2
            i += 1

        if i >= len(Finalized) and Found == False:
            return[[],-1]
        else:
            return path[::-1], Finalized[target][1]


    def augmentGraph(self, filename_camera, filename_toll):
        '''
        Takes the input of files and stores their contents into lists for the safe path function
        Time complexity: O(N + M), being sizes of input files respectively, never greater than V or E
        Space complexity: O(N), being sizes of input files respectively, never greater than V or E
        Error handle: Filenames must be a valid file
        Return: N/A
        Parameter: filename_camera: a file with 1 number per line of locations of cameras
                filename_toll: a file with 2 numbers seperated with a space for 'toll roads'
        Precondition: N/A
        '''

        try:
            CameraFile = open(filename_camera)
            TollFile = open(filename_toll)
        except:
            return

        # Complexity O(n) where n is length of list containing Camera Files
        # Will never be greater than V
        for Line in CameraFile:
            self.RedLights.append(int(Line))

        # Size of self.TollRoads will never be greater than O(V + E)
        self.TollRoads = [0]*len(self.VertexList)
        for Line in TollFile:
            Line = Line.split()
            self.TollRoads[int(Line[0])] = int(Line[1])

        return

    def quickestSafePath(self, source, target):
        '''
        Finds the Quickest Safe path with same method as quickest path but with modifications
        to not encounter "bad" vertices or edges
        Time complexity: O(ElogV)
        Space complexity: O(E +V)
        Error handle: Source and Target must be numbers
        Return: A tuple of 2 elements, Path to target and Cost
        Parameter: Source: Which vertex to start at     Target: the destination vertex
        Precondition: VertexList must be established
        '''

        # Ensuring that inputs are integers
        try:
            source = int(source)
            target = int(target)
        except:
            return



        # Creating a copy of self.VertexList
        ModifiedVertexList = self.VertexList
        TestChange1 = ModifiedVertexList[source]
        TestChange2 = ModifiedVertexList[target]
        # Removing Red Light vertexs
        for Vertex in self.RedLights:
            ModifiedVertexList[Vertex] = None
        # Early cut off if camera is on source or destination
        if ModifiedVertexList[source] != TestChange1 or TestChange2 != ModifiedVertexList[target]:
            return([[],-1])

        # Modifies Quickest Path Code
        Vertices = [-2] * len(ModifiedVertexList)
        Finalized = [None] * len(ModifiedVertexList)

        Discovered = [[source, 0]]
        Vertices[source] = 0

        # Starting at source vertex and using Dijkstra's Algorithm to find shortest path
        while len(Discovered) != 0:
            v = Discovered[0]
            if ModifiedVertexList[v[0]] is not None :
                for edge in ModifiedVertexList[v[0]]:
                    if Vertices[edge[0]] == -2:
                        #Ignore Toll Roads
                        if self.TollRoads[edge[0]] != edge[1]:

                            Discovered.append([edge[0], v[1] + edge[1], v[0]])
                            Vertices[edge[0]] = len(Discovered) - 1

                            # Shuffling the minHeap of Discovered to be in order
                            goodSpot = False
                            i = len(Discovered) - 1
                            while goodSpot == False:
                                if Discovered[i][1] < Discovered[(i - 1) // 2][1]:
                                    Discovered[i], Discovered[(i - 1) // 2] = Discovered[(i - 1) // 2], Discovered[i]
                                    Vertices[Discovered[i][0]], Vertices[Discovered[(i - 1) // 2][0]] = Vertices[Discovered[
                                        (i - 1) // 2][0]], Vertices[Discovered[i][0]]

                                    i = (i - 1) // 2
                                else:
                                    goodSpot = True


                    elif Vertices[edge[0]] != -1:
                        if Discovered[Vertices[edge[0]]][1] > v[1] + edge[1]:
                            Discovered[Vertices[edge[0]]][1] = v[1] + edge[1]
                            Discovered[Vertices[edge[0]]][2] = v[0]

            # Updating the Used vertex to be finalized
            Finalized[Discovered[0][0]] = (Discovered[0])
            Discovered[0] = Discovered[-1]
            Discovered.pop()
            Vertices[v[0]] = -1
            if len(Discovered) != 0:
                Vertices[Discovered[0][0]] = 0
                i = 0
                j = i
                goodSpot = False
                while goodSpot == False:
                    if i * 2 + 2 < len(Discovered):
                        if Discovered[i * 2 + 1][1] < Discovered[i * 2 + 2][1]:
                            j = i * 2 + 1
                        else:
                            j = i * 2 + 2
                    elif i * 2 + 1 < len(Discovered):
                        j = i * 2 + 1
                    else:
                        goodSpot = True

                    if i == j or Discovered[i][1] < Discovered[j][1]:
                        goodSpot = True

                    if goodSpot == False:
                        Discovered[i], Discovered[j] = Discovered[j], Discovered[i]
                        Vertices[Discovered[i][0]], Vertices[Discovered[j][0]] = Vertices[Discovered[j][0]], Vertices[
                            Discovered[i][0]]

                    i = j

        # Tracing Back through Finallized to get the path
        Found = False
        i = 0
        Current = target
        path = []
        while i < len(Finalized) and Found == False:
            try:
                path.append(Current)
                if Current == source:
                    Found = True
                else:
                    Current = Finalized[Current][2]
            except:
                i = len(Finalized) + 2
            i += 1

        if i >= len(Finalized) and Found == False:
            return [[], -1]
        else:
            return path[::-1], Finalized[target][1]

    def addService(self, filename_service):
        '''
        Gets the locations of services nodes/vertices and stores them in a list
        Time complexity: O(X) where X is the number of service stops, never greater than E or V
        Space complexity: O(X), see above
        Error handle: filename_service must be a valid file
        Return: N/A
        Parameter: filename_service: File with the service stops
        Precondition: N/A
        '''

        try:
            ServiceFile = open(filename_service)
        except:
            return

        for line in ServiceFile:
            self.ServiceDetour.append(''.join(line.split()))

        return

    def quickestDetourPath(self, source, target):
        '''
        Finds the quickest detour path using the quickest path function above and the service stations list
        Time complexity: O(ElogV)
        Space complexity:O(E+V)
        Error handle: source and target must be valid numbers
        Return: A tuple of 2 elements, Path to target and Cost
        Parameter: Source: Which vertex to start at     Target: the destination vertex
        Precondition: VertexList must be established
        '''

        try:
            source = int(source)
            target = int(target)
        except:
            return

        # If there is no service stations
        if len(self.ServiceDetour) == 0:
            return self.quickestPath(source, target)

        QuickestPath = None
        MinCost = 10000


        #If there are required stops
        for stop in self.ServiceDetour:
            if source == target and source == stop:
                return [source], 0
            Path, Cost = self.quickestPath(source, stop)
            if Cost != -1:
                returned = self.quickestPath(stop, target)
                if returned[1] != -1:
                    for item in returned[0]:
                        if item != returned[0][0]:
                            Path.append(item)
                    Cost += returned[1]
                    if Cost < MinCost:
                        MinCost = Cost
                        QuickestPath = Path

        if QuickestPath is not None:
            return QuickestPath, MinCost

        # If no path was found
        return [[],-1]

if __name__ == '__main__':
    print('---------------------------------------------------------------------')
    aGraph = Graph()
    aGraph.buildGraph(input('Enter the file name for the graph : '))
    CamFile = input('Enter the file name for camera nodes: ')
    TollFile = input('Enter the file name for the toll roads : ')
    ServFile = input('Enter the file name for the service nodes : ')
    print('---------------------------------------------------------------------')
    SourceNode = input('Source node: ')
    SinkNode = input('Sink node: ')
    Output = aGraph.quickestPath(SourceNode,SinkNode)
    print('---------------------------------------------------------------------')
    print('Quickest path')
    if Output[1] != -1:
        StringPrint = ''
        for numb in Output[0]:
            StringPrint += str(numb) + ' -->'
        StringPrint = StringPrint[:-4]
        print(StringPrint)
        print('Time:',Output[1],'minutes(s)')
    else:
        print('No path exists')
        print('Time: 0 minute(s)')
    print('---------------------------------------------------------------------')
    aGraph.augmentGraph(CamFile,TollFile)
    Output = aGraph.quickestSafePath(SourceNode,SinkNode)
    print('Safe quickest path')
    if Output[1] != -1:
        StringPrint = ''
        for numb in Output[0]:
            StringPrint += str(numb) + ' -->'
        StringPrint = StringPrint[:-4]
        print(StringPrint)
        print('Time:', Output[1], 'minutes(s)')
    else:
        print('No path exists')
        print('Time: 0 minute(s)')
    print('---------------------------------------------------------------------')
    aGraph.addService(ServFile)
    Output = aGraph.quickestDetourPath(SourceNode, SinkNode)
    print('Quickest detour path')
    if Output[1] != -1:
        StringPrint = ''
        for numb in Output[0]:
            StringPrint += str(numb) + ' -->'
        StringPrint = StringPrint[:-4]
        print(StringPrint)
        print('Time:', Output[1], 'minutes(s)')
    else:
        print('No path exists')
        print('Time: 0 minute(s)')
    print('---------------------------------------------------------------------')
    print('Program End')