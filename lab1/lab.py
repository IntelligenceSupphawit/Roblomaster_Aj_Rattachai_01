from robomaster import robot
import time
import robomaster
import csv
from datetime import datetime

# บันทึกข้อมูลลงไฟล์ CSV
csv_file = open('sensor_data.csv', 'w', newline='')
csv_writer = csv.DictWriter(csv_file, fieldnames=['timestamp', 'speed', 'angle', 'yaw', 'pitch', 'roll'])
csv_writer.writeheader()

def log_data(speed, angle, yaw, pitch, roll):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_writer.writerow({
        'timestamp': timestamp,
        'speed': speed,
        'angle': angle,
        'yaw': yaw,
        'pitch': pitch,
        'roll': roll
    })
    csv_file.flush()

# ส่วนบันทึก Callcack Data
def sub_esc_info_handler(esc_info):
    speed, angle, timestamp, state = esc_info
    print(f"chassis esc: speed:{speed}, angle:{angle}, timestamp:{timestamp}, state:{state}")

    log_data("ESC", {
        "speed": speed,
        "angle": angle,
        "esc_timestamp": timestamp,
        "state": state
    })
  

def sub_attitude_info_handler(attitude_info):
    yaw, pitch, roll = attitude_info
    print("chassis attitude: yaw:{yaw}, pitch:{pitch}, roll:{roll} ")

    log_data("Attitude", {
        "yaw": yaw,
        "pitch": pitch,
        "roll": roll
    })

def sub_position_handler(position_info):
    x, y, z = position_info
    print("chassis position: x:{x}, y:{y}, z:{z}")

    log_data("Position", {
        "x": x,
        "y": y,
        "z": z
    })

def sub_imu_info_handler(imu_info):
    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_info
    print("chassis imu: acc_x:{acc_x}, acc_y:{acc_y}, acc_z:{acc_z}, gyro_x:{gyro_x}, gyro_y:{gyro_y}, gyro_z:{gyro_z}")

    log_data("IMU", {
        "acc_x": acc_x,
        "acc_y": acc_y,
        "acc_z": acc_z,
        "gyro_x": gyro_x,
        "gyro_y": gyro_y,
        "gyro_z": gyro_z
    })

def sub_status_info_handler(status_info):
    static_flag, up_hill, down_hill, on_slope, pick_up, slip_flag, impact_x, impact_y, impact_z, \
    roll_over, hill_static = status_info
    print("chassis status: static_flag:{static_flag}, up_hill:{up_hill}, down_hill:{down_hill}, on_slope:{on_slope}, "
          "pick_up:{pick_up}, impact_x:{pact_x}, impact_y:{impact_y}, impact_z:{impact_z}, roll_over:{roll_over}, "
          "hill_static:{hill_static}")
    
    log_data("Status", {
        "static_flag": static_flag,
        "up_hill": up_hill,
        "down_hill": down_hill,
        "on_slope": on_slope,
        "pick_up": pick_up,
        "impact_x": impact_x,
        "impact_y": impact_y,
        "impact_z": impact_z,
        "roll_over": roll_over,
        "hill_static": hill_static
    })

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    # ep_sensor_adaptor = ep_robot.sensor_adaptor

    ep_chassis.sub_status(freq=50, callback=sub_status_info_handler)
    ep_chassis.sub_imu(freq=10, callback=sub_imu_info_handler)
    time.sleep(3)
    ep_chassis.sub_position(freq=1, callback=sub_position_handler)
    ep_chassis.sub_attitude(freq=5, callback=sub_attitude_info_handler) 
    ep_chassis.sub_esc(freq=20, callback=sub_esc_info_handler)
    

    # เดินสี่เหลี่ยม
    x_val = 0.6
    # y_val = 0.6
    z_val = 90
    for i in range(4):
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.move(x=0, y=0, z=-z_val, z_speed=45).wait_for_completed()

    ep_chassis.unsub_position() 

    ep_chassis.unsub_status()
    ep_chassis.unsub_esc()
    ep_chassis.unsub_imu()
    ep_chassis.unsub_attitude()
     

    ep_robot.close()