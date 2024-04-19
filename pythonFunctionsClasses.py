myString = 'Python is great \n'
lines = 4
result = 'lines' + lines * myString
print(result)


multiples = []
for outer in range(1,2):
  multiples.append([])
  for inner in range(1,3): 
    multiples[outer-1].append(inner)
print(multiples)

multiples = []
for outer in range(1,3):
  multiples.append([])
  for inner in range(1,2): 
    multiples[outer-1].append(inner) 
print(multiples)


def factorial(number):
  if not isinstance(number, int):
    raise TypeError("Sorry. number must be an integer.")
  if number < 0:
     raise ValueError("Sorry. number must be zero or positive.")
  def inner_factorial(number): #nested function for calculation of factorial 
     if number <= 1:
        return 1
     return number * inner_factorial(number - 1)
  return inner_factorial(number)

print(factorial(4))

def delta(num):
   if num > 1:
      num = num - 2
   else:
      num = num + 2
   return num
  
def gamma(num):
   if num > 1:
      num = num / 2
   else:
      num = num / -2
   return num
 
def beta(num):
   if num > 1:
      num = num * 2
      num = gamma(num)
   else:
      num = num * -2
      num = delta(num)
   return num
 
def alpha(num):
   if num > 0:
      num += 1
      num = beta(gamma(num))
   else:
      num -=1
      num = beta(delta(num))
   return num
  
print('output = ', alpha(0))

import math
def dB2(param1, param2):
 dB_calc = 20 * math.log10(param1/param2)
 if dB_calc > 6:
  return "High SNR"
 elif dB_calc > 0:
  return "Low SNR"
 return "Noise"

print(dB2(5,5))

my_first_list = ['a', 'b', 'c']
my_second_list = ['d', 'e', 'f', 'g']
my_third_list = my_second_list[0:1] + my_first_list[1:2]
my_third_list.append('h')
print (my_third_list[1:])