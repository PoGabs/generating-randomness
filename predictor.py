triads = ("000", "001", "010", "011", "100", "101", "110", "111")


def generate_predictions(triad_stats):
    """This function takes triad statistics
    and returns a dictionary containing
    the triads as keys and the corresponding prediction
    for each triad as a value (0 or 1)."""
    most_likely_triads = {}
    for triad in triads:
        most_likely_triads[triad] = triad_stats[triad].index(max(triad_stats[triad]))
    return most_likely_triads


def prediction(triad_probabilities, user_string):
    """Returns a predicted string using a dictionary
    of triads with corresponding predictions"""
    prediction_string = ""
    first_slice = 0
    while first_slice < len(user_string) - 3:
        next_digit = str(triad_probabilities[user_string[first_slice:first_slice+3]])
        prediction_string = prediction_string + next_digit
        first_slice += 1
    return prediction_string


def calculate_right_percentage(first_string, second_string):
    """Generate similarity percentage between two strings.
    Second string must be smaller"""
    comparison_string = first_string[3:]
    matches = 0
    zipped_strings = zip(comparison_string, second_string)
    for item in zipped_strings:
        if item[0] == item[1]:
            matches += 1
    percentage = round(matches / len(second_string) * 100, 2)
    return matches, percentage


data_string = ""
upper_limit = 100

print("Please provide AI some data to learn...")
print("The current data length is 0, 100 symbols left")

while len(data_string) < upper_limit:
    print("Print a random string containing 0 or 1:")
    print()
    user_input = input()
    for i in user_input:
        if i in ("0", "1"):
            data_string += i
    if len(data_string) < upper_limit:
        print(f"Current data length is {len(data_string)}, {upper_limit - len(data_string)} symbols left")
print("Final data string:")
print(data_string)
slice_list = [data_string[symbol:symbol + 4] for symbol in range(0, len(data_string))]
final_list = []
for i in slice_list:
    if len(i) == 4:
        final_list.append(i)

main_dict = {}
for i in triads:
    main_dict[i] = [0, 0]

for i in final_list:
    current_triad = i[0:3]
    digit_following_current_triad = i[3]
    if digit_following_current_triad == "0":
        main_dict[current_triad][0] += 1
    elif digit_following_current_triad == "1":
        main_dict[current_triad][1] += 1


triad_predictions = generate_predictions(main_dict)
balance = 1000
print("You have $1000. Every time the system successfully predicts your next press, you lose $1.")
print("Otherwise, you earn $1. Print \"enough\" to leave the game. Let's go!")
while True:
    while True:
        print("Print a random string containing 0 or 1:")
        play_string = input()
        if play_string == "enough":
            print("Game over!")
            exit()
        if any(char.isalpha() for char in play_string):
            continue
        if len(play_string) > 3:
            break
    print("predictions:")
    predicted_triad = prediction(triad_predictions, play_string)
    print(predicted_triad)
    percentage_match = calculate_right_percentage(play_string, predicted_triad)
    print()
    print(f"Computer guessed {percentage_match[0]}"
          f"out of {len(predicted_triad)} symbols right"
          f"({percentage_match[1]} %)")
    # reducing balance according to how much the computer guessed
    balance -= percentage_match[0]
    # increasing balance according to how much the computer did not guess
    balance += len(predicted_triad) - percentage_match[0]
    print(f"Your balance is now ${balance}")
