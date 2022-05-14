import argparse

def count_vowels(str):
    """
    Count vowels will count the number of vowels in the given string
    :param str:
    :return:
    """
    # english vowels
    vowels = ['a','e','i','o','u','y']
    # lower case the string characters
    str=str.lower()
    cnt = 0
    for i in str:
        if i in vowels:
            cnt+=1
    print(cnt)

def perfect_power_number(index):
    """
    the function will print the perfect power number of a given index
    :param index:
    :return:
    """
    index=int(index)
    ans=set()
    # we add one as default - one in power of any number is one
    ans.add(1)
    for i in range (2,index+1):
        for j in range (2,index+1):
            ans.add(i**j)
    # we sort the final list to get the right indexes
    ans= sorted(ans)
    print(ans[index-1])

def lazy_caterer_number(num):
    """
    the function will print the number of slices by receiving the number of cuts
    :param num:
    :return:
    """
    num = int(num)
    # we use num-1 because in the exercise the input will be between 1-100
    p = (num-1)**2 + (num-1) + 2
    if p % 2 == 0:
        p /= 2
        print(int(p))
    else:
        p /= 2
        print(p)

# initiate the parser and its arguments
parser = argparse.ArgumentParser()
parser.add_argument('--task',type=str)
parser.add_argument('--arg',type=str)
args = parser.parse_args()

if args.task == 'vowels':
    count_vowels(args.arg)
elif args.task == 'perfect':
    perfect_power_number(args.arg)
elif args.task == 'lazy':
    lazy_caterer_number(args.arg)
else:
    print('wrong input')
    exit()

