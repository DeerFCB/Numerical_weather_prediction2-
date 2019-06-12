# -*- coding: utf-8 -*-
"""
Created on Fri May 24 08:15:24 2019

@author: Deer
"""
import os
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
from pylab import *
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def read(path):
    path +='draw/'
    files= os.listdir(path)
    df = {}
    filenames = []
    for file in files: #遍历文件夹     
        if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开 
            filename = os.path.splitext(file)[0]
            df[filename] = pd.read_csv(path+file,header=None,sep='\s+').values
    dataor = np.array([df['uc'],df['vc'],df['zc']])
    data23 = np.array([df['uc23'],df['vc23'],df['zc23']])
    dataqn = np.array([df['ucqn'],df['vcqn'],df['zcqn']])
    datawbj = np.array([df['ucwbj'],df['vcwbj'],df['zcwbj']])
    datawbjwnd = np.array([df['ucwbjwnd'],df['vcwbjwnd'],df['zcwbjwnd']])
    datawnd = np.array([df['ucwnd'],df['vcwnd'],df['zcwnd']])
    
    return dataor,data23,dataqn,datawbj,datawbjwnd,datawnd,filenames

def error(dor,d):
    dferror = d.copy()
    dferror = dferror-dor
    return dferror
    
def windspeed(da):
    x1 = ((da[0,:,:] ** 2 + da[1,:,:] ** 2) ** 0.5)[np.newaxis, :]
    da =np.concatenate((da,x1))
    return da

def sample_data(shape=(16, 20)):
    """
    Return ``(x, y, u, v, crs)`` of some vector data
    computed mathematically. The returned CRS will be a North Polar
    Stereographic projection, meaning that the vectors will be unevenly
    spaced in a PlateCarree projection.
    """
    crs = ccrs.PlateCarree()
    x = np.linspace(88.5, 158.5, shape[1])
    y = np.linspace(32.5, 72.5, shape[0])
    X,Y = np.meshgrid(x, y)
    return X, Y, crs

def drawwind(pre,data,path,filenames):
    fig = plt.figure(figsize=(16,20))
    ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    ax.set_extent([88.5, 158.5, 32.5, 72.5], crs=ccrs.PlateCarree())
    ax.coastlines(pre[3])
    fig1 = ax.quiver(pre[0], pre[1], data[0], data[1], data[3], transform=pre[2])
    ax.set_xticks(np.arange(88.5,158.5,9), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(32.5,72.5,9), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter()
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    plt.colorbar(fig1)

    fig.savefig(path+'w'+filenames+'.jpg')
    plt.close(fig)


def drawz(pre,data,path,filenames):
    fig = plt.figure(figsize=(16,20))
    ax2 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax2.set_extent([88.5, 158.5, 32.5, 72.5], crs=ccrs.PlateCarree())
    ax2.coastlines('50m')
    fig2 = ax2.contourf(pre[0], pre[1], data[2], transform=pre[2])
    ax2.set_xticks(np.arange(88.5,158.5,9), crs=ccrs.PlateCarree())
    ax2.set_yticks(np.arange(32.5,72.5,9), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter()
    lat_formatter = LatitudeFormatter()
    ax2.xaxis.set_major_formatter(lon_formatter)
    ax2.yaxis.set_major_formatter(lat_formatter)
    plt.colorbar(fig2)
    fig.savefig(path+'z'+filenames+'.jpg')
    plt.close(fig)


def main():
    path = "C:/Users/Deer/Desktop/shuzhi/" #文件夹目录
    scale = '50m'
    
    X, Y, vector_crs = sample_data(shape=(16, 20))
    pre = [X,Y,vector_crs,scale]
    
    dor,d23,dqn,dwbj,dwbjwnd,dnd,filenames = read(path)
    
    
    #计算风速
    [dor,d23,dqn,dwbj,dwbjwnd,dnd] = \
    map(windspeed,[dor,d23,dqn,dwbj,dwbjwnd,dnd])
    dor1 = [dor]*5
    
    #误差场
    [er23,erqn,erwbj,erwbjwnd,ernd] = \
    map(error,dor1,[d23,dqn,dwbj,dwbjwnd,dnd])
    
    data = [dor,d23,dqn,dwbj,dwbjwnd,dnd,er23,erqn,erwbj,erwbjwnd,ernd]


    names = ['dor','d23','dqn','dwbj','dwbjwnd','dnd','er23','erqn','erwbj','erwbjwnd','ernd']
    for i in range(0,11):
        drawwind(pre,data[i],path,names[i])
        drawz(pre,data[i],path,names[i])


    #风场图
    
    
    
    #ax1 = fig.add_subplot(2, 2, 1, projection=ccrs.PlateCarree())
    #ax2 = fig.add_subplot(2, 2, 3, projection=ccrs.PlateCarree())

    
    
    
    
if __name__ =='__main__':
    main()
    


