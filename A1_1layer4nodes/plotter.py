import numpy as np
import matplotlib.pyplot as plt

text = np.loadtxt('output_ho_nho.txt')

ho_obs = np.loadtxt('ho_obs.txt')
nho_obs = np.loadtxt('nho_obs.txt')
ho_pho = np.loadtxt('ho_pho.txt')
nho_pho = np.loadtxt('nho_pho.txt')

data = np.array([],dtype=float)
ho_obs_data = np.array([],dtype=float)
nho_obs_data = np.array([],dtype=float)
ho_pho_data = np.array([],dtype=float)
nho_pho_data = np.array([],dtype=float)

wrong = 0

#for i in range(0,len(text)):
#	if int(text[i][0]) in ho_obs:
#		ho_obs_data = np.append(ho_obs_data, text[i][2])
#	if int(text[i][0]) in nho_obs:
#		nho_obs_data = np.append(nho_obs_data, text[i][2])
#	if int(text[i][0]) in ho_pho:
#		ho_pho_data = np.append(ho_pho_data, text[i][2])
#	if int(text[i][0]) in nho_pho:
#		nho_pho_data = np.append(nho_pho_data, text[i][2])
#	else:
#		print("Something went wrong!")
#		print(int(text[i][0]))
#		wrong += 1
#		print(wrong)
		
		
#print(len(ho_obs_data))
#print(len(nho_obs_data))
#print(len(ho_pho_data))		
#print(len(nho_pho_data))
		
for i in range(0,len(text)):
	data = np.append(data, text[i][2])

#for i in range(0,len(text)):
#	if text[i][2] > 0.05:
#		nho += 1
#	if text[i][2] <= 0.05:
#		ho += 1

plt.figure(0)
plt.hist(data,100,(0,0.5))
plt.axvline(0.05,c='r')
plt.show()
