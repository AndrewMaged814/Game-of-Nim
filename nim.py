import random
from PIL import Image, ImageDraw, ImageFont


CHOOSE_BAG_STRING = 'select a bag: '
REMOVE_OBJECT_STRING = 'select number of objects: '
DELIMITERS = '-'*20
WINNING_IMG_PATH = 'winning.jpg'
LOSING_IMG_PATH = 'losing.jpg'


class Player:
    '''Class Player identify weather the player is computer or human and remove balls from bags
    :param  is_human: bool, optional Indicates whether the player is a human (True) or a computer (False), by default True
    :attribute     
    name: str
        The name of the player, either entered by the user or "Computer" if the player is a computer
    choise_bag: int
        The index of the bag that the player has selected to remove objects from
    choise_remove: int
        The number of objects that the player has selected to remove from the selected bag

    '''

    def __init__(self, is_human=True):
        self.is_human = is_human
        self.name = input("Username: ") if is_human else "Computer"

    def remove_objects(self, game):
        if self.is_human:
            self.choise_bag = game.check__input(
                1, 3, CHOOSE_BAG_STRING)
            self.choise_remove = game.check__input(
                1, 5, REMOVE_OBJECT_STRING)

        else:
            if game.difficulty == 1:
                game.easy_level(self)
            elif game.difficulty == 2:
                game.medium_level(self)
        game.check_can_remove(self.choise_bag, self.choise_remove, self)

    def random_choose(self):
        self.choise_bag = random.randint(1, 3)
        self.choise_remove = random.randint(1, 5)


class Game:
    """A class that holds the logic for the game

    :attributes
    gameover (bool): Flag indicating whether the game is over or not. Default is False.
    bags (list of ints): A list of integers representing the number of balls in each bag. Default is [10, 10, 10].

    """

    def __init__(self):
        self.gameover = False
        self.bags = [10, 10, 10]

    def check_can_remove(self, bag_index, remove_amount, player):
        """  Verifies if the player can remove the specified amount of balls from the specified bag. 
        If it's possible, the balls are removed and a message is printed. Otherwise, the player is asked to remove objects again."""

        if self.bags[bag_index - 1] >= remove_amount:
            self.bags[bag_index - 1] -= remove_amount
            print(f"{player.name} removed {remove_amount} from bag {bag_index}")
        else:
            print(
                f"{player.name} tried to remove {remove_amount} from bag {bag_index}, but its empty")
            player.remove_objects(self)

    def check__input(self, lower_bound, upper_bound, input_string):
        while True:
            try:
                number = int(input(input_string))
                if lower_bound <= number <= upper_bound:
                    return number
                else:
                    raise ValueError
            except (TypeError, ValueError):
                print('please select a correct number.\n\n')

    def easy_level(self, player):
        player.choise_bag = random.randint(1, 3)
        player.choise_remove = random.randint(1, 5)

    def medium_level(self, player):
        ''' Implement the nim-max algorithm
          The algorithm tries to find the optimal move for the computer
            player such that the other player is left with no winning move.'''
        nim_sum = self.bags[0] ^ self.bags[1] ^ self.bags[2]

        # If the nim_sum is not equal to 0, it means there is a winning move for the current player.
        if nim_sum != 0:
            for i in range(len(self.bags)):
                if self.bags[i] != 0:
                    # The result of choise removal will result the nim_sum result to be zero
                    if (self.bags[i] ^ nim_sum) < self.bags[i]:
                        player.choise_bag = i + 1
                        player.choise_remove = self.bags[i] - \
                            (self.bags[i] ^ nim_sum)
                        if player.choise_remove > 5:
                            self.easy_level(player=player)
                        break
        else:
            # Random move if nim_sum is 0
            self.easy_level(player=player)

    def print_bag(self):
        bag = ' - '.join(str(v) for v in self.bags)
        print(bag)

    def check_win(self, player):
        if sum(self.bags) == 0:
            self.gameover = True
            if player.is_human:
                message = f"Congratulations {player.name}, you won!!!"
                self.show_image(WINNING_IMG_PATH, message)
            else:
                message = "The computer won.. try harder next time okay? "
                self.show_image(LOSING_IMG_PATH, message)

        
    def show_image(self, path, message):
        """ shows an Image and add text on it using PIL libaray"""
        img = Image.open(path)

        I1 = ImageDraw.Draw(img)

        myFont = ImageFont.truetype('impact.ttf', 20)

        I1.text((350, 150), message, font=myFont, fill=(255, 0, 0))
        img.show()

    def start_screen(self):
        print("Please select the difficulty level:")
        print("1. Easy")
        print("2. Medium")
        self.difficulty = self.check__input(
            1, 2, "Enter the number corresponding to your choice: ")

    def gameover_screen(self, players):
        while self.gameover:

            answer = input("Do you want to play again? (yes/no)")
            if answer.lower() == "yes":
                self.gameover = False
                self.bags = [10, 10, 10]
                self.play_game(players)
            elif answer.lower() == "no":
                print("goodbye :)")
                exit()
            else:
                print("Invalid input. Please enter yes or no.")

    def play_game(self, players):
        self.start_screen()
        while self.gameover is False:
            for player in players:
                self.print_bag()
                if (self.gameover):
                    break
                player.remove_objects(self)
                self.check_win(player)
            print(DELIMITERS)
        self.gameover_screen(players)


def main():
    # setup game
    game = Game()
    human = Player()
    ai = Player(is_human=False)

    players = [human, ai]
    print(DELIMITERS)
    game.play_game(players)


if __name__ == '__main__':
    main()
