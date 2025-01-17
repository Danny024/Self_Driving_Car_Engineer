# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Data association class with single nearest neighbor association and gating based on Mahalanobis distance
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np
from scipy.stats.distributions import chi2

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import misc.params as params 

class Association:
    '''Data association class with single nearest neighbor association and gating based on Mahalanobis distance'''
    def __init__(self):
        self.association_matrix = np.matrix([])
        self.unassigned_tracks = []
        self.unassigned_meas = []
        
    def associate(self, track_list, meas_list, KF):
             
        ############
        # TODO Step 3: association:
        # - replace association_matrix with the actual association matrix based on Mahalanobis distance (see below) for all tracks and all measurements
        # - update list of unassigned measurements and unassigned tracks
        ############
        
        # the following only works for at most one track and one measurement
        self.association_matrix = np.matrix([]) # reset matrix
        self.unassigned_tracks = [] # reset lists
        self.unassigned_meas = []

        num_tracks = len(track_list)
        num_meas = len(meas_list)
        
        self.unassigned_tracks = list(range(num_tracks)) if num_tracks > 0 else []
        self.unassigned_meas = list(range(num_meas)) if num_meas > 0 else []
        if len(meas_list) > 0 and len(track_list) > 0: 
            self.association_matrix = np.asmatrix(np.full((num_tracks, num_meas), np.inf))

        for track_idx, track in enumerate (track_list):
            for meas_idx, measurement in enumerate (meas_list):
                distance = self.MHD(track, measurement, KF) # Calculate the Mahalanobis distance
                #print ("the distance is ", distance )
                value = measurement.sensor
                #print ("the measurement sensor is ", value)
                if self.gating (distance, measurement.sensor):
                    self.association_matrix[track_idx, meas_idx] = distance
        ############
        # END student code
        ############ 
                
    def get_closest_track_and_meas(self):
        ############
        # TODO Step 3: find closest track and measurement:
        # - find minimum entry in association matrix
        # - delete row and column
        # - remove corresponding track and measurement from unassigned_tracks and unassigned_meas
        # - return this track and measurement
        ############

        # the following only works for at most one track and one measurement
        update_track = 0
        update_meas = 0

        # get the association matrix
        association_matrix = self.association_matrix
        min_distance = np.min(association_matrix)

        # Check if there is a valid entry in the matrix
        if min_distance != np.inf:
            # Locate the minimum distance in the matrix
            track_idx, meas_idx = np.unravel_index(np.argmin(association_matrix, axis=None), association_matrix.shape)

            #retrieve the actual track and measurement indices
            update_track = self.unassigned_tracks[track_idx]
            update_meas = self.unassigned_meas[meas_idx]

            self.unassigned_tracks.pop(track_idx)
            self.unassigned_meas.pop(meas_idx)

            # Remove the corresponding row and column from the association matrix
            association_matrix = np.delete(association_matrix, track_idx, axis=0)
            association_matrix = np.delete(association_matrix, meas_idx, axis =1)
            self.association_matrix = association_matrix

            return update_track, update_meas
        else :
            # return Nan if no valid pair is found
            return np.nan, np.nan
            
        ############
        # END student code
        ############ 
         

    def gating(self, MHD, sensor): 
        ############
        # TODO Step 3: return True if measurement lies inside gate, otherwise False
        ############
        
        threshold = chi2.ppf(q=params.gating_threshold, df=sensor.dim_meas) 
        #print (" The mhd is ", MHD)
        #print ("the threshold is ", threshold)
        return MHD < threshold
        
        ############
        # END student code
        ############ 
        
    def MHD(self, track, meas, KF):
        ############
        # TODO Step 3: calculate and return Mahalanobis distance
        ############
        
        H_matrix = meas.sensor.get_H(track.x)

        # Compute the innovation vector
        innovation = meas.z - meas.sensor.get_hx(track.x)

        # calculate the innovation covariance
        covariance = KF.S(track, meas, H_matrix)

        #Manhalanoids distance
        #distance = np.sqrt(float(innovation.T @ np.linalg.inv(covariance) @ innovation))
        distance = np.sqrt (innovation.transpose()  * np.linalg.inv(covariance) * innovation)

        return distance
        
        ############
        # END student code
        ############ 
    
    def associate_and_update(self, manager, meas_list, KF):
        # associate measurements and tracks
        self.associate(manager.track_list, meas_list, KF)
    
        # update associated tracks with measurements
        while self.association_matrix.shape[0]>0 and self.association_matrix.shape[1]>0:
            
            # search for next association between a track and a measurement
            ind_track, ind_meas = self.get_closest_track_and_meas()
            if np.isnan(ind_track):
                print('---no more associations---')
                break
            track = manager.track_list[ind_track]
            
            # check visibility, only update tracks in fov    
            if not meas_list[0].sensor.in_fov(track.x):
                continue
            
            # Kalman update
            print('update track', track.id, 'with', meas_list[ind_meas].sensor.name, 'measurement', ind_meas)
            KF.update(track, meas_list[ind_meas])
            
            # update score and track state 
            manager.handle_updated_track(track)
            
            # save updated track
            manager.track_list[ind_track] = track
            
        # run track management 
        manager.manage_tracks(self.unassigned_tracks, self.unassigned_meas, meas_list)
        
        for track in manager.track_list:            
            print('track', track.id, 'score =', track.score)