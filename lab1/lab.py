from robomaster import robot
import time
import robomaster

def sub_esc_info_handler(esc_info):
    speed, angle, timestamp, state = esc_info
    print("chassis esc: speed:{0}, angle:{1}, timestamp:{2}, state:{3}".format(speed, angle, timestamp, state))

def sub_attitude_info_handler(attitude_info):
    yaw, pitch, roll = attitude_info
    print("chassis attitude: yaw:{0}, pitch:{1}, roll:{2} ".format(yaw, pitch, roll))

def sub_position_handler(position_info):
    x, y, z = position_info
    print("chassis position: x:{0}, y:{1}, z:{2}".format(x, y, z))

def sub_imu_info_handler(imu_info):
    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_info
    print("chassis imu: acc_x:{0}, acc_y:{1}, acc_z:{2}, gyro_x:{3}, gyro_y:{4}, gyro_z:{5}".format(
        acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z))

def sub_status_info_handler(status_info):
    static_flag, up_hill, down_hill, on_slope, pick_up, slip_flag, impact_x, impact_y, impact_z, \
    roll_over, hill_static = status_info
    print("chassis status: static_flag:{0}, up_hill:{1}, down_hill:{2}, on_slope:{3}, "
          "pick_up:{4}, impact_x:{5}, impact_y:{6}, impact_z:{7}, roll_over:{8}, "
          "hill_static:{9}".format(static_flag, up_hill, down_hill, on_slope, pick_up,
                                   slip_flag, impact_x, impact_y, impact_z, roll_over, hill_static))

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    # ep_sensor_adaptor = ep_robot.sensor_adaptor
    # 订阅底盘位置信息
    ep_chassis.sub_position(freq=1, callback=sub_position_handler)

    # 订阅底盘姿态信息
    ep_chassis.sub_attitude(freq=5, callback=sub_attitude_info_handler)

    # 订阅底盘IMU信息
    ep_chassis.sub_imu(freq=10, callback=sub_imu_info_handler)

    # 订阅底盘电调信息
    ep_chassis.sub_esc(freq=20, callback=sub_esc_info_handler)

    # 订阅底盘状态信息：
    ep_chassis.sub_status(freq=50, callback=sub_status_info_handler)

    time.sleep(10000)


    # เดินสี่เหลี่ยม
    x_val = 0.6
    # y_val = 0.6
    z_val = 90
    for i in range(4):
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.move(x=0, y=0, z=-z_val, z_speed=45).wait_for_completed()

    ep_chassis.unsub_status()
    ep_chassis.unsub_esc()
    ep_chassis.unsub_imu()
    ep_chassis.unsub_attitude()
    ep_chassis.unsub_position()  

    ep_robot.close()