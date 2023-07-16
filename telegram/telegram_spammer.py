
import os
import requests
from time import sleep
from random import randint
import random
import threading
import asyncio

from telethon.sync import TelegramClient
from telethon import utils
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, MessageService, ChannelParticipantsAdmins
from telethon import events, functions, types
from telethon.errors.rpcerrorlist import PeerFloodError

from colorama import Fore, Back, Style
from colorama.ansi import clear_line, clear_screen

from .data import mensajes
from .data import messages

class TelegramSpammer:

    def __init__(self):
        self.clients = []
        self.groups = []
        self.members = []
        self.groupsById = {}
        self.activeClientIndex = None
        self.client = None # Active client
        self.forwarding = {}
        self.load_forwarding_file()
        self.chats_list = list( map(lambda id: int(id), self.forwarding.keys()) )
        self.stop_event = threading.Event()


    def start_clients(self, clients):
        for account in clients:
            print("Connecting...")
            print(account)

            class_path = os.path.dirname(os.path.abspath(__file__))
            sessions_path = os.path.join(class_path, "sessions")

            if not os.path.exists(sessions_path):
                os.makedirs(sessions_path)

            session_file = f'{sessions_path}/{account["user"]}.session'
            client = TelegramClient(session_file, account["api_id"], account["api_hash"], device_model=account["device_model"], system_version=account["system_version"], app_version=account["app_version"], system_lang_code=account["system_lang_code"], lang_code=account["lang_code"])
            try:
                client.connect()
                client.start()
                self.clients.append(client)
                print (Fore.GREEN + "Client connected." + Style.RESET_ALL)
            except Exception as e:
                print (Fore.RED + "Client NOT connected." + Style.RESET_ALL)
                # err = str(e)
            sleep(1)

        self.activeClientIndex = 0
        self.client = self.clients[self.activeClientIndex]
        print( str(len(self.clients)) +" users connected.")


    def show_active_client(self):
        me = self.client.get_entity('me')

        print( "Información del usuario activo:")
        print( Fore.BLUE + " ID: " + Fore.CYAN + str(me.id) )
        print( Fore.BLUE + " Name: " + Fore.CYAN + str(me.first_name) )
        print( Fore.BLUE + " Surname: " + Fore.CYAN + str(me.last_name) )
        print( Fore.BLUE + " User: " + Fore.CYAN + str(me.username) )
        print( Fore.BLUE + " Phone: " + Fore.CYAN + str(me.phone) )
        print(Style.RESET_ALL)
        #print(utils.get_display_name(me))
        # print(me)
        self.press_any_key()


    def update_profile_picture(self):
        file_name = "image.jpg"
        f = open(file_name,'wb')
        f.write(requests.get('https://thispersondoesnotexist.com/image', headers={'User-Agent': 'My User Agent 1.0'}).content)
        f.close()
        self.client(UploadProfilePhotoRequest(
            self.client.upload_file(file_name)
        ))
        os.remove(file_name)
        print("Telegram profile picture updated..")
        self.press_any_key()


    def change_active_client(self):
        print(" ------------------------------------------------------------------------------------------------------------------------")
        print(" | X\t|\tID\t|\tUser\t\t|\tName\t\t|\tSurname\t|\tPhone\t|")
        print(" ------------------------------------------------------------------------------------------------------------------------")

        for index, client in enumerate(self.clients):
            selected = False
            if client == self.client:
                selected = True
            c = client.get_entity('me')
            u = {
                "id": str(c.id),
                "username": self.prepare_string( str(c.username), 15),
                "name": self.prepare_string( str(c.first_name), 20),
                "last_name": self.prepare_string( str(c.last_name), 20),
                "phone": self.prepare_string( str(c.phone), 15)
            }
            if( selected ):
                print(" | " + Fore.GREEN + str(index) + Style.RESET_ALL + "\t| %s\t| %s\t| %s\t| %s\t| %s\t|" % ( u["id"], u["username"], u["name"], u["last_name"], u["phone"] ), end=Fore.GREEN+" (Cliente Activo)\n"+Style.RESET_ALL )
            else:
                print(" | " + Fore.GREEN + str(index) + Style.RESET_ALL + "\t| %s\t| %s\t| %s\t| %s\t| %s\t|" % ( u["id"], u["username"], u["name"], u["last_name"], u["phone"] ) )
        print(" ------------------------------------------------------------------------------------------------------------------------")

        id_client = input( "\n" + Style.RESET_ALL + "What client would you like to have ACTIVE?: " + Fore.MAGENTA)

        try:
            self.client = self.clients[ int(id_client) ]
            print( Fore.GREEN + "\nActive client updated" + Style.RESET_ALL )
        except:
            print( Fore.RED + "\n(!) An error has occurred. It is likely that the client you entered does not exist.")
        
        self.press_any_key()


    def add_client(self):
        user = input( Style.RESET_ALL + "\nUser: " + Fore.MAGENTA)
        api_id = input( Style.RESET_ALL + "API Id: " + Fore.MAGENTA)
        api_hash = input( Style.RESET_ALL + "API Hash: " + Fore.MAGENTA)
        device_model = input( Style.RESET_ALL + "Device Model: " + Fore.MAGENTA)
        system_version = input( Style.RESET_ALL + "System Version: " + Fore.MAGENTA)
        app_version = input( Style.RESET_ALL + "App Version: " + Fore.MAGENTA)
        system_lang_code = input( Style.RESET_ALL + "System Lang Code: " + Fore.MAGENTA)
        lang_code = input( Style.RESET_ALL + "Lang Code: " + Fore.MAGENTA)
        print(Style.RESET_ALL)
        try:
            class_path = os.path.dirname(os.path.abspath(__file__))
            sessions_path = os.path.join(class_path, "sessions")
            if not os.path.exists(sessions_path):
                os.makedirs(sessions_path)
            session_file = f'{sessions_path}/user.session'
            client = TelegramClient(user, api_id, api_hash)
            TelegramClient(session_file, api_id, api_hash, device_model=device_model, system_version=system_version, app_version=app_version, system_lang_code=system_lang_code, lang_code=lang_code)
            client.connect()
            client.start()
            self.clients.push(client)
            print(Fore.GREEN + "\nClient connected and added successfully. Remember to add it in the clients.py file!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "\n(!) Unable to add this client:\n" + str(e) + Style.RESET_ALL)

        self.press_any_key()


    def get_all_groups(self):
        print("\n\n")
        result = self.client.get_dialogs()
        cont = 0
        for channel in result:
            try:
                if channel.entity.admin_rights == None:
                    print(Fore.GREEN + str(cont) + Style.RESET_ALL + ": " + str(channel.entity.title) + " - " + Fore.MAGENTA + str(channel.entity.id) + Style.RESET_ALL )
                else:
                    print(Fore.GREEN + str(cont) + Style.RESET_ALL + ": " + str(channel.entity.title) + " - " + Fore.MAGENTA + str(channel.entity.id) + Style.RESET_ALL, end=Fore.YELLOW+" (ADMINISTRATOR)\n"+Style.RESET_ALL )
                self.groups.append(channel.entity)
                self.groupsById[str(channel.entity.id)] = channel.entity
                cont+=1 
            except:
                continue

        if input("\nDo you want to save the group list to a file? [y/N]: " + Fore.MAGENTA).upper() == "Y":
            self.save_groups()

        self.press_any_key()


    def save_groups(self):

        if not self.check_groups():
            print(Fore.RED + "(!) There are no groups stored in temporary memory. Try running option 5." + Style.RESET_ALL)
            return False

        print("\nSaving the groups to the file 'groups_list.csv' ...")
        
        try:
            class_path = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(class_path, "data")
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            file_name = f'{data_path}/groups_list.csv'

            if not os.path.isfile(file_name):
                print("File don't exist.")
                
            f = open(file_name,"w",encoding="utf-8")

            for group in self.groups:
                stringGroup = "{0}--.{1}".format(
                    group.id,
                    group.title,
                )
                f.write(stringGroup + "\n")

            f.close()
            print(Fore.GREEN + "Groups saved successfully.")
            
            return True

        except Exception as e:
            print(Fore.RED + "(!) An error has occurred:" + Style.RESET_ALL + str(e))
            return False


    def show_groups(self):
        print("\n\n")

        for index, group in enumerate(self.groups):
            if group.admin_rights == None:
                print(Fore.GREEN + str(index) + Style.RESET_ALL + ": " + str(group.title) + " - " + Fore.MAGENTA + str(group.id) + Style.RESET_ALL )
            else:
                print(Fore.GREEN + str(index) + Style.RESET_ALL + ": " + str(group.title) + " - " + Fore.MAGENTA + str(group.id) + Style.RESET_ALL, end=Fore.YELLOW+" (PERMISOS DE ADMINISTRADOR)\n"+Style.RESET_ALL )
        
    
    def show_group_info(self):
        if not self.check_groups():
            print(Fore.RED + "(!) There are no groups stored in temporary memory. Try running option 5." + Style.RESET_ALL)
            return False
        
        self.show_groups()
        group = int( input(Style.RESET_ALL + "\nSelect group: " + Fore.MAGENTA) )
        print(Fore.YELLOW)
        try:
            print("\n" + self.groups[group].stringify() + Style.RESET_ALL)
            self.press_any_key()
        except:
            print(Fore.RED + "\n(!) The selected group was not found.")


    def clone_group(self):
        # Strings to Replace ( "String to replace--|--String that replaces" )
        replaces = (
            "Info from source group--|--My new group info",
            "Replace this--|--For that",
            # Add more strings to replace here
        )
        # ---------------
        print(Fore.LIGHTBLACK_EX + "\n-------------------------------------------------------------")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 1-" + Fore.YELLOW + " Clone into a New Group                                " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 2-" + Fore.YELLOW + " Clone into an Existing Group                          " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 3-" + Fore.YELLOW + " Exit the menu for cloning groups                      " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------" + Style.RESET_ALL)
        opt = input("Select option: " + Fore.MAGENTA)

        if opt == "1": 
            # TODO: Create a group with the same name, etc., as the selected one, import users, and copy recent messages.
            print(Fore.BLUE + "\nThis function is not yet available! Crashing in 3, 2, 1...")
            sleep(1)
            result = self.client(functions.channels.CreateChannelRequest(
                title='Testing',
                about='Testing',
                broadcast=False,
                megagroup=True,
                for_import=True,
                geo_point=types.InputGeoPoint(
                    lat=7.13,
                    long=7.13,
                    accuracy_radius=42
                ),
                address='Testing'
            ))
            print(result.stringify())
            sleep(1)
            self.clone_group()

        elif opt == "2":
            self.check_groups()
            group1_index = -1
            while group1_index == -1:
                group1_index = int( input(Style.RESET_ALL + "\nWhat Group do you want to CLONE? (-1 to show groups): " + Fore.MAGENTA) )
                if group1_index == -1:
                    self.show_groups()

            group2_index = -1
            while group2_index == -1:
                group2_index = int( input(Style.RESET_ALL + "\nWhat Group do you want to use for cloning? (-1 to show groups): " + Fore.MAGENTA) )
                if group2_index == -1:
                    self.show_groups()

            #  Modify the data of group2 with the same name, etc., as group1, import X users at intervals of Y time, and copy the last Z messages.

            if input( Style.RESET_ALL + "\nDo you want to copy the TITLE of the Group? [y/N]: " + Fore.MAGENTA).upper() == "Y":
                print(Fore.BLUE + "\nUpdating group title..." + Style.RESET_ALL)
                try:
                    self.client(functions.channels.EditTitleRequest(
                        channel=self.groups[group2_index],
                        title=self.groups[group1_index].title
                    ))
                    print(Fore.GREEN + "\nTitle changed to " + self.groups[group1_index].title + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + "\nUnable to update the title. Error: " + str(e) + Style.RESET_ALL)
            
            self.press_any_key()

            if input( Style.RESET_ALL + "\nDo you want to copy the PHOTO of the Group? [y/N]: " + Fore.MAGENTA).upper() == "Y":
                # Get the photos of a channel
                photos = self.client.get_profile_photos(self.groups[group1_index])
                # Download the oldest photo
                photo = self.client.download_media(photos[-1])

                print(Fore.BLUE + "\nUpdating group picture..." + Style.RESET_ALL)
                try:
                    self.client(functions.channels.EditPhotoRequest(
                        channel=self.groups[group2_index],
                        photo=self.client.upload_file(photo)
                    ))
                    print(Fore.GREEN + "\nGroup photo updated successfully." + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + "\nUnable to update the group photo. Error: " + str(e) + Style.RESET_ALL)

            self.press_any_key()
            
            # Copy messages from source group
            num_msg_to_import = int( input(Style.RESET_ALL + "\nHow many messages do you want to import from the original group?: " + Fore.MAGENTA) )
            
            print(Fore.BLUE + "\nImporting messages..." + Style.RESET_ALL)

            msgs = self.client.get_messages(int(self.groups[group1_index].id), limit=num_msg_to_import)
            for msg in reversed(msgs):
                text = str(msg.text)
                for r in replaces:
                    tmp = r.split("--|--")
                    text = text.replace(tmp[0],tmp[1])
                if type(msg) != MessageService:
                    if hasattr(msg, 'media') and msg.media != None:
                        photo = self.client.download_media(msg.media)
                        if photo != None:
                            self.client.send_file(
                                int(self.groups[group2_index].id),
                                photo,
                                caption=text
                            )
                            os.remove(photo)
                    else:
                        self.client.send_message(int(self.groups[group2_index].id), text)

            print(Fore.GREEN + "\nMessages imported successfully." + Style.RESET_ALL)

            # Import users
            num_users_to_import = int( input(Style.RESET_ALL + "\nHow many users do you want to import? (-1 for all): " + Fore.MAGENTA) )
            min_seconds_delay =  int( int( input(Style.RESET_ALL + "\nMinimum time (sec.) between users added by the same client (Recommended 180): " + Fore.MAGENTA) ) / len(self.clients) )
            max_seconds_delay =  int( int( input(Style.RESET_ALL + "\nMaximum time (sec.) between users added by the same client (Recommended 300): " + Fore.MAGENTA) ) / len(self.clients) )
            print(Fore.BLUE + "\nImporting users..." + Style.RESET_ALL)

            try:
                members = self.client.get_participants(int(self.groups[group1_index].id), aggressive=True)
                sleep(1)
                # REMOVE ADMINS
                try:
                    admins = self.client.get_participants(int(self.groups[group1_index].id), filter=ChannelParticipantsAdmins, aggressive=True)
                    sleep(1)
                    admins_set = set(admins)
                    members = [member for member in members if member not in admins_set]
                except:
                    print("Unable to extract Admins.")
 
                cont = 0
                for user in members:
                    if user.bot == True or user.fake == True or user.scam == True:
                        continue
                    if cont == num_users_to_import:
                        break
                    if self.invite_user_to_group(user, group2_index):
                        cont+=1

                    # Pause
                    print (Fore.BLUE + "    * Sleeping between %s and %s seconds." % ( str(min_seconds_delay), str(max_seconds_delay) ))
                    sleep(randint(min_seconds_delay,max_seconds_delay))


                    # Change client
                    n = self.clients.index(self.client)
                    if n+1 == len(self.clients):
                        n = 0
                    else:
                        n += 1
                    self.client = self.clients[ n ]

                print(Style.RESET_ALL + "\nImported " + str( cont ) + " members.")
                
            except Exception as e:
                print( Fore.RED + "\n(!) Error: "+ str(e))

            self.press_any_key()
            self.clone_group()

        elif opt == "3":
            return

        else:
            print(Fore.RED + "\nWrong option!" + Style.RESET_ALL)
            sleep(1)
            self.clone_group()
    

    def invite_user_to_group(self, user, group_index, send_pm = False, lang = "EN"):
        if user.mutual_contact == False:
            try:
                if user.first_name: 
                    first_name = str(user.first_name)
                else: 
                    first_name = str(user.username)
                if user.last_name: 
                    last_name = str(user.first_name)
                else: 
                    last_name = str(user.username)

                if user.contact == True:
                    self.client(functions.contacts.DeleteContactsRequest(
                        user,
                    ))

                #sleep(randint(1,5))

                self.client(functions.contacts.AddContactRequest(
                    user,
                    first_name=first_name,
                    last_name=last_name,
                    phone=str(user.phone),
                    add_phone_privacy_exception=True
                ))
                print(Fore.GREEN + "The following contact has been added successfully:" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + str(e))
                print(Fore.RED + "Unable to add the following contact:" + Style.RESET_ALL)
        
        print(user)
        #print(group)

        print("\nTrying to add the user to our group...")

        group = self.groups[group_index]

        # ImportChatInviteRequest, AddChatUserRequest
        try:
            self.client( InviteToChannelRequest( group, [user] ) )
            print (Fore.GREEN + "%s added to group." % str(user.id) + Style.RESET_ALL)

            # Deleting message "User Join to group"
            msg = self.client.get_messages(group, limit=1)                        
            for m in msg:
                if type(m) == MessageService:
                    self.client.delete_messages(group, m.id)
            r = True

        except PeerFloodError as flood:
            print (Fore.RED + "¡FLOOD! Unable to add %s." % (user.id))
            print (Fore.RED + str(flood))
            #sleep(randint(1000,5000))
            sleep(randint(1,5))
            return False
        except Exception as e:
            print (Fore.RED + "Unable to add %s." % str(user.id) )
            print (Fore.RED + str(e))
            sleep(randint(1,5))
            return False
        
        if send_pm == True:
            print( Fore.BLUE + "\nSending random private message to the user..." )
            self.send_msg(user, lang)
        return True


    def all_clients_join_group(self, group):
        for client in self.clients:
            try:
                client(JoinChannelRequest(channel=group.username))
            except Exception as e:
                print( Fore.RED + "\n(!) Error: "+ str(e))


    def all_clients_to_admin_group(self):
        if not self.check_groups():
            print(Fore.RED + "(!) There are no groups stored in temporary memory. Try running option 5." + Style.RESET_ALL)
            return False
        
        error = True

        while(error):
            try:
                group_index = int( input(Style.RESET_ALL + "\n¿A qué Grupo quieres invitar al resto de Clientes? (-1 para mostrar grupos): " + Fore.MAGENTA) )
                while group_index == -1:
                    self.showGroups(False)
                    group_index = int( input(Style.RESET_ALL + "\n¿A qué Grupo quieres invitar al resto de Clientes? (-1 para mostrar grupos): " + Fore.MAGENTA) )
                error = False
            except:
                print(Fore.RED + "(!) Ha ocurrido un ERROR, es probable que el grupo seleccionado no exista." + Style.RESET_ALL)
                error = True
                sleep(1)

        group = self.groups[group_index]

        # Todos los clientes se unen al grupo
        for client in self.clients:
            if self.client != client:
                try:
                    client(JoinChannelRequest(channel=group.username))
                    print(Fore.BLUE + "\nClient joined to group. Upgrading to admin... ")
                    userEntity = client.get_entity('me')
                    # if self.inviteUserToGroup(userEntity, group):
                    self.client.edit_admin(group.username, userEntity, is_admin=True)
                except Exception as e:
                    print( Fore.RED + "\n(!) Error: "+ str(e))

        self.press_any_key()


    def get_members_from_group(self):
        if not self.check_groups():
            print(Fore.RED + "(!) There are no groups stored in temporary memory. Try running option 5." + Style.RESET_ALL)
            return False
        
        error = True

        while(error):
            try:
                group_index = int( input(Style.RESET_ALL + "\nFrom which Group do you want to EXTRACT the users? (-1 to show groups): " + Fore.MAGENTA) )
                while group_index == -1:
                    self.show_groups()
                    group_index = int( input(Style.RESET_ALL + "\nFrom which Group do you want to EXTRACT the users? (-1 to show groups): " + Fore.MAGENTA) )

                if input(Style.RESET_ALL + "\nDo you want to extract the Administrators as well? [y/N]: " + Fore.MAGENTA).upper() == "Y":
                    self.members = self.client.get_participants(self.groups[group_index], aggressive=True)
                else:
                    #TODO
                    self.members = self.client.get_participants(self.groups[group_index], aggressive=True)
                error = False
            except:
                print(Fore.RED + "(!) An ERROR occurred while extracting the group members " + group_index + Style.RESET_ALL)
                error = True
                sleep(1)
        try:
            self.group_selected = self.groups[group_index]
            print(Style.RESET_ALL + "\nA total of " + str( len(self.members) ) + " members have been extracted.")
            self.press_any_key()
        except Exception as e:
            print( Fore.RED + "\n(!) Error: "+ str(e))


    def get_members_from_file(self):
        file_name = "members.txt"
        self.members = []
        class_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(class_path, "data")
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        file_path = f'{data_path}/{file_name}'
        
        if os.path.isfile(file_path):
            f = open(file_name,"r",encoding="utf-8")
            for line in f:
                self.members.append(line.rstrip())
            f.close()

    def show_members(self):
        for user in self.members:
            print(user)
            input()
        self.press_any_key()


    def import_members_to_group(self):
        if not self.check_members():
            print(Fore.RED + "(!) There are no members stored in temporary memory. Try running option 12." + Style.RESET_ALL)
            return False
        error = True

        while(error):
            try:
                group_index = int( input(Style.RESET_ALL + "\nTo which group do you want to IMPORT the extracted members? (-1 to show groups): " + Fore.MAGENTA) )
                while group_index == -1:
                    self.show_groups(False)
                    group_index = int( input(Style.RESET_ALL + "\nTo which group do you want to IMPORT the extracted members? (-1 to show groups): " + Fore.MAGENTA) )
                selected_group = self.groups[group_index]
                error = False
            except:
                print(Fore.RED + "(!) An ERROR occurred while extracting the members from the group " + group_index + Style.RESET_ALL)
                error = True
                sleep(1)

        # Importar usuarios
        num_users_to_import = int( input(Style.RESET_ALL + "\nHow many users do you want to import? (-1 for all): " + Fore.MAGENTA) )
        min_seconds_delay =  int( input(Style.RESET_ALL + "\nMinimum time (sec.) between users added by the same client (Recommended 180): " + Fore.MAGENTA) ) / len(self.clients)
        max_seconds_delay =  int( input(Style.RESET_ALL + "\nMaximum time (sec.) between users added by the same client (Recommended 300): " + Fore.MAGENTA) ) / len(self.clients)
        print(Fore.BLUE + "\nImporting users..." + Style.RESET_ALL)

        cont = 0
        for user in self.members:
            if self.invite_user_to_group(user, selected_group, True):
                cont+=1
                # Change client
                n = self.clients.index(self.client)
                if n+1 == len(self.clients):
                    n = 0
                else:
                    n += 1
                self.client = self.clients[ n ]
            print (Fore.BLUE + "    * Sleeping between %s and %s seconds." % ( str(min_seconds_delay), str(max_seconds_delay) ))
            sleep(randint(min_seconds_delay,max_seconds_delay))
            if cont == num_users_to_import:
                break

        print(Style.RESET_ALL + "\nA total of " + str( cont ) + " members has been imported.")
        self.press_any_key()


    def send_msg(self, user, lang="ES"):
        if lang == "ES":
            msg = random.choice(mensajes.mensajes)
        else:
            msg = random.choice(messages.mensajes)

        if user.first_name: 
            msg = msg.replace("{{name}}", user.first_name)
        else: 
            msg = msg.replace("{{name}}", user.username)

        msg = msg.replace("{{group}}", self.group_selected.title)

        try: 
            print (Fore.RED + "Sending message to: ", user.username + Style.RESET_ALL)
            # if self.client.send_message(entity=self.client.get_entity(user.username),message=msg):
            if self.client.send_message(user, msg):
                print(Fore.GREEN + "\nMessage sent successfully." + Style.RESET_ALL)
                return True
            print(Fore.RED + "\nUnable to send message." + Style.RESET_ALL)
            return False

        except Exception as e: 
            print (Fore.YELLOW + "Unable to send a message to %s. Error: %s" % (user.id, e))


    def spam_members(self):
        
        if not self.check_members():
            print(Fore.RED + "(!) There are no members stored in temporary memory. Try running option 12." + Style.RESET_ALL)
            return False
        
        min_seconds_delay = 10
        max_seconds_delay = 100

        lang = input("\nIn what language do you want to send the messages? [es/EN]: " + Fore.MAGENTA).upper()

        if lang == "ES":
            print( Fore.BLUE + "Preparando los mensajes en ESPAÑOL..." + Style.RESET_ALL)
        else:
            print( Fore.BLUE + "Preparing ENGLISH messages..." + Style.RESET_ALL)
            lang == "EN"

        cont = 0
        for user in self.members:
            if self.send_msg(user, lang):
                cont += 1
            sleep(randint(min_seconds_delay,max_seconds_delay))

        print( Fore.BLUE + "A total of " + cont + " messages have been sent successfully." + Style.RESET_ALL)


    def redirect_msg(self):
        print("\n\nWith this option, you can copy messages from another group, and the bot will write them in the group of your choice.\nThis function requires being in 'listening mode' (option 18).")
        print(Fore.LIGHTBLACK_EX + "\n\n-------------------------------------------------------------")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 1-" + Fore.YELLOW + " Add Redirection                                       " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 2-" + Fore.YELLOW + " Remove Redirection                                    " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 3-" + Fore.YELLOW + " Show all Redirections                                 " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 4-" + Fore.YELLOW + " Update redirections file                              " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 5-" + Fore.YELLOW + " Go Back                                               " + Fore.LIGHTBLACK_EX + "|")
        print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------" + Style.RESET_ALL)
        opt = input("Select option: " + Fore.MAGENTA)

        if opt == "1":
            if not self.check_groups():
                print(Fore.RED + "(!) There are no groups stored in temporary memory. Try running option 5." + Style.RESET_ALL)
            else:
                group_A = int( input(Style.RESET_ALL + "\nSource Group (-1 to show groups): " + Fore.MAGENTA) )
                while group_A == -1:
                    self.showGroups(False)
                    group_A = int( input(Style.RESET_ALL + "\nSource Group (-1 to show groups): " + Fore.MAGENTA) )

                group_B = int( input(Style.RESET_ALL + "\nTarget group - where you want to forward the messages (-1 to show groups): " + Fore.MAGENTA) )
                while group_B == -1:
                    self.showGroups(False)
                    group_B = int( input(Style.RESET_ALL + "\nTarget group - where you want to forward the messages (-1 to show groups): " + Fore.MAGENTA) )

                group_A = self.groups[group_A]
                group_B = self.groups[group_B]

                if str(group_A.id) in self.forwarding:
                    if group_B.id in self.forwarding[str(group_A.id)]['groups_to_send']:
                        print(Fore.BLUE + "\nThe group '" + group_A.title + "' is already forwarding to '" + group_B.title + "'.")
                    else:
                        self.forwarding[str(group_A.id)]['groups_to_send'].append(str(group_B.id))
                        print(Fore.BLUE + "\nRedirection from '" + group_A.title + "' to '" + group_B.title + "' ADDED successfully.")
                else:
                    # Comprobamos si existe el atributo 'access_hash'. Si no existe será un chat, si existe será un megagrupo
                    if hasattr(group_A, 'access_hash'):
                        access_hash = group_A.access_hash
                    else:
                        access_hash = ""

                    self.forwarding[str(group_A.id)] = {
                        "group_id": group_A.id,
                        "group_name": group_A.title,
                        "group_access_hash": access_hash,
                        "groups_to_send": [ str(group_B.id) ]
                    }

                # Update File
                self.update_forwarding_file()
                # Back to menu
                sleep(1)
                self.redirect_msg()
            # -- END OPTION 1

        elif opt == "2": # Eliminar Reenvío
            if not self.check_redirects():
                print(Fore.RED + "(!) There are no redirects available." + Style.RESET_ALL)
                self.redirect_msg()

            print(Fore.BLUE + "\nTO-DO. (For now, you can delete redirections directly from the forwarding.csv file.)" + Style.RESET_ALL)
            #remove_redirection_from_file
            #self.updateForwardingFile()
            sleep(1)
            self.redirect_msg()
            # -- END OPTION 2

        elif opt == "3": # Show all redirections
            if not self.check_redirects():
                print(Fore.RED + "(!) There are no redirects available." + Style.RESET_ALL)
                self.redirect_msg()

            for redirect in self.forwarding.values():
                print(Style.RESET_ALL + "\n(" + Fore.GREEN + str(redirect['group_id']) + Style.RESET_ALL + ") " + Fore.BLUE + str(redirect['group_name']) + Style.RESET_ALL )
                for group_id in redirect['groups_to_send']:
                    print("  - " + str(group_id))

            self.press_any_key()
            self.redirect_msg()
            # -- END OPTION 3

        elif opt == "4": # Exit
            self.update_forwarding_file()

        elif opt == "5": # Exit
            return
        
        else:
            print(Fore.RED + "\nWrong option!" + Style.RESET_ALL)
            sleep(1)
            self.redirect_msg()
            

    def update_forwarding_file(self):
        print(Fore.BLUE + "\nSaving groups at 'forwarding.csv' ...")
        try:
            file_name = "forwarding.csv"
            class_path = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(class_path, "data")
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            file_path = f'{data_path}/{file_name}'

            f = open(file_path,"w",encoding="utf-8")

            for forward in self.forwarding:
                groups = ";;".join(self.forwarding[forward]['groups_to_send'])
                stringForward = "{0}-|||-{1}-|||-{2}-|||-{3}".format(
                    self.forwarding[forward]['group_name'],
                    self.forwarding[forward]['group_id'],
                    self.forwarding[forward]['group_access_hash'],
                    groups
                )
                f.write(stringForward + "\n")
            f.close()
            print(Fore.BLUE + "\nFile updated successfully." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "\n(!) Unable to save redirections at file.\n" + str(e) + Style.RESET_ALL)


    def load_forwarding_file(self):
        file_name = "forwarding.csv"
        class_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(class_path, "data")
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        file_path = f'{data_path}/{file_name}'
        try:
            f = open(file_path,"r",encoding="utf-8")
            for line in f:
                columns = line.split("-|||-")
                
                group_name = columns[0] # Source group name
                group_id = columns[1] # Source group ID
                group_access_hash = columns[2] # Source group Access_Hash
                groups_to_send = columns[3].rstrip("\n").split(";;") # Array with IDs of target groups
                self.forwarding[group_id] = {
                    'group_id': group_id,
                    'group_name': group_name,
                    'group_access_hash': group_access_hash,
                    'groups_to_send': groups_to_send,
                }
                #self.forwarding[group_id] = InputPeerChannel(int(group_id),int(group_access_hash))
            f.close()
        except Exception as e:
            if not os.path.isfile(file_path):
                print(Fore.BLUE + "\nFile '" + file_name + "' does not exist. It have been created." + Style.RESET_ALL)
                f = open(file_path,"w",encoding="utf-8")
                f.close()

    # FORWARD MESSAGES FROM ONE GROUP TO ANOTHER (Only works when listening to events)
    async def new_msg_received(self, event):
        chat_id = int(event.chat_id)
        if(chat_id < 0): chat_id*=-1
        texto=str(event.text)

        for r in self.replaces:
            tmp = r.split("--|--")
            texto = texto.replace(tmp[0],tmp[1])
        
        try:
            if event.media != None:
                photo = self.client.download_media(event.media)
                if photo != None:
                    await self.client.send_file(
                        chat_id,
                        photo,
                        caption=texto[0:200]
                    )
                    os.remove(photo)
                else:
                    await self.client.send_message( chat_id, texto)
        except:
            pass


    # LISTENING MODE
    def listen_events(self):
        #TODO
        print(Fore.BLUE + "\n\n(TO-DO) Listening events...\n" + Style.RESET_ALL)
        sleep(2)
        '''
        self.chats_list = list(map(lambda id: int(id), self.forwarding.keys()))

        self.stop_event = threading.Event()

        @self.client.on(events.NewMessage(chats=self.chats_list))
        async def newMessage(event):
            await self.new_msg_received(event)

        async def run_client():
            await self.client.run_until_disconnected()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(run_client())
        finally:
            loop.close()

        self.stop_event.wait()
        '''

    def start_listening_events(self):
        telegram_thread = threading.Thread(target=self.listen_events)
        telegram_thread.start()


    def finish(self):
        self.stop_event.set()
        '''
        for index, client in enumerate(self.clients):
            client.disconnect()

        active_threads = threading.enumerate()
        for thread in active_threads:
            if thread != threading.current_thread():
                thread.join()
        '''

    def prepare_string(self, string, num_chars):
        if len(string) > num_chars:
            return string[0:num_chars]
        elif len(string) < num_chars:
            while len(string) < num_chars:
                string += " "
        return string
    

    def check_groups(self):
        if len(self.groups) < 1:
            return False
        return True
    

    def check_members(self):
        if len(self.members) < 1:
            return False
        return True

    
    def check_redirects(self):
        if len(self.forwarding) < 1:
            return True
        return False


    def press_any_key(self):
        input( Fore.BLUE + "\nPress any key to continue..." + Style.RESET_ALL )
        