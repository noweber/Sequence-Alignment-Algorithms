import sys      # argv
import time     # time elapsed
import psutil # type: ignore
from math import floor
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

""" Provided in project prompt """
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

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
    file.write(Memory)
    file.close()

def PrintOpt(OPT):
    for i in reversed(range(len(OPT))):
        for j in range(len(OPT[i])):
            print(OPT[i][j], end=" ")
        print("\n")

def GetBasicBottomUpDynamicProgrammingTable(X, Y):
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
    return OPT

""" BASIC IMPLEMENTATION """
def BasicSequenceAlignment(X, Y):
   
    M = len(X)
    N = len(Y)
    
    """ BOTTOM UP PASS"""
    OPT = GetBasicBottomUpDynamicProgrammingTable(X, Y)
        
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
        if i > 0 and j > 0 and OPT[i][j] == OPT[i-1][j-1] + ALPHA[X[i-1]][Y[j-1]]:      
            X_Align = X[i-1] + X_Align
            Y_Align = Y[j-1] + Y_Align
            if i > 0:
                i -=1 
            if j > 0:
                j -= 1

        # y gap
        elif j > 0 and OPT[i][j] == OPT[i][j-1] + DELTA:    
            X_Align = "_" + X_Align
            Y_Align = Y[j-1] + Y_Align
            if j > 0:
                j -= 1

        # x gap
        elif i > 0 and OPT[i][j] == OPT[i-1][j] + DELTA:                      
            X_Align = X[i-1] + X_Align
            Y_Align = "_" + Y_Align
            if i > 0:
                i -= 1

    # Optimal cost at OPT[M][N]
    return OPT[M][N], X_Align, Y_Align

def CostOfAlignment(Xs, Ys):
    """ BASIC """
    M = len(Xs)
    N = len(Ys)

    # M+1 and N+1 -- range is non-inclusive, row/col 0 will be BASE CASE
    OPT = [[0 for j in range(N+1)] for i in range(M+1)]

    # Base Cases
    for i in range(M+1):
        OPT[i][0] = i * DELTA
    for j in range(N+1):
        OPT[0][j] = j * DELTA

    for i in range(1, M+1):
        for j in range(1, N+1):
            OPT[i][j] = min(OPT[i-1][j-1] + ALPHA[Xs[i-1]][Ys[j-1]],
                            OPT[i-1][j] + DELTA,
                            OPT[i][j-1] + DELTA)

    return OPT[M][:]

    """ EFFICIENT """
    """
    # Bottom-up pass to find similarity between a half of X (Xs) and a substring of Y (Ys)
    # Fill array from L -> R, column by column
    # Memory efficient by only keeping 2 columns until we get similarity between Xs and Ys at OPT(len(Xs), len(Ys))
    OPT = [[0 for i in range(2)] for j in range(len(Ys))]   # i columns, j rows
    
    yi = 0
    # Initial values
    # Empty Ys
    for j in range(len(Ys)):
        OPT[j][0] = j * DELTA
    # Empty Xs
    OPT[0][1] = DELTA

    # For all substrings of Xs
    for xi in range(1, len(Xs)):        
        # Go down column of Ys from 1 and compute opt sol
        for j in range(len(Ys)):
            if j == 0:
                OPT[j][0] = yi * DELTA
                yi = yi + 1

            OPT[j][1] = min(OPT[j-1][0] + ALPHA[X[xi-1]][Y[j-1]],   # Diag
                            OPT[j-1][1] + DELTA,                    # Left
                            OPT[j][0] + DELTA)                      # Down
        
        # Shift over 1 index of OPT to prep for new values
        # for j in range(len(Ys)):

    return OPT[1][:]
    """

""" EFFICIENT IMPLEMENTATION """
def EfficientSequenceAlignment(X, Y):
    M = len(X)
    N = len(Y)

    # BASE CASES:
    OPT = [[None for j in range(N+1)] for i in range(M+1)]
    if M == 1 or N == 1:
        return BasicSequenceAlignment(X, Y)
    elif M == 0 and N != 0:
         # TODO: Return ?
        return DELTA, "_", Y, # If the other string is empty, it may need to return multiple "__"
    elif M != 0 and N == 0:
         # TODO: Return ?
        return DELTA, X, "_",
    
    # DIVIDE: Figure out which index is optimal to divide Y at.
    # Find where to divide Y
    #   - Split X into XL and XR
    #   - If X is odd length, take either floor or ceil for len(X)/2
    XL = ""
    XR = ""
    if len(X) % 2 == 0:
        XL = X[:len(X)//2]
        XR = X[len(X)//2:]
    else:
        XL = X[:floor(len(X)/2)]
        XR = X[floor(len(X)/2):]
    
    # Get cost of aligning XL with all possible substrings of Y starting with Y1
    CostXL = CostOfAlignment(XL, Y)

    # Get cost of aligning XR with all possible substrings of Y ending with YN
    #CostXR = CostOfAlignment(XR, Y)
    CostXR = CostOfAlignment(XR[::-1], Y[::-1])  # Reversed XR and Y
    CostXR = CostXR[::-1]
    
    # Add CostXL + CostXR as OptXY.
    # Select the minimum value from OptXY as YSplitIndex (the optimal index to split Y at).
    OptXY = [0] * len(CostXL)
    for i in range(len(CostXL)):
        OptXY[i] = CostXL[i] + CostXR[i]

    #print(OptXY)
    min = OptXY[0]
    YSplitIndex = 0
    for i in range(1, len(OptXY)):
        if OptXY[i] < min:
            min = OptXY[i]
            YSplitIndex = i

    # CONQUER: Figure out the optimal cost and aligned strings for the X and Y splits.
    # Recursively call EfficientSequenceAlignment(X_Left, Y from 0 to Y_Split_Index) storing Optimal_Cost_Left, X_Align_Left, and Y_Align_Left.
    # Recursively call EfficientSequenceAlignment(X_Left, Y from Y_Split_Index Y.Length) storing Optimal_Cost_Right, X_Align_Right, and Y_Align_Right.   
    # Return Optimal_Cost_Left + Optimal_Cost_Right, X_Align_Left + X_Align_Right, Y_Align_Left + Y_Align_Right (instead of just the Basic solution).
    Optimal_Cost_Left, X_Align_Left, Y_Align_Left = EfficientSequenceAlignment(XL, Y[:YSplitIndex])
    Optimal_Cost_Right, X_Align_Right, Y_Align_Right = EfficientSequenceAlignment(XR, Y[YSplitIndex:])
    
    result = Optimal_Cost_Left + Optimal_Cost_Right, X_Align_Left + X_Align_Right, Y_Align_Left + Y_Align_Right
    #print(result)
    return result

if __name__ == "__main__":
    X, Y = InitFiles()

    startTime = time.time()

    cost, X_Align, Y_Align = EfficientSequenceAlignment(X, Y)

    timeElapsed = (time.time() - startTime) * 1000
    memory = process_memory()
    Output(str(cost), X_Align, Y_Align, str(timeElapsed), str(memory))

