# coding: utf-8

def edit_distance(original, converted):
  table = []
  for j in xrange(len(original) + 1):
    table.append([0] * (len(converted) + 1)) # row is regarded as a deep copy, so we need to generate a separate array
  print table
  for i in xrange(len(original) + 1):
    table[i][0] = i
  for j in xrange(len(converted) + 1):
    table[0][j] = j
  for i in xrange(1, len(original) + 1):
    for j in xrange(1, len(converted) + 1):
      if original[i-1] == converted[j-1]:
        x = 0
      else:
        x = 1
      
      min_trans = min(table[i-1][j] + 1, table[i][j-1] + 1, table[i-1][j-1] + x)
      table[i][j] = min_trans
  print table
  return table

def reverse_trace(table, original, converted):
  i = len(table) - 1
  j = len(table[i]) - 1
  current = table[i][j]
  rules = []
  while i > 0 or j > 0:
    i_positive = (i > 0)
    j_positive = (j > 0)
    # the table is already built
    min_trans = max(len(table) + 1, len(table[i]) + 1) # num. which do not exist in the table
    if i_positive:
      min_trans = min(min_trans, table[i-1][j])
    if j_positive:
      min_trans = min(min_trans, table[i][j-1])
    if i_positive and j_positive:
      min_trans = min(min_trans, table[i-1][j-1])
    # transition from the upper element
    if i_positive and j_positive and min_trans == table[i-1][j-1]:
      #print original[i-1] + " -> " + converted[j-1]
      rules.append((original[i-1], converted[j-1]))
      i -= 1
      j -= 1
    elif i_positive and min_trans == table[i-1][j]:
      print original[i-1] + " -> null"
      rules.append((original[i-1], ""))
      i -= 1
    # transition from the left element
    elif j_positive and min_trans == table[i][j-1]:
      print "null -> " + converted[j-1]
      rules.append(("", converted[j-1]))
      j -= 1
   
  return rules

def consider_window_size_two(rules):
   for i in xrange(1, len(rules)):
     print rules[i][0] + rules[i-1][0] + " -> " + rules[i][1] + rules[i-1][1]
     new_rule = [rules[i][0] + rules[i-1][0], rules[i][1] + rules[i-1][1]]

def consider_window(rules, j):
   aligned_rules = []
   for i in xrange((j-1), len(rules)):
     before = ""
     after = ""
     for win_size in xrange(1, j+1):
       before += rules[i-(win_size-1)][0]
       after += rules[i-(win_size-1)][1]
     print before + " -> " + after
     aligned_rules.append((before, after))
   return aligned_rules

def rules_with_window_size(original, converted, j):
  table = edit_distance(original, converted)
  rules = reverse_trace(table, original, converted)
  return consider_window(rules, j)

if __name__ == "__main__":
  table = edit_distance(u"かなり", u"かなぁーり")
  rules = reverse_trace(table, u"かなり", u"かなぁーり")
  #consider_window_size_two(rules)
  #consider_window(rules, 2)
  #consider_window(rules, 3)
  rules_with_window_size(u"かなり", u"かなぁーり", 2)
  rules_with_window_size(u"かなり", u"かなぁーり", 3)
  rules_with_window_size(u"かなり", u"かなぁーり", 1)
  rules_with_window_size(u"ということ", u"ってこと", 1)
