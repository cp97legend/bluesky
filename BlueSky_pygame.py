#!/usr/bin/env python
""" Pygame BlueSky start script """
import pygame as pg
import bluesky as bs
from bluesky.ui.pygame import splash


def main():
    """ Start the mainloop (and possible other threads) """
    splash.show()
    bs.init(gui='pygame')
    # bs.sim.op()
    bs.scr.init()

    # Main loop for BlueSky
    while not bs.sim.state == bs.END:
        bs.sim.update()   # Update sim
        bs.scr.update()   # GUI update

    bs.sim.quit()
    pg.quit()

    print('BlueSky normal end.')


if __name__ == '__main__':
    print("   *****   BlueSky 空中交通模拟器 *****")
    print("基于 GNU General Public License v3 发布")
    # Run mainloop if BlueSky_pygame is called directly
    main()
