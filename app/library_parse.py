#!/usr/bin/env python

# import re


def parse_discipline_list(discipline_input):
    dis_list = []
    for i in discipline_input:
        if i == "abo":
            dis_list.append('Abombwe')
        elif i == "ani":
            dis_list.append('Animalism')
        elif i == "aus":
            dis_list.append('Auspex')
        elif i == "cel":
            dis_list.append('Celerity')
        elif i == "chi":
            dis_list.append('Chimerstry')
        elif i == "dai":
            dis_list.append('Daimoinon')
        elif i == "dom":
            dis_list.append('Dominate')
        elif i == "for":
            dis_list.append('Fortitude')
        elif i == "dem":
            dis_list.append('Dementation')
        elif i == "mel":
            dis_list.append('Melpominee')
        elif i == "myt":
            dis_list.append('Mytherceria')
        elif i == "nec":
            dis_list.append('Necromancy')
        elif i == "obe":
            dis_list.append('Obeah')
        elif i == "obf":
            dis_list.append('Obfuscate')
        elif i == "obt":
            dis_list.append('Obtenebration')
        elif i == "pot":
            dis_list.append('Potence')
        elif i == "pre":
            dis_list.append('Presence')
        elif i == "PRE":
            dis_list.append('Presence')
        elif i == "pro":
            dis_list.append('Protean')
        elif i == "ser":
            dis_list.append('Serpentis')
        elif i == "san":
            dis_list.append('Sanguinus')
        elif i == "spi":
            dis_list.append('Spiritus')
        elif i == "tem":
            dis_list.append('Temporis')
        elif i == "thn":
            dis_list.append('Thanatosis')
        elif i == "tha":
            dis_list.append('Thaumaturgy')
        elif i == "qui":
            dis_list.append('Quietus')
        elif i == "val":
            dis_list.append('Valeren')
        elif i == "vic":
            dis_list.append('Vicissitude')
        elif i == "vis":
            dis_list.append('Visceratika')
    return dis_list


# def parse_capacity_list(capacity_input):
#     capacity_list = []
#     if "+" in capacity_input:
#         capacity = int(capacity_input[0])
#         capacity_list = list(range(capacity), 12)
#     elif "-" in capacity_input:
#         capacity = capacity_input.split("-")
#         capacity_list = list(range(1, int(capacity[0]) + 1))
#     else:
#         capacity_list.append(int(capacity_input))
#     return capacity_list

# def parse_sect_list(sect_input):
#     sect_list = []
#     for i in sect_input:
#         if i == "c":
#             sect_list.append("Camarilla")
#         if i == "s":
#             sect_list.append("Sabbat")
#         if i == "i":
#             sect_list.append("Independent")
#         if i == "a":
#             sect_list.append("Anarch")
#         if i == "l":
#             sect_list.append("Laibon")

#     return sect_list

# def parse_title_list(title_worth_input):

#     camarilla = {
#         "primogen": 1,
#         "prince": 2,
#         "justicar": 3,
#         "imperator": 3,
#         "inner circle": 4
#     }

#     sabbat = {
#         "bishop": 1,
#         "archbishop": 2,
#         "priscus": 3,
#         "cardinal": 3,
#         "regent": 4
#     }

#     independent = {
#         "1 vote": 1,
#         "2 votes": 2,
#         "3 votes": 3,
#     }

#     laibon = {
#         "magaji": 2,
#         "kholo": 2,
#     }

#     anarch = {
#         "baron": 2,
#     }

#     sects = [camarilla, sabbat, independent, laibon, anarch]

#     title_list = []
#     title_worth = int(title_worth_input[0])

#     if len(title_worth_input) == 1:
#         for i in sects:
#             for k, v in i.items():
#                 if v >= title_worth:
#                     title_list.append(k)
#     elif title_worth_input[1] == "c":
#         for k, v in camarilla.items():
#             if v >= title_worth:
#                 title_list.append(k)
#     elif title_worth_input[1] == "s":
#         for k, v in sabbat.items():
#             if v >= title_worth:
#                 title_list.append(k)
#     elif title_worth_input[1] == "a":
#         for k, v in anarch.items():
#             if v >= title_worth:
#                 title_list.append(k)
#     elif title_worth_input[1] == "i":
#         for k, v in independent.items():
#             if v >= title_worth:
#                 title_list.append(k)
#     elif title_worth_input[1] == "l":
#         for k, v in laibon.items():
#             if v >= title_worth:
#                 title_list.append(k)

#     return title_list


def parse_clan_list(clan_input):
    clan_list = []
    if clan_input == "abo":
        clan_list.append("Abomination")
    elif clan_input == "ahr":
        clan_list.append("Ahrimane")
    elif clan_input == "aku":
        clan_list.append("Akunanse")
    elif clan_input == "ass":
        clan_list.append("Assamite")
    elif clan_input == "baa":
        clan_list.append("Baali")
    elif clan_input == "blo":
        clan_list.append("Blood Brothers")
    elif clan_input == "bru":
        clan_list.append("Brujah")
    elif clan_input == "abru":
        clan_list.append("Brujah Antitribu")
    elif clan_input == "cai":
        clan_list.append("Caitiff")
    elif clan_input == "dau":
        clan_list.append("Daughter of Cacophony")
    elif clan_input == "fol":
        clan_list.append("Follower of Set")
    elif clan_input == "gan":
        clan_list.append("Gangrel")
    elif clan_input == "agan":
        clan_list.append("Gangrel Antitribu")
    elif clan_input == "gar":
        clan_list.append("Gargoyle")
    elif clan_input == "gio":
        clan_list.append("Giovanni")
    elif clan_input == "gur":
        clan_list.append("Guruhi")
    elif clan_input == "har":
        clan_list.append("Harbringer of Skulls")
    elif clan_input == "imb":
        clan_list.append("Imbue")
    elif clan_input == "ish":
        clan_list.append("Ishtarri")
    elif clan_input == "kia":
        clan_list.append("Kiasyd")
    elif clan_input == "las":
        clan_list.append("Lasombra")
    elif clan_input == "mal":
        clan_list.append("Malkavian")
    elif clan_input == "amal":
        clan_list.append("Malkavian Antitribu")
    elif clan_input == "nag":
        clan_list.append("Nagaraja")
    elif clan_input == "nos":
        clan_list.append("Nosferatu")
    elif clan_input == "anos":
        clan_list.append("Nosferatu Antitribu")
    elif clan_input == "ose":
        clan_list.append("Osebo")
    elif clan_input == "pan":
        clan_list.append("Pander")
    elif clan_input == "rav":
        clan_list.append("Ravnos")
    elif clan_input == "sal":
        clan_list.append("Salubri")
    elif clan_input == "asal":
        clan_list.append("Salubri Antitribu")
    elif clan_input == "sam":
        clan_list.append("Samedi")
    elif clan_input == "tor":
        clan_list.append("Toreador")
    elif clan_input == "ator":
        clan_list.append("Toreador Antitribu")
    elif clan_input == "tre":
        clan_list.append("Tremere")
    elif clan_input == "atre":
        clan_list.append("Tremere Antitribu")
    elif clan_input == "tru":
        clan_list.append("True Brujah")
    elif clan_input == "tzi":
        clan_list.append("Tzimisce")
    elif clan_input == "ven":
        clan_list.append("Ventrue")
    elif clan_input == "aven":
        clan_list.append("Ventrue Antitribu")

    return clan_list
