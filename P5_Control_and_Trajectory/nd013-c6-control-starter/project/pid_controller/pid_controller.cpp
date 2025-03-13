/**********************************************
 * Self-Driving Car Nano-degree - Udacity
 *  Created on: December 11, 2020
 *      Author: Mathilde Badoual
 **********************************************/

#include "pid_controller.h"
#include <vector>
#include <iostream>
#include <math.h>

using namespace std;

PID::PID() {
   // Define Errors for PID
   epsilon_p = 0.0;
   epsilon_i = 0.0;
   epsilon_d = 0.0;
   Kp = 0.0;
   Ki = 0.0;
   Kd = 0.0;
   output_limit_min = 0.0;
   output_limit_max = 0.0;
   delta_t = 0.0;
}

PID::~PID() {}

void PID::Init(double Kp, double Ki, double Kd, double output_lim_max, double output_lim_min) {
   /**
   * TODO: Initialize PID coefficients (and errors, if needed)
   **/
  this->Kp = Kp;
  this->Ki = Ki;
  this->Kd = Kd;
  this->output_limit_max = output_limit_max;
  this->output_limit_min = output_lim_min;

  // Reset the variables
  epsilon_p = 0.0;
  epsilon_i = 0.0;
  epsilon_d = 0.0;
  delta_t = 0.0;
}


void PID::UpdateError(double cte) {
   /**
   * TODO: Update PID errors based on cte.
   **/
  double prior_p_error = epsilon_p;
  epsilon_p = cte;

  epsilon_d = 0.0;
  if (delta_t > 0.0){
   epsilon_d = (cte - prior_p_error) / delta_t;
  }

  epsilon_i = epsilon_i + (cte * delta_t);
}

double PID::TotalError() {
   /**
   * TODO: Calculate and return the total error
    * The code should return a value in the interval [output_lim_mini, output_lim_maxi]
   */
    double control = Kp * epsilon_p + Ki * epsilon_i + Kd * epsilon_d;

    // Ensuring results stay within acceptable boundaries
    if (control >= output_limit_max){
      return output_limit_max;
    }
    if (control <= output_limit_min){
      return output_limit_min;
    }
    return control;
}

double PID::UpdateDeltaTime(double new_delta_time) {
   /**
   * TODO: Update the delta time with new value
   */
  delta_t = new_delta_time;
  return delta_t;
}