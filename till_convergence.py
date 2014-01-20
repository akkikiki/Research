# coding: utf-8
import sys, codecs, calc_alignment
from node import Node

def iterate_till_converge():
  argv = sys.argv
  mean = 2 # intialize for the probability
  # THRESHOLD = 0.00001 # based on heuristics, 0 in the original paper???
  rules_prob = initialize()
  # rules_count = {}
  iteration = 1
  while mean != 0.0:#mean > THRESHOLD:
    rules_count = {}
    print "--------num. of iteration = " + str(iteration)
    f = codecs.open(argv[1], "r", "utf-8")
    for line in f:
      original_converted_list = calc_alignment.get_original_informal_pair(line[:-1])
      #if original_converted_list[0][0] == "" and original_converted_list[0][1] == "":
      if original_converted_list == [("", "")]:
        continue
      for pair in original_converted_list:
        converted = pair[0]
        original = pair[1]
        rules_count, rules = select_optimal_path(original, converted, rules_prob, rules_count)
    iteration += 1
    new_rules_prob = calc_alignment.calc_conditional_prob(rules_count)
    mean = calc_difference(rules_prob, new_rules_prob)
    rules_prob = new_rules_prob
    #mean = 0.0 # testing
  print "--------num. of iteration ended at = " + str(iteration)
  return new_rules_prob, rules_count

def select_optimal_path_no_count(original, converted, rules_prob, rules_count):
  # producing a new rules, frequency dictionary for the current data
  # each node needs 1.prob. 2.indices of the prvious node
  # initialization
  node_matrix = [[Node((-1, -1), None, ("", ""), 1.0) for j in xrange(len(converted) + 1)] for i in xrange(len(original) + 1) ]
  # for i and j < 3, initialization is necessary
  for i in xrange(len(original) + 1):
    for j in xrange(len(converted) + 1):
      if i == 0 and j == 0:
        node_matrix[0][0] = Node((0, 0), None, ("", ""), 1.0)
        continue # avoid prob being updated to 0.0
      flag, prob, prev_node, rule = calc_optimal_prev_node(node_matrix, i, j, original, converted, rules_prob)
      if not flag:
        continue # the rule does not exist in the rules_prob dictionary
      node_matrix[i][j] = Node((i, j), prev_node, rule, prob)
  rules = trace_optimal_path(node_matrix)
  return rules_count, rules

def initialize():
  # returns rules with their initial probability
  rules = calc_alignment.calc_alignment()
  return calc_alignment.calc_conditional_prob(rules)

def select_optimal_path(original, converted, rules_prob, rules_count):
  # producing a new rules, frequency dictionary for the current data
  # each node needs 1.prob. 2.indices of the prvious node
  # initialization
  node_matrix = [[Node((-1, -1), None, ("", ""), 1.0) for j in xrange(len(converted) + 1)] for i in xrange(len(original) + 1) ]
  # for i and j < 3, initialization is necessary
  for i in xrange(len(original) + 1):
    for j in xrange(len(converted) + 1):
      if i == 0 and j == 0:
        node_matrix[0][0] = Node((0, 0), None, ("", ""), 1.0)
        continue # avoid prob being updated to 0.0
      flag, prob, prev_node, rule = calc_optimal_prev_node(node_matrix, i, j, original, converted, rules_prob)
      if not flag:
        continue # the rule does not exist in the rules_prob dictionary
      node_matrix[i][j] = Node((i, j), prev_node, rule, prob)
  print_node_matrix(node_matrix) 
  rules = trace_optimal_path(node_matrix)
  for rule in rules:
    if rule not in rules_count:
      rules_count[rule] = 1
    else:
      rules_count[rule] += 1
  return rules_count, rules

def calc_optimal_prev_node(node_matrix, i_in, j_in, original, converted, rules_prob):
  left_max = max(0, j_in-3)
  upper_max = max(0, i_in-3)
  #prob = 0
  prob = sys.float_info.min # underflow??
  # ret_prev_node = Node((-1, -1), None, ("", ""), 0.0) # path not being considered as prob = 0 when there is no rule in the distionary
  ret_prev_node = node_matrix[upper_max][left_max] # initialized at left-upper node within a window
  if i_in - upper_max < 1: # i - 1 may be -1
    org = ""
  else:
    org = original[upper_max:i_in]
  if j_in - left_max < 1:
    conv = ""
  else:
    conv = converted[left_max:j_in]

  # ret_rule = ("", "") # for self_referring case
  ret_rule = (org, conv) # for self_referring case
  i_in_increment = i_in + 1
  j_in_increment = j_in + 1
  for i in xrange(upper_max, i_in_increment):
    if i_in - i < 1: # i - 1 may be -1
      org = ""
    else:
      org = original[i:i_in]

    for j in xrange(left_max, j_in_increment):
      if i == i_in and j == j_in:
        continue # self referring
      prev_node = node_matrix[i][j]
      if j_in - j < 1:
        conv = ""
      else:
        conv = converted[j:j_in]

      rule = (org, conv)
      print "current rule considering: " + org + " -> " + conv
      print "current position in previous window i: " + str(i) + " j:" + str(j)
      print "current node considering in the original matrix i_in: " + str(i_in) + " j_in:" + str(j_in)
      print ""
      if not rule in rules_prob:
        #return False, None, None, None
        continue # to the next previous node window
      trans_prob = rules_prob[rule]
      # what happens for the ties??, in this case, first one appearing will be selected
      print prev_node.get_prob() * trans_prob
      if prev_node.get_prob() * trans_prob > prob:
        print "!!!!!!!!!!!the above prob is considered!!!!!!!"
        ret_rule = rule
        prob = prev_node.get_prob() * trans_prob
        ret_prev_node = prev_node
        print ret_prev_node.get_position()
  print "--- the prob. of rule is set as " + str(prob)
  return True, prob, ret_prev_node, ret_rule

# better to write a class of a node
# use the OOP paradigm and the code will be revised
def trace_optimal_path(node_matrix):
  rules = []
  end_node = node_matrix[-1][-1]
  print "---info. about the ending node--"
  end_node.show_info()
  prev_node = end_node.get_prev_node()
  current_node = end_node
  while current_node.get_position() != (0, 0):
    print "prev. node position at " + str(prev_node.get_position())
    rules.append(current_node.get_rule())
    current_node = prev_node
    prev_node = current_node.get_prev_node()
  return rules

def print_node_matrix(node_matrix):
  for i in xrange(len(node_matrix)):
    for j in xrange(len(node_matrix[i])):
      node_matrix[i][j].show_info()

def calc_difference(rules_prob, new_rules_prob):
  # keys which appear in both dictionaries are added twice
  total_diff = 0
  for k, v in rules_prob.items():
    # TODO: we are not considering all rules
    if not k in new_rules_prob:
      new_rules_prob[k] = 0.0
    total_diff += abs(rules_prob[k] - new_rules_prob[k])

  for k, v in new_rules_prob.items():
    if not k in rules_prob:
      rules_prob[k] = 0.0
    total_diff += abs(rules_prob[k] - new_rules_prob[k])
  return total_diff / len(rules_prob)

def write_dic(dic, f_out):
  for k, v in sorted(dic.items(), key=lambda x:x[1]):
    if k[0] == k[1] or v == 0.0:
      continue
    out = k[0] + " -> " + k[1] + " " + str(v)
    f_out.write(out + "\n")

def write_dic_concurrently(count_dic, rule_dic, f_out):
  for k, v in sorted(count_dic.items(), key=lambda x:x[1], reverse = True):
   if k[0] == k[1] or v == 0.0:
     continue
   out = k[0] + " -> " + k[1] + "\t" + str(v) + "\t" + str(rule_dic[k])
   f_out.write(out + "\n")

if __name__ == "__main__":
  argv = sys.argv
  rules_prob, rules_count = iterate_till_converge()
  f_out = codecs.open(argv[1] + "_converged_rules", "w", "utf-8")
 
  write_dic_concurrently(rules_count, rules_prob, f_out)
  #write_dic(rules_count, f_out)
  #write_dic(rules_prob, f_out)
