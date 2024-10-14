# --- TRICEII_trajectoryPlot_forOCHRE.py ---
# --- Author: C. Feltman ---
# DESCRIPTION: Plot the TRICEII trajectories in various forms


# --- --- --- --- ---
import time
start_time = time.time()
# --- --- --- --- ---

# --- --- --- ---
# --- TOGGLES ---
# --- --- --- ---
wRocket = 4
wFile =0
modifier = ''
inputPath_modifier = r'attitude'
outputPath_modifier = r'C:\Users\cfelt\Desktop\rockets\TRICE-II\Papers' # e.g. 'L2' or 'Langmuir'. It's the name of the broader output folder


# --------------LatvsLong------------------
altLatPlot = False
LatLong_Height = 10
LatLong_Width = 7
LatLong_Gridsize =2
LatLong_tickLabelSize = 12
LatLong_costLineSize = 2
LatLong_lineThickness = 2
LatLong_RktTrajectoryColor = 'tab:red'
LatLong_textSize = 8
lonW = 3
lonE = 27
latS = 65
latN = 86
res = '50m'
wImage = 10

Plot_LatLong = True

# --- --- --- ---
# --- import ---
# --- --- --- ---
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
from spaceToolsLib.Variables import fliers
from spaceToolsLib.Tools import prgMsg,Done,loadDictFromFile
from glob import glob
from data_paths import TRICE_data_folder
from missionAttributes import TRICE_mission_dicts
import cartopy.crs as ccrs

def ACESII_EISCAT_DensitySlice(wRocket, rocketFolderPath):

    # --- ACES II Flight/Integration Data ---
    rocketAttrs, b, c = TRICE_mission_dicts()
    rocketID = rocketAttrs.rocketID[wRocket-4]
    globalAttrsMod = rocketAttrs.globalAttributes[wRocket-4]
    inputFiles= glob(f'{rocketFolderPath}attitude\{fliers[wRocket-4]}{modifier}\*.cdf')[wFile]
    fileoutName = f'TRICEII_{rocketID}_EISCAT_Tromso_rktSlice.cdf'


    # --- --- --- --- --- -
    # --- LOAD THE DATA ---
    # --- --- --- --- --- -

    # --- get the data from the file ---
    prgMsg(f'Loading data TRICEII attitude Files')
    data_dict_attitude = loadDictFromFile(inputFiles)
    Done(start_time)

    try:
        lat = data_dict_attitude['latg'][0]
        long = data_dict_attitude['long'][0]
        Alt = data_dict_attitude['alt'][0]
        Epoch = data_dict_attitude['Epoch'][0]
    except:
        lat = data_dict_attitude['Latitude'][0]
        long = data_dict_attitude['Longitude'][0]
        Alt = data_dict_attitude['Altitude'][0]


    if Plot_LatLong:

        # Define projection
        projProjection = ccrs.Orthographic(central_longitude=15, central_latitude=70)
        projTransform = ccrs.PlateCarree()

        # Start Plot
        fig, ax = plt.subplots(1, subplot_kw=dict(projection=projProjection))
        figure_height = LatLong_Height
        figure_width = LatLong_Width
        fig.set_figwidth(figure_width)
        fig.set_figheight(figure_height)

        # PLOT
        gl = ax.gridlines(draw_labels=True, linewidth=LatLong_Gridsize,
                                   alpha=0.4,
                                   linestyle='--',
                                   color='black')

        gl.xlabel_style = {'size': LatLong_tickLabelSize, 'color': 'black', 'weight': 'bold'}
        gl.ylabel_style = {'size': LatLong_tickLabelSize, 'color': 'black', 'weight': 'bold'}
        gl.top_labels = False

        # extent of map
        ax.set_extent([lonW, lonE, latS, latN])  # controls lat/long axes display

        # coastlines
        ax.coastlines(resolution=res, color='black', alpha=1, linewidth=LatLong_costLineSize)  # adds coastlines with resolution

        # --- Plot the rocket trajectory --
        ax.plot(long, lat, transform=projTransform,linewidth=LatLong_lineThickness, color=LatLong_RktTrajectoryColor)
        # add colored box representing the cusp
        ax.axhspan(ymin=75.2, ymax=79, xmin=0, xmax=30, color='red', alpha=0.8, transform=projTransform)

        ax.legend(['TRICEII High Flyer'],fontsize=10)


        # add UTC timestamps
        timeTargetsUTC = [dt.datetime(2018, 12, 8, 8, 27, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 29, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 31, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 33, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 35, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 37, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 39, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 41, 00, 000000),
                          dt.datetime(2018, 12, 8, 8, 43, 00, 000000)
                      ] # find the UTC dates times of the specifically sampled labels
        LatLong_vertical_Alignments = ['bottom' for tme in timeTargetsUTC]
        LatLong_horizontal_Alignments = ['left' for tme in timeTargetsUTC]

        # find the lat/long of the targetTimes
        for j,time in enumerate(timeTargetsUTC):
            index = np.abs(Epoch - time).argmin()
            yPos = lat[index]
            xPos = long[index]
            vertical_text_label_adjustments = [0 for tme in timeTargetsUTC]
            horizontal_text_label_adjustments = [0.1 for tme in timeTargetsUTC]
            deltaY = vertical_text_label_adjustments[j] * yPos
            deltaX = horizontal_text_label_adjustments[j] * xPos
            ax.text(x=xPos + deltaX, y=yPos + deltaY, s=time.strftime("%H:%M:%S") + ' UTC', color='red', weight='bold',
                          va=LatLong_vertical_Alignments[j], ha=LatLong_horizontal_Alignments[j], size=LatLong_textSize,transform=projTransform)




        plt.tight_layout()
        fig.savefig(outputPath_modifier + r'\TRICEII_52003_LatLong.png')





# --- --- --- ---
# --- EXECUTE ---
# --- --- --- ---
rocketFolderPath = TRICE_data_folder
ACESII_EISCAT_DensitySlice(wRocket, rocketFolderPath)