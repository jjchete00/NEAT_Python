#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:50:40 2023

@author: Juan Jose Vidal
"""

import pygame
import neat
import os
from math import dist


pygame.init() 


width, height = 1100, 700

car = pygame.image.load("imagenes/coin.png")
cookie = pygame.image.load("imagenes/cookie.png")
background = pygame.image.load("imagenes/background2.jpg")
plat = pygame.image.load("imagenes/platform.png")
enemigo = pygame.image.load("imagenes/enemigo.png")

st_im = pygame.image.load("imagenes/standing.png")
lw_im = pygame.image.load("imagenes/left_walk.png")
rw_im = pygame.image.load("imagenes/right_walk.png")
expl = pygame.image.load("imagenes/explosion.png")

window = pygame.display.set_mode((width,height))

pygame.display.set_caption("NEAT algorithm test")


class Player():
    
    x_pos = width*0.1
    y_pos = 500
    v_x = 10 
    v_y = 10
    JUMP_VEL = 9
    
    def __init__(self):
        
        self.image = st_im 
        self.im_left = lw_im
        self.im_right = rw_im

        self.ryan_still = True
        self.ryan_jump=False 
        self.ryan_left = False
        self.ryan_right = False
        
        self.jump_vel = self.JUMP_VEL 
        
        self.rect = pygame.Rect(self.x_pos,self.y_pos,self.image.get_width(),self.image.get_height())
        self.ryan_rect = self.image.get_rect()
        self.ryan_rect.x = self.x_pos
        self.ryan_rect.y = self.y_pos
        
        
    def update(self,window):
        
        if self.ryan_still:
            self.still()

        if self.ryan_left: 
            self.left()
            
        if self.ryan_right:
            self.right()
        
        if self.ryan_jump:
            self.jump()


    def jump(self):
        if self.ryan_jump:
            self.ryan_rect.y -= self.jump_vel*4
            self.jump_vel -= 1
    
        if self.jump_vel < - self.JUMP_VEL:
            self.ryan_jump = False
            self.jump_vel = self.JUMP_VEL
    
    def left(self):

        if self.ryan_rect.x > 0:
            self.ryan_rect.x -= self.v_x
            self.image = lw_im
            self.ryan_left = False

    def right(self):
        if self.ryan_rect.topright[0] < width:
            self.ryan_rect.x += self.v_x
            self.image = rw_im
            self.ryan_right = False

    def still(self):
        self.image = st_im

    def draw(self,window):
        window.blit(self.image, (self.ryan_rect.x,self.ryan_rect.y))  

class Wallpaper():
    x_plat = 0
    y_plat = 550
    
    def __init__(self):
        self.im_bg = background

    def draw(self,window):
        window.blit(self.im_bg, (0,0))

class Plataforma():
    
    x_plat = 250
    y_plat = 400
    
    def __init__(self):

        self.im_plat = plat
        self.plat_rect = pygame.Rect(self.x_plat,self.y_plat,self.im_plat.get_width() ,5) 

    def draw(self,window):
        window.blit(self.im_plat, (self.x_plat,self.y_plat))
  
class Obstaculo():
    
    x_obs = 700
    y_obs = 500
    grosor = 50
    
    def __init__(self):
        self.im_ene = enemigo
        self.rect_obs = pygame.Rect(self.x_obs,self.y_obs,self.grosor,self.grosor) 
        
    def draw(self,window):
        window.blit(self.im_ene,(self.x_obs,self.y_obs))

class Cookies():
    
    c1_x,c1_y = 610,500
    c2_x,c2_y = 700,400
    grosor = 50

    def __init__(self):
        #self.cookie1 = cookie
        self.cookie2 = cookie


        #self.rect_cookie1 = pygame.Rect(self.c1_x,self.c1_y,self.grosor,self.grosor) # the cookies
        self.rect_cookie2 = pygame.Rect(self.c2_x,self.c2_y,self.grosor,self.grosor) # the cookies

    def draw(self,window):
        #window.blit(self.cookie1, (self.rect_cookie1.x,self.rect_cookie1.y))  # literalmente yo
        window.blit(self.cookie2, (self.rect_cookie2.x,self.rect_cookie2.y))  # literalmente yo

class Goal():
    
    x_goal = 1000
    y_goal = 500
    grosor = 50
    
    def __init__(self):
        
        self.im_goal = car
        self.rect = pygame.Rect(self.x_goal,self.y_goal,self.im_goal.get_width(),self.im_goal.get_height())
        self.car_rect = self.im_goal.get_rect()
        self.car_rect.x = self.x_goal
        self.car_rect.y = self.y_goal
    
    def draw(self,window):
        window.blit(self.im_goal, (self.car_rect.x,self.car_rect.y))
        
class DeathBeam():

    x_db = 10
    y_db = 0
    vel_db =3
    w_db = 2
    l_db = height

    def __init__(self):
        self.rect_db = pygame.Rect(self.x_db,self.y_db,self.w_db,self.l_db)

    def update(self):
        self.rect_db.x += self.vel_db

    def draw(self,window):
        pygame.draw.rect(window, (255, 0, 0 ), self.rect_db)


def eval_genomes(genomes, config):
    
    global ge, nets
    
    isrun = True
    players = []
    nplayers = 0
    fondo = Wallpaper()
    plataf = Plataforma()
    enem = Obstaculo()
    coche = Goal()
    rayo = DeathBeam()
    galletas = Cookies()

    ge = [] 
    nets = []

    def remove(index):
        # when a player dies, we delete the genome
        players.pop(index)
        ge.pop(index)
        nets.pop(index)
        
        
    for genome_id, genome in genomes:
        players.append(Player())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    
    # this is set so I only give cookie once
    check1 = [False for i in range(len(players))]
    check2 = [False for i in range(len(players))]
    check3 = [False for i in range(len(players))]

    while isrun:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        fondo.draw(window)
        enem.draw(window)
        coche.draw(window)
        rayo.draw(window)
        galletas.draw(window)
        rayo.update()

        for player in players:
            player.draw(window)
            player.update(window)
        
        for i,player in enumerate(players):
            if len(players) == 1:
                isrun = False
                break

            # here we need to check the outputs
            output = nets[i].activate(
                (players[i].ryan_rect.centerx,
                players[i].ryan_rect.centery, 
                dist(player.ryan_rect.center,enem.rect_obs.center)))

            decision = output.index(max(output)) # this tells me what output is better

            if decision == 0: # stay still
                pass
            if decision == 1: # move left
                players[i].ryan_left=True
            elif decision == 2: # move right 
                players[i].ryan_right=True
            else: # jump 
                players[i].ryan_jump=True

            # they are done if they get hit by the ray
            if player.ryan_rect.colliderect(rayo.rect_db):
                window.blit(expl,player.ryan_rect.topleft)
                ge[i].fitness -= 20
                remove(i)
                continue
                
            # spank if they hit the box
            if players[i].ryan_rect.colliderect(enem.rect_obs):
                window.blit(expl,player.ryan_rect.topleft)
                ge[i].fitness -= 50
                remove(i)
                continue

            # mini - cookie if they get in front of the box. works better without it
            '''
            distancia = dist(player.ryan_rect.center,( enem.rect_obs.centerx - 100, enem.rect_obs.centery))
            if players[i].ryan_rect.colliderect(galletas.rect_cookie1):
                if check1[i]==False:
                    ge[i].fitness += 5
                    check1[i]=True
                continue
            '''

            # cookie if they get on top of the box
            distancia = dist(player.ryan_rect.center,( enem.rect_obs.centerx, enem.rect_obs.centery+100 ))
            if players[i].ryan_rect.colliderect(galletas.rect_cookie2):
                pygame.draw.rect(window, (0, 255, 0), players[i].ryan_rect, 2)
                if check2[i]==False:
                    ge[i].fitness += 100
                    check2[i]=True
                continue
            
            # mega - cookie if they get to the car
            distancia = dist(player.ryan_rect.center,( enem.rect_obs.centerx, enem.rect_obs.centery))
            if players[i].ryan_rect.colliderect(coche.car_rect):
                pygame.draw.rect(window, (0, 255, 0), players[i].ryan_rect, 2)
                if check3[i]==False:
                    ge[i].fitness += 200
                    check3[i]=True
                remove(i)
                continue

            
        pygame.time.delay(20) 
        pygame.display.update()
    

def run_neat(config_path):
    
    # NEAT config
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction, 
        neat.DefaultSpeciesSet, 
        neat.DefaultStagnation, 
        config_path)
    
    p = neat.Population(config)
    
    # statistical results
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(1))

    # now we run the game with 50 generations of 50 members eeach
    p.run(eval_genomes, 50) 


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run_neat(config_path)
