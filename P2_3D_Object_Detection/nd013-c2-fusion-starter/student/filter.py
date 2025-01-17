# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        # State dimension
        self.state_dim = params.dim_state
        #Time step interval
        self.time_step = params.dt
        #Process noise scaling factor
        self.noise_scale = params.q

    def F(self):
        """Return the transition matrix F"""
        dt = self.time_step
        return np.matrix([
            [1., 0., 0., dt, 0., 0.],
            [0., 1., 0., 0., dt, 0.],
            [0., 0., 1., 0., 0., dt],
            [0., 0., 0., 1., 0., 0.],
            [0., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 1.]
        ])


    def Q(self):
        """Return the process noise covariance matrix Q"""
        q = self.noise_scale
        dt = self.time_step
        q1 = (dt**3 / 3) * q
        q2 = (dt**2 / 2) * q
        q3 = dt * q

        return np.matrix([
            [q1, 0., 0., q2, 0., 0.,],
            [0., q1, 0., 0., q2, 0.],
            [0., 0., q1, 0., 0., q2],
            [q2, 0., 0., q3, 0., 0.],
            [0., q2, 0., 0., q3, 0.],
            [0., 0., q2, 0., 0., q3]
        ])


    def predict(self, track):
        """Predict the next state x and covariance P and save them in track"""
        predicted_state = self.F() * track.x # Predicted state
        predicted_covariance = self.F() * track.P * self.F().T + self.Q() #Predicted Covariance
        track.set_x(predicted_state)
        track.set_P(predicted_covariance)
        

    def update(self, track, meas):
        """Update the state x and covariance P with a measurement and save them in track"""
        residual = self.gamma(track, meas)
        H_matrix = meas.sensor.get_H(track.x)
        residual_covariance = self.S(track, meas, H_matrix)
        identity_matrix = np.identity(self.state_dim)
        kalman_gain = track.P * H_matrix.T * np.linalg.inv(residual_covariance) #Kalman gain
        updated_state = track.x + kalman_gain * residual #Updated state
        updated_covariance = (identity_matrix - kalman_gain * H_matrix) * track.P #Updated Covariance
        track.set_x(updated_state)
        track.set_P(updated_covariance)
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        """Calculate and return the residual gamma"""
        return meas.z - meas.sensor.get_hx(track.x)

    def S(self, track, meas, H_matrix):
        """Calculate and return the covariance of the residual S"""

        return H_matrix * track.P * H_matrix.T +  meas.R