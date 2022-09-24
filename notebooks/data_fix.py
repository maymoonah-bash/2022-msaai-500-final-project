import re
string = open("..\data\car_price_prediction.csv", encoding="utf8").read()
new_str = re.sub("[^a-zA-Z0-9\n\.\,]", ' ', string)
open('b.txt', 'w').write(new_str)