#!/usr/bin/env python3
"""
Author: Elijah Harmon
Description:
"""

def main():
    user_input = input("> ")

    try:
        user_input = int(user_input)
    except:
        print()
        exit("Error")

    for x in range(0, user_input):
        print(x)

if __name__ == '__main__':
    main()
