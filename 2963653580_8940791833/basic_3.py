import sys      # argv
import time     # time elapsed
import psutil # type: ignore
import gc

""" Given Parameters """
# Gap penalty
DELTA = 30

# Mismatch penalty -- 0 if matching
ALPHA = {
            "A": { "A": 0, "C": 110, "G": 48, "T": 94 },
            "C": { "A": 110, "C": 0, "G": 118, "T": 48 },
            "G": { "A": 48, "C": 118, "G": 0, "T": 110 },
            "T": { "A": 94, "C": 48, "G": 110, "T": 0 }
        }

inputFile = sys.argv[1]     # Input file name
outputFile = sys.argv[2]    # Output file name

inputLines = []
numBase = 0
numIndices = 0

def InitFiles():
    global numBase
    global numIndices

    """ INPUT FILE """
    with open(inputFile) as file:
        for line in file:
            sLine = line.rstrip()

            # inputLines.append(line.rstrip())

            if sLine.isdigit():
                numIndices += 1
                inputLines.append(int(sLine))
            else:
                numBase += 1
                inputLines.append(sLine)
    line1 = []
    line2 = []

    stringNum = 0
    i = 0

    """ GENERATE INPUT STRINGS """
    while i < len(inputLines):
        if isinstance(inputLines[i], str):
            stringNum += 1
        if(stringNum == 1):
            line1.append(inputLines[i])
            i += 1
            while not isinstance(inputLines[i], str):   
                line1.append(line1[len(line1)-1][:inputLines[i]+1] + line1[len(line1)-1] + line1[len(line1)-1][inputLines[i]+1:])
                i += 1
        elif stringNum == 2:
            line2.append(inputLines[i])
            i += 1
            while i < len(inputLines) and not isinstance(inputLines[i], str):       
                line2.append(line2[len(line2)-1][:inputLines[i]+1] + line2[len(line2)-1] + line2[len(line2)-1][inputLines[i]+1:])
                i += 1      
    return line1[len(line1)-1], line2[len(line2)-1]

def Output(cost, X_Align, Y_Align, Time, Memory):
    """
    1. Cost of the alignment (Integer)
    2. First string alignment ( Consists of A, C, T, G, _ (gap) characters)
    3. Second string alignment ( Consists of A, C, T, G, _ (gap) characters )
    4. Time in Milliseconds (Float)
    5. Memory in Kilobytes (Float)
    """
    file = open(outputFile, "w")
    file.write(cost + "\n")
    file.write(X_Align + "\n")
    file.write(Y_Align + "\n")
    file.write(Time + "\n")
    #print("CPU: " + str(Time))
    file.write(Memory)
    #print("Memory: " + str(memory_consumed))
    file.close()

def PrintOpt(OPT):
    for i in reversed(range(len(OPT))):
        for j in range(len(OPT[i])):
            print(OPT[i][j], end=" ")
        print("\n")

""" BASIC IMPLEMENTATION """
def SequenceAlignment(X, Y):
    
    M = len(X)
    N = len(Y)

    # M+1 and N+1 -- range is non-inclusive, row/col 0 will be BASE CASE
    OPT = [[None for j in range(N+1)] for i in range(M+1)]

    """ BOTTOM UP PASS"""
    # Base Cases
    for i in range(M+1):
        OPT[i][0] = i * DELTA
    for j in range(N+1):
        OPT[0][j] = j * DELTA

    for i in range(1, M+1):
        for j in range(1, N+1):
            OPT[i][j] = min(OPT[i-1][j-1] + ALPHA[X[i-1]][Y[j-1]],
                            OPT[i-1][j] + DELTA,
                            OPT[i][j-1] + DELTA)
        
    """ TOP DOWN PASS """
    # Follow path that minimized OPT(M-1, N-1)
    # Prepend to each Align string because working from the end
    X_Align = ""
    Y_Align = ""

    # Start from the end and go back
    i = M
    j = N

    # OR -- go until at 0, 0
    # Do not check 0 of OPT -- base case
    while i > 0 or j > 0:      
        # KEEP THIS ORDER TO MATCH THE SAMPLE OUTPUTS

        # diag
        if OPT[i][j] == OPT[i-1][j-1] + ALPHA[X[i-1]][Y[j-1]]:      
            X_Align = X[i-1] + X_Align
            Y_Align = Y[j-1] + Y_Align
            if i > 0:
                i -=1 
            if j > 0:
                j -= 1

        # y gap
        elif OPT[i][j] == OPT[i][j-1] + DELTA:    
            X_Align = "_" + X_Align
            Y_Align = Y[j-1] + Y_Align
            if j > 0:
                j -= 1

        # x gap
        elif OPT[i][j] == OPT[i-1][j] + DELTA:                      
            X_Align = X[i-1] + X_Align
            Y_Align = "_" + Y_Align
            if i > 0:
                i -= 1

    # Optimal cost at OPT[M][N]
    return OPT[M][N], X_Align, Y_Align

""" Provided in project prompt """
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

if __name__ == "__main__":
    gc.disable()
    X, Y = InitFiles()
    startTime = time.time()
    start_memory = process_memory()
    #print(start_memory)
    cost, X_Align, Y_Align = SequenceAlignment(X, Y)
    end_memory = process_memory()
    #print(end_memory)
    timeElapsed = (time.time() - startTime) * 1000
    memory_consumed = max((end_memory - start_memory), 0)
    Output(str(cost), X_Align, Y_Align, str(timeElapsed), str(memory_consumed))
    #Output(str(cost), X_Align, Y_Align, str(timeElapsed), str(end_memory))
    gc.enable()