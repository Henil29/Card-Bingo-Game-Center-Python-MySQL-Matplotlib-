import random
import time
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

class CardGame:
    def __init__(self):
        
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="game"
        )
        self.mycursor = self.mydb.cursor()
        
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.deck = []
        
        for suit in suits:
            for rank in ranks:
                card = f"{rank} of {suit}"
                self.deck.append(card)
                
        random.shuffle(self.deck)
        
        self.players = {1: sorted(self.deck[:5], key=lambda card: card.split()[-1]),
                        2: sorted(self.deck[5:10], key=lambda card: card.split()[-1]),
                        3: sorted(self.deck[10:15], key=lambda card: card.split()[-1]),
                        4: sorted(self.deck[15:20], key=lambda card: card.split()[-1])}
        self.deck = self.deck[20:]
    
    def print_cards(self, player):
        
        for i, card in enumerate(self.players[player], 1):
            print(f"{i}. {card}")

    def replace_card(self, player, card_index, new_card):
        
        if 0 <= card_index < len(self.players[player]):
            removed_card = self.players[player][card_index]
            self.players[player][card_index] = new_card
            self.players[player].sort(key=lambda card: card.split()[-1])
            self.deck.append(removed_card)
            return removed_card
        else:
            print("Invalid card index.")
            return None

    def get_most_common_suit(self, player):
        
        suits_count = {}
        for card in self.players[player]:
            suit = card.split()[-1]
            suits_count[suit] = suits_count.get(suit, 0) + 1
        return max(suits_count.items(), key=lambda x: x[1])
    
    def end_game(self, winning_player, winning_suit):
        
        print(f"Game Over! Player {winning_player} wins with five {winning_suit}s!")
        print("\nWinning Cards:")
        self.print_cards(winning_player)
        self.database(winning_player)
        
    def database(self, winning_player):
        sql = "INSERT INTO card_history (winner) VALUES (%s)"
        b1 = f"player{winning_player}"
        val = (b1,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        self.mycursor.execute("SELECT count FROM card_winning_count WHERE player = %s", val)
        self.myresult = self.mycursor.fetchall()
        self.count = self.myresult[0][0] + 1
        
        self.mycursor.execute("UPDATE card_winning_count SET count = %s WHERE player = %s", (self.count, b1))
        self.mydb.commit()

        self.mycursor.close()
        self.mydb.close()
        
    def play(self):
        
        current_player = 1
        while True:
            print(f"\n>>> Player {current_player}'s Turn <<<")
            print("\nYour cards:")
            self.print_cards(current_player)

            most_common_suit = self.get_most_common_suit(current_player)
            print(f"\nSuggestion: Keep cards of {most_common_suit[0]} suit.")

            # Draw a card
            extra_card = self.deck.pop(random.randint(0, len(self.deck) - 1))
            print(f"\nYou drew a card: {extra_card}")
            player_ans = input("Do you want to keep this card? (yes/no): ").strip().lower()

            if player_ans == 'yes':
                while True:
                    try:
                        card_to_remove = int(input("Enter the number of the card to replace: ")) - 1
                        self.replace_card(current_player, card_to_remove, extra_card)
                        print("\nUpdated cards:")
                        self.print_cards(current_player)
                        break
                    except (IndexError, ValueError):
                        print("Invalid choice. Please try again.")
            else:
                self.deck.append(extra_card)

            # won or not
            most_common_suit = self.get_most_common_suit(current_player)
            if most_common_suit[1] == 5:
                self.end_game(current_player, most_common_suit[0])
                break

            current_player = 1 if current_player == 4 else current_player + 1
            time.sleep(1)
class Bingo:
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="game"
        )
        self.mycursor = self.mydb.cursor()
        
        numbers = list(range(1, 26))
        random.shuffle(numbers)
        self.player1_numbers=np.array(numbers).reshape(5,5)
        random.shuffle(numbers)
        self.player2_numbers=np.array(numbers).reshape(5,5)
        random.shuffle(numbers)
        self.player3_numbers=np.array(numbers).reshape(5,5)
        random.shuffle(numbers)
        self.player4_numbers=np.array(numbers).reshape(5,5)
        
        self.players={1:self.player1_numbers,2: self.player2_numbers,3:self.player3_numbers,4:self.player4_numbers}
        
        self.remove_number_list=[]
        
    def database(self,winning_player):
        sql = "INSERT INTO bingo_history (winner) VALUES (%s)"
        b1=f"player{winning_player}"
        val = (b1,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        
        # second table
        self.mycursor.execute(f"SELECT count FROM bingo_winning_count where player= %s",val)
        self.myresult = self.mycursor.fetchall()
        self.count=self.myresult[0][0]+1
        
        self.mycursor.execute(f"UPDATE bingo_winning_count SET count = %s WHERE player = %s", (self.count,b1))
        self.mydb.commit()

        self.mycursor.close()
        self.mydb.close()
        
    def check_bingo(self,player):
        totle_bingo={ 1:0, 2:0 ,3:0,4:0}
        
        # row check
        for i in range(5):
            row_check=0
            for j in range(5):
                if self.players[player][i][j]==0:
                    row_check+=1
            if row_check==5:
                totle_bingo[player]+=1
                
        # column check
        for i in range(5):
            column_check=0
            for j in range(5):
                if self.players[player][j][i]==0:
                    column_check+=1
            if column_check==5:
                totle_bingo[player]+=1
                
        diagonal_check1=0
        diagonal_check2=0
        for i in range(5):
            if self.players[player][i][i]==0:
                diagonal_check1+=1
            if self.players[player][i][4-i]==0:
                diagonal_check2+=1
        
        if diagonal_check1==5:
            totle_bingo[player]+=1
        if diagonal_check2==5:
            totle_bingo[player]+=1
            
        if totle_bingo[player]>=5:
            return True
        else:
            return False
        
    def remove_number(self,player,number):
        remove_number=number
        while True:
                
            if remove_number in self.remove_number_list:
                print("Number already removed. Please enter a different number.")
                remove_number=int(input("Enter the number to remove: "))
            elif remove_number>25 or remove_number<1:
                print("Invalid number. Please enter a number between 1 and 25.")
                remove_number=int(input("Enter the number to remove: "))
            else:
                self.remove_number_list.append(remove_number)
                break
         
        for i in range(5):
            for j in range(5):
                
                for k in range(1,3):
                    if self.players[k][i][j]==remove_number:
                        self.players[k][i][j]=0
                        break
    
    def ask_number(self):
        
        current_player = 1
        
        while True:
            print(f"\nPlayer {current_player}'s turn")
            print("\n",self.players[current_player])
            if self.check_bingo(current_player):
                print(f"Player {current_player} wins!")
                break
            
            while True:
                try:
                    remove_number=int(input("Enter the number to remove: "))
                    
                    break
                except ValueError:
                    print("Please enter only numbers.")
                    continue
            
            self.remove_number(current_player,remove_number)
            print(self.players[current_player])
            time.sleep(1)
            if self.check_bingo(current_player):
                print(f"Player {current_player} wins!")
                break
            
            if current_player>=4:
                current_player=1
            else:
                current_player+=1


print("\nWelcome to the Game Center!")
while(True):
    print("\nPress 1 to play the Card Game.")
    print("Press 2 to play the Bingo Game.")
    print("Press any number to exit.")
    game=""

    while True:
        try:
            choice = int(input("\nEnter your choice:"))
            break
        except ValueError:
            print("Please enter only numbers.")
            continue
    
    if(choice==1):
        game="card"
    elif(choice==2):
        game="bingo"
    else:
        print("Exiting the game center...")
        break
    
    print(f"\nWelcome to the {game} Game!")
    while(True):
        print(f"\nPress 1 to start the {game} game.")
        print("Press 2 to view the history.")
        print("Press 3 to view the winning chart.")
        print("Press 4 to exit.")

        choice = int(input("\nEnter your choice:"))
        if(choice==1 and game=="bingo"):
            game1 = Bingo()
            game1.ask_number()
        elif(choice==1 and game=="card"):
            game1 = CardGame()
            game1.play()

        elif(choice==2):
            mydb = mysql.connector.connect(
                host="localhost",
                user ="root",
                password="",
                database="game"
            )
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT * FROM {game}_history")
            myresult = mycursor.fetchall()
            print("\nHistory:")
            for x in myresult:
                print(f"{x[0]} : {x[1]}")
            mycursor.close()
            mydb.close()
            
        elif(choice==3):

            mydb = mysql.connector.connect(
                host="localhost",
                user ="root",
                password="",
                database="game"
            )
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT * FROM {game}_winning_count")
            myresult = mycursor.fetchall()
            
            winner_list=[]
            winner_name=[]
            for x in myresult:
                winner_name.append(x[1])
                winner_list.append(x[2])
            
            x=np.array(winner_list)
            y=np.array(winner_name)
            color=['red','green','blue','yellow']
            font={'family':'serif','color':'blue','weight':'bold','size':12}
            
            while(True):
                print("\nPress 1 to view the Bar graph:")
                print("Press 2 to view the Scatter plot:")
                print("Press 3 to view the Line graph:")
                print("Press 4 to view the Pie chart:")
                print("Press 5 to view all the graphs:")
                print("Press 6 to exit.")
                choice=int(input("\nEnter your choice:"))
                if(choice==1):
                    plt.bar(y,x,color=color,width=0.4,edgecolor='black',linewidth=2)
                    plt.xlabel('Player',fontdict=font)
                    plt.ylabel('Winning Count',fontdict=font)
                    plt.title("Winning Chart")
                    plt.show()
                
                elif(choice==2):
                    plt.scatter(y,x,c=x,cmap='viridis')
                    plt.xlabel('Player',fontdict=font)
                    plt.ylabel('Winning Count',fontdict=font)
                    plt.show()
                
                elif(choice==3):
                    plt.plot(y,x, marker='o',markersize=10,  markeredgecolor='r', markerfacecolor='r',linewidth='5',color='g')
                    plt.xlabel('Player',fontdict=font)
                    plt.ylabel('Winning Count',fontdict=font)
                    plt.show()
                
                elif(choice==4):
                    plt.pie(x, labels=y,autopct='%1.1f%%')
                    plt.legend(title="Player",loc="center left",bbox_to_anchor=(1,0,0.5,1))
                    plt.show()
                
                elif(choice==5):
                    plt.subplot(2, 2, 1)
                    plt.bar(y,x,color=color,width=0.4,edgecolor='black',linewidth=2)
                    plt.xlabel('Player',fontdict=font)
                    plt.ylabel('Winning Count',fontdict=font)
                    
                    plt.subplot(2, 2, 2)
                    plt.scatter(y,x,c=x,cmap='viridis')
                    plt.xlabel('Player',fontdict=font)
                    plt.ylabel('Winning Count',fontdict=font)
                    
                    plt.subplot(2, 2, 3)
                    plt.plot(y,x, marker='o',markersize=10,  markeredgecolor='r', markerfacecolor='r',linewidth='5',color='g')
                    plt.xlabel('Player',fontdict=font)
                    plt.ylabel('Winning Count',fontdict=font)
                    
                    plt.subplot(2, 2, 4)
                    plt.pie(x, labels=y,autopct='%1.1f%%')
                    plt.legend(title="Player",loc="center left",bbox_to_anchor=(1,0,0.5,1))
                    
                    
                    plt.suptitle("Winning Chart")
                    plt.tight_layout()
                    plt.show()
                
                elif(choice==6):
                    break
                else:
                    print("Invalid choice.Please try again.")
                
                print("Graphs are displayed.")
                mydb.close()
                mycursor.close()
            
        elif(choice==4):
            print(f"Exiting the {game} game...")
            break
        else:
            print("Invalid choice. Please try again.")