# coding: utf-8
import re, sys, codecs
import alignment, read_inf_xml, clean_annotated_tweet

def calc_alignment_sentence(sentence, rules):
  # need to consider the case of multiple non-standard words
  original_converted_list = get_original_informal_pair(sentence)
  ## hopefully, change it to multiple rules
  # current_rules = alignment.reverse_trace(table, original, converted)
  current_rules = []
  for pair in original_converted_list:
    converted = pair[0]
    original = pair[1]
    print "----before alignining ---"
    print converted, original
    current_rules.extend(alignment.rules_with_window_size(original, converted, 1))
    current_rules.extend(alignment.rules_with_window_size(original, converted, 2))
    current_rules.extend(alignment.rules_with_window_size(original, converted, 3))
  for rule in current_rules:
    #print rule
    if not rules.has_key(rule):
      rules[rule] = 1
    else:
      rules[rule] += 1

def get_original_informal_pair(sentence):
  attributes = read_inf_xml.parse_attributes(sentence)
  if attributes == []: return [("", "")]
  converted_original_list = []
  i = 0
  while i + 3 < len(attributes):
    converted = clean_annotated_tweet.filter_juman_interjection(attributes[i + 3])
    print "converted = " + converted 
    original = attributes[i]
    pair = (converted, original)
    converted_original_list.append(pair)
    i += 4
  '''
  print "--------printing attributes"
  for p in attributes:
    print p
  for pair in converted_original_list:
    print pair[0], pair[1]
  '''
  return converted_original_list

def filter_juman_interjection(raw_segment):
  ret_segment = re.sub(u"（感動詞(,)?(非標準表記|長音挿入)?）", "", raw_segment)
  return ret_segment

def calc_alignment():
  # calculats the frequency, as the initialization of the convergence
  argv = sys.argv
  f_in = codecs.open(argv[1], "r", "utf-8")
  f_out = codecs.open(argv[1] + "_alignment", "w", "utf-8")
  rules = {}
  for line in f_in:
    calc_alignment_sentence(line[:-1], rules)
  # calculate the rules applied for each sentence
  #print out the simple frequency
  for k, v in sorted(rules.items(), key=lambda x:x[1]):
    if k[0] == k[1]: continue
    print k[0] + " -> " + k[1] + " " + str(rules[k])
    f_out.write(k[0] + " -> " + k[1] + " " + str(rules[k]) + "\n")
  return rules

def calc_conditional_prob(rules):
  rules_prob = {}
  total_formal_count = {}
  # calculating the total number of a specific informal chracter
  for k, v in rules.items():
    #TODO: consider the pair, not only the informal word
    before = k[0]
    if k[0] not in total_formal_count:
      total_formal_count[k[0]] = v  # informal character
    else:
      total_formal_count[k[0]] += v
  for k, v in rules.items():
    rules_prob[k] = (1.0 * v) / total_formal_count[k[0]]
  return rules_prob

def calc_current_conditional_prob():
  rules = calc_alignment()
  for k, v in sorted(calc_conditional_prob(rules).items(), key=lambda x:x[1]):
    if k[0] == k[1]: continue
    print k[0] + " -> " + k[1] + " " + str(v)

if __name__ == "__main__":
  calc_current_conditional_prob()
