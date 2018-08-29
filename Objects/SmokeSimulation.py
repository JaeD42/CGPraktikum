
import numpy as np
import math
import pygame
from Utils.settings import *

class SmokeSimulation():

    def __init__(self,num_particles,position):
        self.num_particles = num_particles
        self.start_pos = position
        self.positions = np.random.normal(scale = 10,size=(num_particles,2))+position
        self.velocities = np.random.normal(scale = 2,size=(num_particles,2))
        self.h=5
        self.sigma = 0.1
        self.beta = 5
        self.rho_0 = 4.5
        self.k=5
        self.k_near = 6
        self.size = 7


    def step(self,dt,g=9.81):
        self.velocities[:,1]=-8*(1-(self.positions[:,1]-self.start_pos[1])/50)

        #self.apply_viscosity(dt)
        old_pos = self.positions[:]
        self.positions = self.positions + dt*self.velocities
        #self.double_density(dt)

        #self.velocities = (self.positions-old_pos)/dt

    def apply_viscosity(self,dt):
        for i in range(self.num_particles):
            rij_v = self.positions - self.positions[i]
            rij = np.linalg.norm(rij_v,axis=1)
            q = rij/self.h
            indx = q<1
            rij_v = rij_v[indx]
            rij = rij[indx]
            q = 1-q[indx]

            indx3 = np.abs(rij)<0.50

            rij_v = rij_v[indx3]
            rij = rij[indx3]
            q = 1-q[indx3]

            rij_n = rij_v/rij[:,None]
            #print(rij_n.shape)
            u = np.einsum("ij,ij->i",-self.velocities[indx][indx3]+self.velocities[i,None],rij_n)
            #print(np.isnan(u).any())
            #print(u.shape)
            indx2 = u>0

            u = u[indx2]
            q = q[indx2]
            I = dt*q*(self.sigma*u+self.beta*np.power(u,2))
            I = rij_n[indx2]*I[:,None]

            self.velocities[indx][indx3][indx2]-=I/2
            self.velocities[i]+=np.sum(I/2,axis=0)




    def double_density(self,dt):
        for i in range(self.num_particles):
            rho = 0
            rho_near = 0


            rij_v = self.positions - self.positions[i]
            rij = np.linalg.norm(rij_v,axis=1)
            q = rij/self.h
            indx = q<1
            rij_v = rij_v[indx]
            rij = rij[indx]
            q = 1-q[indx]
            rho = np.sum(np.power(q,2))
            rho_near = np.sum(np.power(q,3))

            #for j in range(self.num_particles):
            #    rij_v = self.positions[j]-self.positions[i]
            #    rij = math.sqrt(rij_v[1]**2+rij_v[0]**2)
            #    if rij==0:
            #        continue
            #    rij_n = rij_v/rij

            #    q = rij/self.h

            #    if q<1:
            #        rho += (1-q)**2
            #        rho_near+=(1-q)**3
            P = self.k*(rho-self.rho_0)
            P_near = self.k_near*rho_near
            dX = np.array([0.0,0.0])

            indx2 = rij!=0
            rij_v = rij_v[indx2]
            rij = rij[indx2]
            q   = q[indx2]


            rij_n = rij_v/rij[:,None]

            D = dt**2 * (P*(q) + P_near*(q)**2)

            D = rij_n*D[:,None]

            self.positions[indx][indx2]+=D/2
            self.positions[i]-=np.sum(D/2,axis=0)



    def draw(self,screen,col=(0,0,0)):
        surf = pygame.Surface((2*self.size,2*self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf,(0,0,0,2),[self.size,self.size],self.size)
        for i in range(self.num_particles):
            #pygame.draw.circle(surf,(0,0,0,20),[int(j) for j in self.positions[i]],5)
            screen.blit(surf,[int(j)-self.size for j in self.positions[i]])

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Choo Choo")
    running = True

    smoke = SmokeSimulation(100,(600,350))

    # Settings
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, FLAGS, bestdepth)

    for _ in range(200):
        screen.fill((255,255,255))
        smoke.step(0.01)
        smoke.draw(screen)
        pygame.display.flip()
    pygame.quit()
