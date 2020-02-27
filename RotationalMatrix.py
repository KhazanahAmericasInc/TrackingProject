import  numpy as np

def ConverttoRad (num):
    return num/180*np.pi

def Rotate_on_Z(matrix):
    rotationalMatrix = [[np.cosT1, -np.sin(T1), 0], [np.sin(T1), np.cos(T1), 0], [0,0,1]]
    return np.dot(matrix, rotationalMatrix)


T1 = 0
T2 = 0


T1 = ConverttoRad(T1)
T2 = ConverttoRad(T2)

R0_1= [[np.cosT1, -np.sin(T1), 0], [np.sin(T1), np.cos(T1), 0], [0,0,1]]
R1_2= [[np.cos(T2), -np.sin(T2), 0], [np.sin(T2), np.cos(T2), 0], [0,0,1]]

R0_2 = np.dot(R0_1, R1_2)

print(R0_2)