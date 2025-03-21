import numpy
from sklearn import linear_model
import pandas as pd
import csv
from sklearn.preprocessing import OrdinalEncoder
from matplotlib import pyplot as plt

elo_array = []
cpl_array = []
blunder_array = []
match_array = []
cheater_array = []

cpl_array1 = []
cpl_array2 = []
cpl_array3 = []
cpl_array4 = []
cpl_array5 = []
cpl_array6 = []
cpl_array7 = []
cheater_array1 = []
cheater_array2 = []
cheater_array3 = []
cheater_array4 = []
cheater_array5 = []
cheater_array6 = []
cheater_array7 = []
match_array1 = []
match_array2 = []
match_array3 = []
match_array4 = []
match_array5 = []
match_array6 = []
match_array7 = []
blunder_array1 = []
blunder_array2 = []
blunder_array3 = []
blunder_array4 = []
blunder_array5 = []
blunder_array6 = []
blunder_array7 = []

training_data = open("/Users/harry/Documents/Project_Git/hxw285/training_data.csv", "r")
reader = csv.reader(training_data)
for line in reader:
  elo_array.append(float(line[0]))
  cpl_array.append(float(line[1]))
  blunder_array.append(float(line[2]))
  match_array.append(float(line[3]))
  cheater_array.append(float(line[4]))

def split_by_elo():

      count = 0

      for elo in elo_array:
            if elo > 2299:
                  cpl_array1.append(cpl_array[count])
                  cheater_array1.append(cheater_array[count])
                  match_array1.append(match_array[count])
                  blunder_array1.append(blunder_array[count])
            elif elo > 2199:
                  cpl_array2.append(cpl_array[count])
                  cheater_array2.append(cheater_array[count])
                  match_array2.append(match_array[count])
                  blunder_array2.append(blunder_array[count])
            elif elo > 1999:
                  cpl_array3.append(cpl_array[count])
                  cheater_array3.append(cheater_array[count])
                  match_array3.append(match_array[count])
                  blunder_array3.append(blunder_array[count])
            elif elo > 1799:
                  cpl_array4.append(cpl_array[count])
                  cheater_array4.append(cheater_array[count])
                  match_array4.append(match_array[count])
                  blunder_array4.append(blunder_array[count])
            elif elo > 1599:
                  cpl_array5.append(cpl_array[count])
                  cheater_array5.append(cheater_array[count])
                  match_array5.append(match_array[count])
                  blunder_array5.append(blunder_array[count])
            elif elo > 1399:
                  cpl_array6.append(cpl_array[count])
                  cheater_array6.append(cheater_array[count])
                  match_array6.append(match_array[count])
                  blunder_array6.append(blunder_array[count])
            else:
                  cpl_array7.append(cpl_array[count])
                  cheater_array7.append(cheater_array[count])
                  match_array7.append(match_array[count])
                  blunder_array7.append(blunder_array[count])
            count += 1

split_by_elo()

def get_probabilities(x_array, y_array):
      X = numpy.array(x_array).reshape(-1,1)
      Y = numpy.array(y_array)

      logr = linear_model.LogisticRegression()
      logr.fit(X, Y)

      def logit_to_prob(logr, X):
            log_odds = logr.coef_ * X + logr.intercept_
            odds = numpy.exp(log_odds)
            probability = odds / (1 + odds)
            return(probability)

      probabilities = []

      for prob in logit_to_prob(logr, X):
            probabilities.append(float(prob[0]))

      return(probabilities)

#print(get_probabilities(cpl_array5, cheater_array5))

def probability_average(data_array, cheat_array):

      probabilities_array = get_probabilities(data_array, cheat_array)

      count = 0
      non_cheater_total = 0
      non_cheater_count = 0
      cheater_total = 0
      cheater_count = 0
      highest_cheater_chance = 0
      lowest_cheater_chance = 1

      for probability in probabilities_array:
            cheater = cheat_array[count]
            if cheater == 0:
                  cheater = "No"
            else:
                  cheater = "Yes"
            probability = [probability, cheater]
            if cheater == "No":
                  non_cheater_total += probability[0]
                  non_cheater_count += 1
                  if probability[0] < lowest_cheater_chance:
                        lowest_cheater_chance = probability[0]
            else:
                  cheater_total += probability[0]
                  cheater_count += 1
                  if probability[0] > highest_cheater_chance:
                        highest_cheater_chance = probability[0]
            print(probability)
            count += 1

      non_cheater_odds = non_cheater_total / non_cheater_count
      cheater_odds = cheater_total / cheater_count
      print("Non-cheater average:", non_cheater_odds)
      print(f"Lowest cheater chance: {lowest_cheater_chance}%")
      print("Cheater average:", cheater_odds)
      print(f"Highest cheater chance: {highest_cheater_chance}%")

#probability_average(cpl_array6, cheater_array6)

def predict_cheater(x_array, y_array, input):
      X = numpy.array(x_array).reshape(-1,1)
      Y = numpy.array(y_array)

      logr = linear_model.LogisticRegression()
      logr.fit(X, Y)

      prediction = logr.predict(numpy.array([input]).reshape(-1,1))
      if prediction[0] == 0:
            return("No")
      else:
            return("Yes")

print(predict_cheater(cpl_array5, cheater_array5, 15))
print(predict_cheater(match_array5, cheater_array5, 50))
print(predict_cheater(blunder_array5, cheater_array5, 1))

def plot_graph(data_array, cheat_array, title, x_label):

      c = {'chosen_data': data_array, 'cheater': cheat_array}

      cf = pd.DataFrame(data=c)

      print(cf)

      is_a_cheater = [0, 1]

      enc = OrdinalEncoder(categories = [is_a_cheater])

      cf['cheater'] = enc.fit_transform(cf[['cheater']])

      print(cf)

      plt.scatter(cf.chosen_data, cf.cheater)
      plt.title(title)
      plt.xlabel(x_label)
      plt.ylabel("Cheater")
      plt.yticks([0, 1], ['No', 'Yes'])

      plt.show()

plot_graph(cpl_array1, cheater_array1, "2299 < ELO < 3191", "Average Centipawn Loss")
plot_graph(cpl_array2, cheater_array2, "2199 < ELO < 2300", "Average Centipawn Loss")
plot_graph(cpl_array3, cheater_array3, "1999 < ELO < 2200", "Average Centipawn Loss")
plot_graph(cpl_array4, cheater_array4, "1799 < ELO < 2000", "Average Centipawn Loss")
plot_graph(cpl_array5, cheater_array5, "1599 < ELO < 1800", "Average Centipawn Loss")
plot_graph(cpl_array6, cheater_array6, "1399 < ELO < 1600", "Average Centipawn Loss")
plot_graph(cpl_array7, cheater_array7, "1319 < ELO < 1400", "Average Centipawn Loss")

plot_graph(match_array1, cheater_array1, "2299 < ELO < 3191", "Stockfish Match %")
plot_graph(match_array2, cheater_array2, "2199 < ELO < 2300", "Stockfish Match %")
plot_graph(match_array3, cheater_array3, "1999 < ELO < 2200", "Stockfish Match %")
plot_graph(match_array4, cheater_array4, "1799 < ELO < 2000", "Stockfish Match %")
plot_graph(match_array5, cheater_array5, "1599 < ELO < 1800", "Stockfish Match %")
plot_graph(match_array6, cheater_array6, "1399 < ELO < 1600", "Stockfish Match %")
plot_graph(match_array7, cheater_array7, "1319 < ELO < 1400", "Stockfish Match %")

plot_graph(blunder_array1, cheater_array1, "2299 < ELO < 3191", "Blunder %")
plot_graph(blunder_array2, cheater_array2, "2199 < ELO < 2300", "Blunder %")
plot_graph(blunder_array3, cheater_array3, "1999 < ELO < 2200", "Blunder %")
plot_graph(blunder_array4, cheater_array4, "1799 < ELO < 2000", "Blunder %")
plot_graph(blunder_array5, cheater_array5, "1599 < ELO < 1800", "Blunder %")
plot_graph(blunder_array6, cheater_array6, "1399 < ELO < 1600", "Blunder %")
plot_graph(blunder_array7, cheater_array7, "1319 < ELO < 1400", "Blunder %")
