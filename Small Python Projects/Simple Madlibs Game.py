#Simple madlibs game using fstrings

adj = input("Input an adjective: ")
noun = input("Input a noun: ")
pTenseVerb = input("Input a past tense verb: ")
adj2 = input("Input another adjective: ")
noun2 = input("Input another noun: ")
noun3 = input("Input another noun: ")
adj3 = input("Input another adjective: ")
verb = input("Input a verb: ")
adj4 = input("Input another adjective: ")

madlib = f"Today I went to the zoo. I saw a(n) {adj} {noun} jumping up and down in its tree. He {pTenseVerb} through the large tunnel\
 that led to its {adj2} {noun2}. I got some peanuts and passed them through the cage to a gigantic gray {noun3} towering above \
my head. Feeding that animal made me hungry. I went to get a {adj3} scoop of ice cream. Afterwards I had to {verb} to catch the bus!\
 When I got home I told my mom about my {adj4} day at the zoo."

print(madlib)