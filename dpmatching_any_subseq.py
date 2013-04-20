#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Given an target word, this code extracts a subsequence which edit distance is one.
# e.g. TARGET WORD: sleep INPUT: I want to slep ASAP. OUTPUT: slep
# levenshtein distance referred from http://d.hatena.ne.jp/naoya/20090329/1238307757
def levenshtein_distance(a, b):
  m = [[0]*(len(b)+1) for i in range(len(a)+1)]
  for i in xrange(len(a)+1):
    #the upper distance
    m[i][0] = 0
  for j in xrange(len(b)+1):
    m[0][j] = j
  for i in xrange(1, len(a)+ 1):
    for j in xrange(1, len(b)+1):
      if a[i-1] == b[j-1]:
        x = 0
      else:
        x = 1
      m[i][j] = min(m[i-1][j] + 1, m[i][j-1] + 1, m[i-1][j-1] + x)
  #return m[-1][-1]
  return m

def find_min_edit_place(dp_array):
  len_x = len(dp_array)
  len_y = len(dp_array[0]) - 1
  now_indice = 0
  now_max = 4 #since おはよう is length 4
  for i in range(len_x):
    if now_max >= dp_array[i][len_y]:
      now_max = dp_array[i][len_y]
      now_indice = i
  # the real now indice is +1 but ok for the purpose of extracting subsequence
  # limit to edit distance = 1
  if now_max <= 1:
    return now_indice
  else: 
    return -1

def find_begin_indice(dp_array, end_indice):
  now_indice = end_indice
  now_y_indice = len(dp_array[0]) - 1
  
  #look upper part or left hand corner
  while(now_y_indice != 1):
    # heading for upper left hand
    if dp_array[now_indice][now_y_indice - 1] >= dp_array[now_indice - 1][now_y_indice-1]:
       now_indice -= 1
    now_y_indice -= 1
  # due to the empty string inserted at the dp_array
  return now_indice-1

def extract_subseq(a, b):
  dp_array = levenshtein_distance(a, b)
  end_indice = find_min_edit_place(dp_array)
  if end_indice == -1: return 'edit distance not 1'
  begin_indice = find_begin_indice(dp_array, end_indice)
  return a[begin_indice : end_indice]

if __name__ == '__main__':        
  import sys
  
  s1 = sys.argv[1]
  s2 = sys.argv[2]
  s1_encoded = unicode(s1, sys.stdin.encoding)
  
  
  dp_array = levenshtein_distance(unicode(s1, sys.stdin.encoding), unicode(s2, sys.stdin.encoding))
  
  end_indice = find_min_edit_place(dp_array)
  begin_indice = find_begin_indice(dp_array, end_indice)
  
  print begin_indice, end_indice
  print s1_encoded[begin_indice : end_indice]
