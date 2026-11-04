with open(r'C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(9405, 9425):
    print(f'{i+1}: {lines[i].strip()}')
