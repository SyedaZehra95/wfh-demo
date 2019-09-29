import numpy as np
import base64

import matplotlib.pyplot as plt

# Function to Convert Our Frame into Base64 Format 
def Convert_Frame_to_Base64(Frame):
  bs64 = base64.b64encode(Frame)
  return bs64

# Function to Convert Base64 into Frame which Algos take input 
def Convert_Base64_to_Frame(bs64):
  #bs64 = bas64.decode()
  print('hello')
  print('Convert_Base64_to_Frame',bs64)
  bs64=str.encode(bs64)
  Frame_copy = base64.decodebytes(bs64)
  print('hello1')
  Frame_copy = np.frombuffer(random_noise_copy , dtype=np.float64)
  print('hello2')
  Frame_copy = Frame_copy.reshape(100 , 100)
  print('function')
  return Frame_copy

# This conversion is a lossless , coversion 
def compare_bs64_numpy(random_noise , random_noise_copy):
  return np.array_equal(random_noise , random_noise_copy)
