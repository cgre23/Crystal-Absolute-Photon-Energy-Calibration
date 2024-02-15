# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:12:59 2019

@author: ggeloni
Edited to function by cgrech (Jul 6, 21)
"""

from sympy.utilities.iterables import multiset_permutations
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import time
import logging

def HXRSSopt(X, Y):
    dthp, dthy, dthr, alpha = Y
    h_list, k_list, l_list, roll_angle_list, pa_list = X
    p_angle_list, phen_list, label_list, linestyle_list, gid_list, color_list, roll_list =[], [], [], [], [], [], []
    
    def plotIR(hlm,Phene,Pitch,thy,thr):
 
        #Note: same conventions as LCLS!
        fig2 = plt.figure(1)
        plot = fig2.add_subplot(111)
        plot.set_title(" ")
        
        Pitch = 0
        Phene = 0
        hlm = [0,0,0]
    #annotaz = plot.annotate(" ", (0,0), (-60, 650), xycoords='axes fraction', textcoords='offset points', va='top') 
 
    def rotm(th,ux,uy,uz):
        r = np.array((
            ( ux*ux*(1-np.cos(th))+np.cos(th),     ux*uy*(1-np.cos(th))-uz*np.sin(th),     ux*uz*(1-np.cos(th))+uy*np.sin(th) ),
            ( ux*uy*(1-np.cos(th))+uz*np.sin(th),  uy*uy*(1-np.cos(th))+np.cos(th),        uy*uz*(1-np.cos(th))-ux*np.sin(th) ),
            ( ux*uz*(1-np.cos(th))-uy*np.sin(th),  uy*uz*(1-np.cos(th))+ux*np.sin(th),     uz*uz*(1-np.cos(th))+np.cos(th)    )
            )) 
        return r

    #(1) Pitch of thp around PitchAx, and rotation of Yaw and Roll axis:
    def rotm1(thp,pitchax,rollax,yawax):    
        r1 = rotm(np.pi/2-thp,pitchax[0],pitchax[1],pitchax[2])
        rollax2 = r1.dot(rollax)
        yawax2  = r1.dot(yawax)
        return r1, rollax2, yawax2

    #(2) Yaw of thy around yawax2, and rotation of Roll axis:
    def rotm2(thy,rollax2,yawax2):    
        r2 = rotm(thy,yawax2[0],yawax2[1],yawax2[2])
        rollax3 = r2.dot(rollax2)    
        return r2, rollax3

    #(3) Roll of thr around Rollax3:
    def rotm3(thr,rollax3):    
        r3 = rotm(thr,rollax3[0],rollax3[1],rollax3[2])
        return r3

    def kirot(thp,thy,thr,n0, pitchax,rollax,yawax):
        #note: it seems like in Alberto's tool the roll and yaw are not transformed by subsequent rotations. For comparison, Ileave this out too.
        r1, rollax2, yawax2 = rotm1(thp,pitchax,rollax,yawax)
        rollax2=rollax
        yawax2=yawax
        r2, rollax3 = rotm2(thy,rollax2,yawax2)
        rollax3=rollax
        r3 = rotm3(thr,rollax3)    
        return r3.dot(r2.dot(r1.dot(n0)))

    def phev(fact,n,h,k,l,a,thp,thy,thr,n0, pitchax,rollax,yawax):
        d=a/np.sqrt(h**2+k**2+l**2)
        return fact*np.sqrt(h**2+k**2+l**2)/(2*d*n*np.linalg.norm(kirot(thp,thy,thr,n0, pitchax,rollax,yawax).dot((h,k,l))))

    def plotene(thplist,fact,n,h,k,l,a,DTHP,thylist,thr,n0,pitchax,rollax,yawax):
        count=0
        for thp, thy in zip(thplist/180*np.pi, thylist): 
            eevlist[count] = (phev(fact,1,h,k,l,a,thp,thy,thr,n0,pitchax,rollax,yawax))
            count = count+1   
        rosso = np.array((1,1,1))
        verde = np.array((2,2,0))
        nero = np.array((1,1,3))
        blu = np.array((4,0,0))
        magenta = np.array((3,3,1))
        arancio = np.array((2,2,4))
        azzurro = np.array((3,3,3))
        giallo = np.array((1,1,5))
        viola = np.array((1,3,5))
        marrone = np.array((5,5,5))
        porpora = np.array((1,5,5))
        grigio = np.array((3,5,5))
        oro = np.array((3,5,5))
        beige = np.array((3,3,5))
        aquamarine = np.array((4,4,4))
        wheat = np.array((4,4,0))    
        if [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(rosso)): 
            colore='red'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(verde)): 
            colore='green'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(nero)):  
            colore='black'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(blu)): 
            colore='blue'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(magenta)): 
            colore='magenta'        
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(arancio)): 
            colore='orange'        
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(azzurro)): 
            colore='cyan'        
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(giallo)): 
            colore='yellow'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(viola)): 
            colore='violet'  
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(marrone)): 
            colore='brown'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(porpora)): 
            colore='purple'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(grigio)): 
            colore='grey'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(oro)): 
            colore='gold'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(beige)): 
            colore='beige'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(aquamarine)): 
            colore='aquamarine'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(wheat)): 
            colore='wheat'
        else :
            colore = 'black'        
        simbolo ='dashed'    
        if (h>=0 and k>=0 and l >=0) or (h<=0 and k<=0 and l<=0):
            simbolo = 'solid'    
        if not(h == k):
            simbolo = 'dashdot'
     
        #plt.plot(thplist+DTHP,eevlist,color=colore, linestyle=simbolo,label='['+str(h)+str(k)+str(l)+']'.format([h,k,l]),gid=[h,k,l])
        #plt.ylim((3000,19000))
        #plt.ylabel('Photon Energy (eV)')
        #plt.xlabel('Pitch angle (deg) \n \n (111) red - (220) green - (1,1,3) black - (400) blue - (331) magenta - (224) orange - (333) cyan - (115) yellow - (135) violet - (555) brown - (155) purple - (355) grey - (335) beige - (444) aquamarine - (440) wheat\n STYLE: - dashdot: h != k ; solid: h=k and h,k,l all positive ; dashed: otherwise \n CONVENTION h>=0 i.e. [h,k,l] coincides with [-h,-k,-l]')    
        
        gid=[h,k,l]
        color=colore
        linestyle=str(simbolo)
        label=str('['+str(h)+str(k)+str(l)+']'.format([h,k,l]))
        thplist_f=thplist+DTHP
        
        return thplist_f, eevlist, label, linestyle, gid, color

#User defined quantities
################ AMERICAN NAME CONVENTION --- OUR ROLL IS YAW HERE AND VICEVERSA!!!######################

    pitchax =  np.array((1,-1,0))/np.linalg.norm(np.array((1,-1,0)))
    #pitchax =  np.array((-1,1,0))/np.linalg.norm(np.array((-1,1,0)))
    rollax  =  np.array((0,0,1))/np.linalg.norm(np.array((0,0,1)))
    yawax   =  np.array((1,1,0))/np.linalg.norm(np.array((1,1,0)))
    n0 = -rollax #direction of incident radiation
    
    
    a = 3.5667899884942195e-10
    hbar = 1.05457173e-34
    clight = 299792458.0
    eel = 1.60217657e-19
    
    fact = 2*np.pi*clight*hbar/eel
    
    nord=1   
    DTHP = dthp#-0.6921-0.09 

    for h, k, l, roll_angle, pitch_a in zip(h_list, k_list, l_list, roll_angle_list, pa_list):
        thplist=np.linspace(pitch_a,pitch_a,1)+DTHP 
        eevlist=np.zeros(len(thplist))
        
        DTHY = dthy+(alpha*thplist)    #15#15#0#-0.15#-0.39#-0.15 #0.0885
        DTHR = dthr
        thylist=(-DTHY+roll_angle)/180*np.pi                 #######AMERICAN YAW DEFINITION 
        thr=(-DTHR)/180*np.pi#0.0/180*np.pi   #########AMERICAN ROLL DEFINITION
        
        ref = h*np.array((1,0,0))+k*np.array((0,1,0))+l*np.array((0,0,1))
        p_angle, phen, label, linestyle, gid, color = plotene(thplist,fact,nord,h,k,l,a,DTHP,thylist,thr,n0,pitchax,rollax,yawax)
        phen_list.append(float(phen))   
                    
    return phen_list


def HXRSSopt_roll(X, Y):
    dthp, dthy, dthr, alpha = Y
    h_list, k_list, l_list, pitch_angle_list, centroid_ra = X
    r_angle_list, phen_list, label_list, linestyle_list, gid_list, color_list, roll_list =[], [], [], [], [], [], []
    
    def plotIR(hlm,Phene,Pitch,thy,thr):
 
        #Note: same conventions as LCLS!
        fig2 = plt.figure(1)
        plot = fig2.add_subplot(111)
        plot.set_title(" ")
        
        Pitch = 0
        Phene = 0
        hlm = [0,0,0]
    #annotaz = plot.annotate(" ", (0,0), (-60, 650), xycoords='axes fraction', textcoords='offset points', va='top') 
 
    def rotm(th,ux,uy,uz):
        r = np.array((
            ( ux*ux*(1-np.cos(th))+np.cos(th),     ux*uy*(1-np.cos(th))-uz*np.sin(th),     ux*uz*(1-np.cos(th))+uy*np.sin(th) ),
            ( ux*uy*(1-np.cos(th))+uz*np.sin(th),  uy*uy*(1-np.cos(th))+np.cos(th),        uy*uz*(1-np.cos(th))-ux*np.sin(th) ),
            ( ux*uz*(1-np.cos(th))-uy*np.sin(th),  uy*uz*(1-np.cos(th))+ux*np.sin(th),     uz*uz*(1-np.cos(th))+np.cos(th)    )
            )) 
        return r

    #(1) Pitch of thp around PitchAx, and rotation of Yaw and Roll axis:
    def rotm1(thp,pitchax,rollax,yawax):    
        r1 = rotm(np.pi/2-thp,pitchax[0],pitchax[1],pitchax[2])
        rollax2 = r1.dot(rollax)
        yawax2  = r1.dot(yawax)
        return r1, rollax2, yawax2

    #(2) Yaw of thy around yawax2, and rotation of Roll axis:
    def rotm2(thy,rollax2,yawax2):    
        r2 = rotm(thy,yawax2[0],yawax2[1],yawax2[2])
        rollax3 = r2.dot(rollax2)    
        return r2, rollax3

    #(3) Roll of thr around Rollax3:
    def rotm3(thr,rollax3):    
        r3 = rotm(thr,rollax3[0],rollax3[1],rollax3[2])
        return r3

    def kirot(thp,thy,thr,n0, pitchax,rollax,yawax):
        #note: it seems like in Alberto's tool the roll and yaw are not transformed by subsequent rotations. For comparison, Ileave this out too.
        r1, rollax2, yawax2 = rotm1(thp,pitchax,rollax,yawax)
        rollax2=rollax
        yawax2=yawax
        r2, rollax3 = rotm2(thy,rollax2,yawax2)
        rollax3=rollax
        r3 = rotm3(thr,rollax3)    
        return r3.dot(r2.dot(r1.dot(n0)))

    def phev(fact,n,h,k,l,a,thp,thy,thr,n0, pitchax,rollax,yawax):
        d=a/np.sqrt(h**2+k**2+l**2)
        return fact*np.sqrt(h**2+k**2+l**2)/(2*d*n*np.linalg.norm(kirot(thp,thy,thr,n0, pitchax,rollax,yawax).dot((h,k,l))))

    def plotene(thp,fact,n,h,k,l,a,DTHY,thylist,thr,n0,pitchax,rollax,yawax):
        count=0
        for thy in thylist/180*np.pi:
            eevlist[count] = (phev(fact,1,h,k,l,a,thp,thy,thr,n0,pitchax,rollax,yawax))
            count = count+1   
        rosso = np.array((1,1,1))
        verde = np.array((2,2,0))
        nero = np.array((1,1,3))
        blu = np.array((4,0,0))
        magenta = np.array((3,3,1))
        arancio = np.array((2,2,4))
        azzurro = np.array((3,3,3))
        giallo = np.array((1,1,5))
        viola = np.array((1,3,5))
        marrone = np.array((5,5,5))
        porpora = np.array((1,5,5))
        grigio = np.array((3,5,5))
        oro = np.array((3,5,5))
        beige = np.array((3,3,5))
        aquamarine = np.array((4,4,4))
        wheat = np.array((4,4,0))    
        if [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(rosso)): 
            colore='red'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(verde)): 
            colore='green'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(nero)):  
            colore='black'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(blu)): 
            colore='blue'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(magenta)): 
            colore='magenta'        
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(arancio)): 
            colore='orange'        
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(azzurro)): 
            colore='cyan'        
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(giallo)): 
            colore='yellow'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(viola)): 
            colore='violet'  
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(marrone)): 
            colore='brown'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(porpora)): 
            colore='purple'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(grigio)): 
            colore='grey'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(oro)): 
            colore='gold'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(beige)): 
            colore='beige'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(aquamarine)): 
            colore='aquamarine'
        elif [np.abs(h),np.abs(k),np.abs(l)] in list(multiset_permutations(wheat)): 
            colore='wheat'
        else :
            colore = 'black'        
        simbolo ='dashed'    
        if (h>=0 and k>=0 and l >=0) or (h<=0 and k<=0 and l<=0):
            simbolo = 'solid'    
        if not(h == k):
            simbolo = 'dashdot'
           
        gid=[h,k,l]
        color=colore
        linestyle=str(simbolo)
        label=str('['+str(h)+str(k)+str(l)+']'.format([h,k,l]))
        thylist_f=thylist+DTHY
        
        return thylist_f, eevlist, label, linestyle, gid, color

#User defined quantities
################ AMERICAN NAME CONVENTION --- OUR ROLL IS YAW HERE AND VICEVERSA!!!######################

    pitchax =  np.array((1,-1,0))/np.linalg.norm(np.array((1,-1,0)))
    #pitchax =  np.array((-1,1,0))/np.linalg.norm(np.array((-1,1,0)))
    rollax  =  np.array((0,0,1))/np.linalg.norm(np.array((0,0,1)))
    yawax   =  np.array((1,1,0))/np.linalg.norm(np.array((1,1,0)))
    n0 = -rollax #direction of incident radiation
    
    
    a = 3.5667899884942195e-10
    hbar = 1.05457173e-34
    clight = 299792458.0
    eel = 1.60217657e-19
    
    fact = 2*np.pi*clight*hbar/eel
    
    nord=1   
    DTHP = dthp#-0.6921-0.09 

    for h, k, l, pitch_angle, roll_a in zip(h_list, k_list, l_list, pitch_angle_list, centroid_ra):
        thylist=np.linspace(roll_a,roll_a,1) 
        eevlist=np.zeros(len(thylist))
        
        thp=(-DTHP+pitch_angle)/180*np.pi                 #######AMERICAN YAW DEFINITION 
        DTHY = dthy+(alpha*thp)    #15#15#0#-0.15#-0.39#-0.15 #0.0885
        DTHR = dthr
        thr=(-DTHR)/180*np.pi#0.0/180*np.pi   #########AMERICAN ROLL DEFINITION
        
        ref = h*np.array((1,0,0))+k*np.array((0,1,0))+l*np.array((0,0,1))
        r_angle, phen, label, linestyle, gid, color = plotene(thp,fact,nord,h,k,l,a,DTHY,thylist,thr,n0,pitchax,rollax,yawax)
        phen_list.append(float(phen))   
                    
    return phen_list