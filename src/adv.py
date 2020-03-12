from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons\nGo forward or be still"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}

items = {
    'sword': Item('sword', 'It looks rusty. Don\'t get tetanus!'),
    'coin': Item('coin', 'Is that gold!! Oh no wait... it is silver.'),
    'knife': Item('knife', 'Ouch sharp!'),
    'bat': Item('bat', 'Don\'t know why you would take a live animal but ok.')
}

# Link items to rooms
room['foyer'].items = [items['sword'], items['coin']]
room['overlook'].items = [items['knife']]
room['narrow'].items = [items['bat']]


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.


def try_direction(direction, room):
    attribute = direction + '_to'

    if hasattr(room, attribute):
        new_room = getattr(room, attribute)
        return new_room
    else:
        print('\nCan not go this way!!!')
        return room


user = input('What is your name? ')
if not user:
    user = "nothing"
    print('You are nothing')
player = Player(user, room['outside'])

print(f"\nWe will experiance both confounding growth and unbridled ecstasy {user}...\nare you ready? ")
print(f"only one of us are alive..\n\n..here are your rules\n")
print(f"to pick up an item type take then the items name")
print(f"e.g. take saber")
print(f"You will be stuck in a loop of misery if there is any input other than that directed.")
print(f"Lets begin")

user_input = ''
valid_input = ['n', 's', 'e', 'w', 'q']

while not user_input == 'q':
    print(player.room)
    user_input = input('Which way do you want to do or go?\n'
                      'Directions: [n] North [s] South [e] East [w] West\n'
                      'Items: take (item), drop (item), or inspect (item)\n'
                      '[i] Inventory\n'
                      'or [q] Quit:\n')

    if user_input in valid_input:

        player.room = try_direction(user_input, player.room)

    elif 'take' in user_input or 'drop' in user_input or 'inspect' in user_input:
        action = user_input.split()
        print(action)
        action_verb = action[0]
        action_item = action[1]

        try:
            item = items[action_item]

            if action_verb == 'take':
                if item in player.room.items:
                    player.room.removeItem(items[action_item])
                    player.take_item(items[action_item])
                    print(items[action_item].on_take())
                else:
                    print('\nItem is not in the room')

            elif action_verb == 'drop':
                if item in player.items:
                    player.room.addItem(items[action_item])
                    player.drop_item(items[action_item])
                    print(items[action_item].on_drop())
                else:
                    print('You do not have this item.')

            elif action_verb == 'inspect':
                if item in player.items:
                    print(item.inspect())
                else:
                    print('\nThis is not an item in your inventory.')

        except KeyError:
            print('\nThis is not an item.\n')

        print(f'{player.name}\'s items: ', player.items)

    elif user_input == 'i':
        print(f'\nYour items: {player.items}')

    elif user_input == 'q':
        print('Thanks for playing!!!')

    else:
        print('Incorrect input. Please follow instructions.')