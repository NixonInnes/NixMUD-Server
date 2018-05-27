import re

from Channels.npc import broadcast
from Entities.class_ import Class
from Entities.race import Race
from Entities.user import User
from Handlers import handlers
from Utilities.defaults import DEFAULT_TILE


def auth(client, msg):
    """
    Manage the authorisation process:
        Register->choose race->choose class
        Login
    """
    if client.state is client.states.RACE:
        choose_race(client, msg)
        return
    if client.state is client.states.CLASS:
        choose_class(client, msg)
        return

    args = msg.strip().split()

    if not args or (len(args) is not 2 and len(args) is not 4):
        client.send('To login type: <username> <password>\r\n' \
                    'To register type: register <username> <password> <password>')
        return

    if args[0] == 'register':
        register(client, args[1], args[2], args[3])
        return

    login(client, args[0], args[1])


def login(client, username, password):
    """
    Login to the server. Checks user exists, verifies provided password, and performs the necessary tasks to load
    the Entities.User and associated functions
    """
    dbUser = User.search(name=username)
    if not dbUser or not dbUser.verify_password(password):
        client.send('Invalid username or password!')
        return
    client.user = User.load(dbUser)
    client.user.hook_client(client)
    client.handler = handlers['default'](client.user)
    client.state = client.states.AUTHD
    client.user.p.send_text(f'Welcome, {client.user.name}')
    broadcast(f'{client.user.name} has entered the realm!')


def register(client, username, password1, password2):
    """
    Creates a new Database.models.User, then moves the client state to choose a race
    """
    if password1 != password2:
        client.send('Mismatching passwords!')
        return
    if not re.match('^[\w-]', username):
        client.send('Invalid username, please only use alphanumerics')
        return
    if len(username) < 3 or len(username) > 15:
        client.send('Invalid username length, must be between 3 - 15 characters')
        return
    if User.exists(name=username):
        client.send('That username is already taken, sorry!')
        return
    user = User.create(name=username, password=password1)
    client.user = User.load(user, dummy=True)
    client.state = client.states.RACE
    choose_race(client, -1)


def choose_race(client, msg):
    """
    Interface to choose a race during registration, once chosen moves client state to choose a class
    """
    races = {race.id:race for race in Race.all()}
    client.send('Please select a race:\r\n' +
                '\r\n'.join([f'[{race.id}] {race.name}\r\n' for race in races.values()]))
    try:
        msg = int(msg)
    except:
        return
    if msg not in races:
        return
    client.user.race = Race.load(races[msg])
    client.send(f'You have chosen {client.user.race.name}')
    client.state = client.states.CLASS
    choose_class(client, -1)


def choose_class(client, msg):
    """
    Interface to choose a class, once chosen the user is saved and the client state is set to unauthorised to allow login
    """
    classes = {class_.id:class_ for class_ in Class.all()}
    client.send('Please select a class:\r\n' +
                '\r\n'.join([f'[{class_.id}] {class_.name}\r\n' for class_ in classes.values()]))
    try:
        msg = int(msg)
    except:
        return
    if msg not in classes:
        return
    client.user.class_ = Class.load(classes[msg])

    client.send(f'You have chosen {client.user.class_.name}\r\n'
                f'You have successfully registered.\r\n'
                f'Please now login.')
    client.user.save()
    client.state = client.states.UNAUTH




