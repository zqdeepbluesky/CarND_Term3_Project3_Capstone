from pid import PID
from lowpass import LowPassFilter
from yaw_controller import YawController
import rospy

GAS_DENSITY = 2.858
ONE_MPH = 0.44704

MIN_SPEED = 0.1
KP        = 0.3
KI        = 0.1
KD        = 0
MN        = 0
MX        = 0.2

TAU       = 0.5
TS        = 0.02


class Controller(object):
    def __init__(self, vehicle_mass, fuel_capacity, brake_deadband,
                 decel_limit, accel_limit, wheel_radius, wheel_base,
                 steer_ratio, max_lat_accel, max_steer_angle):
        # TODO: Implement
        self.yaw_controller = YawController(wheel_base      = wheel_base,
                                            steer_ratio     = steer_ratio,
                                            min_speed       = MIN_SPEED,
                                            max_lat_accel   = max_lat_accel,
                                            max_steer_angle = max_steer_angle)

        self.throttle_controller = PID(kp=KP, kd=KD, ki=KI, mn=MN, mx=MX)
        self.vel_lpf = LowPassFilter(tau=TAU, ts=TS)

        self.vehicle_mass   = vehicle_mass
        self.fuel_capacity  = fuel_capacity
        self.brake_deadband = brake_deadband
        self.decel_limit    = decel_limit
        self.accel_limit    = accel_limit
        self.wheel_radius   = wheel_radius

        self.last_time = rospy.get_time()




    def control(self, linear_vel, angular_vel, current_vel, dbw_enabled):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer
        if not dbw_enabled:
            self.throttle_controller.reset()
            return 0., 0., 0.

        current_vel = self.vel_lpf.filt(current_vel)
        steering = self.yaw_controller.get_steering(linear_velocity=linear_vel,
                                                    angular_velocity=angular_vel,
                                                    current_velocity=current_vel)

        vel_error = linear_vel - current_vel
        self.last_vel = current_vel

        current_time = rospy.get_time()
        sample_time = current_time - self.last_time
        self.last_time = current_time

        throttle = self.throttle_controller.step(error=vel_error, sample_time=sample_time)
        brake = 0

        if linear_vel == 0 and current_vel < 0.1:
            throttle = 0
            brake = 400 # N.m to hold the car in place if we are stopped at a light. Acceleration ~ 1m/s^2

        elif throttle < 0.1 and vel_error < 0:
            throttle = 0
            decel = max(vel_error, self.decel_limit)
            brake = abs(decel) * self.vehicle_mass * self.wheel_radius # Torque N*m

        return throttle, brake, steering