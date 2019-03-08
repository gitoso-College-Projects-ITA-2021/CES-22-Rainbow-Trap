#!/usr/bin/python
# -*- coding: utf-8 -*-


# Import Python libraries
import os
import sys
import getopt
import pygame
from pygame.locals import *

# Import local Classes
from background import Background
from game import Game

# Import resources
images_dir = os.path.join("..", "imagens")


def usage():
    """
    Imprime informações de uso deste programa.
    """
    prog = sys.argv[0]
    print("Usage:")
    print("\t%s [-f|--fullscreen] [-r <XxY>|--resolution=<XxY>]" % prog)
    print()
# usage()


def parse_opts(argv):
    """
    Pega as informações da linha de comando e retorna 
    """
    # Analise a linha de commando usando 'getopt'
    try:
        opts, args = getopt.gnu_getopt(argv[1:], "hfr:",
                                       ["help", "fullscreen", "resolution="])
    except getopt.GetoptError:
        # imprime informacao e sai
        usage()
        sys.exit(2)

    options = {
        "fullscreen": False,
        "resolution": (640, 480),
        }

    for o, a in opts:
        if o in ("-f", "--fullscreen"):
            options["fullscreen"] = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-r", "--resolution"):
            a = a.lower()
            r = a.split("x")
            if len(r) == 2:
                options["resolution"] = r
                continue

            r = a.split(",")
            if len(r) == 2:
                options["resolution"] = r
                continue

            r = a.split(":")
            if len(r) == 2:
                options["resolution"] = r
                continue
    # for o, a in opts
    r = options["resolution"]
    options["resolution"] = [int(r[0]), int(r[1])]
    return options
# parse_opts()


def main(argv):
    # primeiro vamos verificar que estamos no diretorio certo para conseguir
    # encontrar as imagens e outros recursos, e inicializar o pygame com as
    # opcoes passadas pela linha de comando
    fullpath = os.path.abspath(argv[0])
    dir = os.path.dirname(fullpath)
    os.chdir(dir)

    options = parse_opts(argv)
    game = Game(options["resolution"], options["fullscreen"])
    game.loop()
# main()


# este comando fala para o python chamar o main se estao executando o script
if __name__ == '__main__':
    main(sys.argv)
