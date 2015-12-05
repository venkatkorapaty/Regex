"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, Venkat Korapaty,
# 2013, 2014, 2015
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2015
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.


def is_regex(s):
    '''(string) -> bool
    Takes a string s, and returns True if it is a valid regular expression
    else, returns False
    >>> is_regex('0')
    True
    >>> is_regex('2*')
    True
    >>> is_regex('((1.(0|2)*).0)')
    True
    >>> is_regex('wot')
    False
    >>> is_regex('(3.0)')
    False
    '''
    # base case
    if s == '':
        return False
    # checks if the regex is either '1', '2', '0' or 'e'
    if len(s) == 1:
        if s in {'0', '1', '2', 'e'}:
            return True
        return False
    # if the regex has an asterick at the end, recurses without the asterick
    elif s[-1] == '*':
        return is_regex(s[:-1])
    # if the regex's have brackets at the end
    elif s[0] == '(' and s[len(s) - 1] == ')':
        # finds location of the root
        dot_bar = dot_bar_loca(s)
        # if the root return is False, then it is an invalid regex
        if dot_bar is False:
            return False
        # recurse by splitting them and retuns True if they are both True
        return is_regex(s[1:dot_bar]) and is_regex(s[dot_bar + 1:len(s) - 1])
    else:
        return False


def parenthesis(s, count=0):
    '''(str, int) -> int or bool
    Finds the closing parethesis index for the respective opening parenthesis.
    REQ: s[0] == '('
    REQ: amount of opening brackets == amount of closing brackets
    >>> parenthesis('(1|2)')
    4
    >>> parenthesis('(((1.(0|2)*).0))')
    15
    >>> parenthesis('((()))')
    5
    '''
    if s == '':
        return False
    # if it starts with an opening bracket, recurses and adds to the count
    if s[0] == '(':
        return 1 + parenthesis(s[1:], count + 1)
    # if it is not a closing bracket, dont add to the count and recurse
    if s[0] != ')':
        return 1 + parenthesis(s[1:], count)
    # if it is a closing bracket
    elif s[0] == ')':
        # it has reached the end and returns the index
        if count - 1 == 0:
            return 0
        # it has reached a closing bracket before the desired one
        return 1 + parenthesis(s[1:], count - 1)


def all_regex_permutations(s):
    '''(str or list) -> list
    Takes in a regular expression and returns all permutations of it
    that are valid regular expressions
    (Brute-force method)
    >>> all_regex_permutations('3')
    set()
    >>> all_regex_permutations('2*')
    {'2*'}
    >>> all_regex_permutations('(1.e)')
    {'(e.1)', '(1.e)'}
    >>> all_regex_permutations('((e*.1)|1)')
    {'((e.1)|1)*', '((1|1).e)*', '((1|e).1*)', '((1*|e).1)', '(1.(e|1*))',\
 '(e.(1|1))*', '(1.(1*|e))', '((e.1*)|1)', '(1.(1|e*))', '(1.(e|1))*',\
 '(e|(1.1))*', '(1.(e|1)*)', '((1*|1).e)', '((1|e)*.1)', '(1*|(1.e))',\
 '(1.(e*|1))', '((e|1)*.1)', '(1.(1|e))*', '(e.(1|1*))', '(e.(1|1)*)',\
 '((e|1*).1)', '(1*.(1|e))', '((1.e)|1*)', '((1.e)*|1)', '(e*.(1|1))',\
 '((1.1)|e)*', '((1.1)*|e)', '(1|(e.1*))', '((e|1).1*)', '(e|(1.1*))',\
 '(e|(1.1)*)', '((1.e)|1)*', '((1|e).1)*', '((1.1)|e*)', '((e|1).1)*',\
 '(1|(e*.1))', '(1|(1.e*))', '(1|(1.e))*', '(1|(e.1)*)', '(e|(1*.1))',\
 '(1*.(e|1))', '((e.1)|1*)', '((e.1)*|1)', '((1|1).e*)', '((e*|1).1)',\
 '((e*.1)|1)', '((1|1)*.e)', '((1*.e)|1)', '((1.e*)|1)', '((1.1*)|e)',\
 '((1|1*).e)', '((1*.1)|e)', '(1.(1|e)*)', '(e*|(1.1))', '((1|e*).1)',\
 '(1*|(e.1))', '(1|(1*.e))', '(e.(1*|1))', '(1|(1.e)*)', '(1|(e.1))*'}

    '''
    # finds all the possible permutations of the regex string
    perm_list = perm(s)
    # intializes the set to be returned
    regex_perms = set()
    # for each element in the permutation list
    for element in perm_list:
        # checks whether its a valid regex and its not already in the set
        if is_regex(element):
            # adds it to the set
            regex_perms.add(element)
    return regex_perms


def perm(s):
    '''(str) -> list
    Takes in a string and returns all possible permutations of it in a list
    >>> perm('abc')
    ['cba', 'bca', 'cab', 'acb', 'bac', 'abc']
    >>> perm('uwot')
    ['towu', 'otwu', 'twou', 'wtou', 'owtu', 'wotu', 'touw', 'otuw', 'tuow',\
 'utow', 'outw', 'uotw', 'twuo', 'wtuo', 'tuwo', 'utwo', 'wuto', 'uwto',\
 'owut', 'wout', 'ouwt', 'uowt', 'wuot', 'uwot']
    '''
    if len(s) == 1:
        return [s[0]]
    # list to return
    perms = []
    # loop through entire string
    for i in range(len(s)):
        string = s[:i] + s[i + 1:]
        # finds permutations of the short regex with an index missing
        result = perm(string)
        # adds the letter at the end of each permutation of the regexs
        for element in range(len(result)):
            # adds the missing symbol from the string to the permutation
            result[element] += s[i]
            # adds the permutation to the list to be returned
            perms.append(result[element])
    return perms


def regex_match(r, s):
    '''(RegexTree, str) -> bool
    Takes in a RegexTree rooted at r and a string and checks if the string
    matches the regex, if it does, return True, else False
    >>> tree = build_regex_tree('((0.(1*.2)*)|(e*.1))*')
    >>> regex_match(tree, '01112121111112')
    True
    >>> tree = build_regex_tree('(1*.2)')
    >>> regex_match(tree, '11111112')
    True
    >>> tree = build_regex_tree('((1.2**).(0**|2))')
    >>> regex_match(tree, '12222200002')
    False
    '''
    # base case
    if isinstance(r, Leaf):
        # if the leaf is an 'e'
        if r.get_symbol() == 'e':
            # returns true if the string is empty as e represents empty string
            if s == '':
                return True
            # since string isnt empty, gives false
            return False
        # if the string is empty otherwise, it gives false
        if s == '':
            return False
        # returns whether the string is equal to the symbol
        return s == r.get_symbol()
    # deals with dot trees
    elif isinstance(r, DotTree):
        # splits the string up from every index and sends it through to the
        # left child and right child to check if they are both a string\
        for i in range(len(s) + 1):
            temp = regex_match(r.get_left_child(), s[:i]) and regex_match(
                r.get_right_child(), s[i:])
            # if both ever reach True, it will return True
            if temp:
                return True
        return False
    # deals with bar trees
    elif isinstance(r, BarTree):
        # checks if the entire string is equal to the regex left of the bar
        left = regex_match(r.get_left_child(), s)
        # checks if the entire string is equal to the regex right of the bar
        right = regex_match(r.get_right_child(), s)
        # if the left gives True, returns True
        if left:
            return True
        # if the right gives True, returns True
        if right:
            return True
        # if neither are True, then returns False
        return False
    # deals with star trees
    else:
        # if the string is empty, returns True
        if s == '':
            return True
        # calls helper function
        #return star_case(r, s)
        if regex_match(r.get_child(), s):
            return True
        else:
            if len(s) == 1:
                return regex_match(r.get_child(), s)
            return star_helper(r, s)


def star_helper(r, s):
    '''(RegexTree, str) -> bool
    This function takes the index where the part of the string matches the
    regex tree, and call star case with everything after the string to see
    if the rest of it matches, false if it does not match at all
    >>> star_helper(StarTree(BarTree(Leaf('1'), Leaf('2'))), '12')
    True
    >>> star_helper(StarTree(BarTree(Leaf('1'), Leaf('2'))), '01')
    False
    '''
    # finds the index where the shortened string is true
    temp = star_index(r, s)
    # if it gives false, then return false
    if temp is False:
        return False
    # calls star case for everything past the shorted portion of the string
    return regex_match(r, s[temp + 1:])


def star_index(r, s):
    '''(RegexTree, str) -> int or bool
    Returns the index where within the string, it keeps splicing the string
    from left to right until it reaches a point where a smaller string within
    the string matches, and returns that index, returns false if no shortened
    version of the string matches the regex
    >>> star_index(StarTree(BarTree(Leaf('1'), Leaf('2'))), '12')
    0
    >>> star_index(StarTree(DotTree(Leaf('1'), Leaf('2'))), '12222')
    1
    >>> star_index(StarTree(DotTree(Leaf('1'), Leaf('2'))), '012222')
    False
    '''
    # starts from the index at the end of the string
    i = len(s)
    # tests keeps shortening string left to right until a True case is found
    while not regex_match(r.get_child(), s[:i]):
        # theres only 1 index in s but it already tested false, meaning it
        # cannot match
        if len(s[:i]) == 1:
            return False
        # reduces index by 1
        i -= 1
    return i - 1


def build_regex_tree(regex):
    '''(str) -> RegexTree
    Takes in a valid regex and creates the regex tree for it and returns the
    rootof it.
    REQ: regex must be a valid regex
    >>> build_regex_tree('(2*|e)') == BarTree(StarTree(Leaf('2')), Leaf('e'))
    True
    >>> tree = build_regex_tree('(1.(e.2*)*)')
    >>> tree == DotTree(Leaf('1'), StarTree(DotTree(Leaf('e'), StarTree(Leaf(\
    '2')))))
    True
    '''
    # base cases
    if len(regex) == 1:
        # when the regex is just '1', '2', '0', or 'e'
        return Leaf(regex)
    elif regex[len(regex) - 1] == '*':
        # when the regex has an asterick at the end, starts with a StarTree
        return StarTree(build_regex_tree(regex[:len(regex) - 1]))
    else:
        # finds location of the bar or dot in the regex
        symbol = dot_bar_loca(regex)
        # if the regex has a dot, creates a DotTree and recurses
        if regex[symbol] == '.':
            return DotTree(build_regex_tree(regex[1:symbol]
                                            ), build_regex_tree(regex[
                                                symbol + 1:len(regex) - 1]))
        # else it must be made with a BarTree and recurses
        else:
            return BarTree(build_regex_tree(regex[1:symbol]
                                            ), build_regex_tree(regex[
                                                symbol + 1:len(regex) - 1]))


def dot_bar_loca(s, count=0, s_len=0):
    '''(str) -> int or bool
    Returns the location of the dot or bar after the first regex within the
    string
    >>> dot_bar_loca('(1|2)')
    2
    >>> dot_bar_loca('(e*.1)')
    3
    >>> dot_bar_loca('((2.e*)**|0)')
    9
    '''
    if s == '':
        return False
    # keeps the original string's length
    if s_len == 0:
        s_len = len(s) - 1
    # if this step is true, then the regex is not valid
    if count == s_len:
        return False
    if len(s) == 1:
        return False
    # if there is a regex with brackets within the regex, recurses past that
    if s[1] == '(':
        temp = parenthesis(s[1:])
        # should parenthesis return False, it means s is not a valid regex
        if temp is False:
            return False
        count += temp + 1
        return dot_bar_loca(s[count:], count, s_len)
    # if the next index in the string is not '.' or '|', recurse past it
    elif s[1] != '.' and s[1] != '|':
        return dot_bar_loca(s[1:], count + 1, s_len)
    # the desired value is found and returns it's index
    else:
        return count + 1

if __name__ == '__main__':
    print(perm("123"))