from robomaster import robot
import time
import robomaster
import csv
from datetime import datetime

logging_enabled = False  # ป้องกันการบันทึกข้อมูลก่อนเริ่มต้น

# บันทึกข้อมูลลงไฟล์ CSV

sensor_state = {
    "timestamp": None,
    "speed": None, "angle": None,
    "yaw": None, "pitch": None, "roll": None,
    "acc_x": None, "acc_y": None, "acc_z": None,
    "gyro_x": None, "gyro_y": None, "gyro_z": None,
    "x": None, "y": None, "z": None,
    "static_flag": None, "impact_x": None, "impact_y": None, "impact_z": None,
    "up_hill": None, "down_hill": None, "on_slope": None,
}

fieldnames = list(sensor_state.keys())
csv_file = open('sensor_data.csv', 'w', newline='')
csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
csv_writer.writeheader()

def update_and_log(**kwargs):
    global sensor_state
    if not logging_enabled:
        return  # ไม่บันทึกข้อมูลหาก logging enabled = false
    
    sensor_state.update(kwargs)
    sensor_state['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_writer.writerow(sensor_state)
    csv_file.flush()


# ส่วนบันทึก Callcack Data
def sub_esc_info_handler(esc_info):
    speed, angle, timestamp, state = esc_info
    print(f"chassis esc: speed:{speed}, angle:{angle}, timestamp:{timestamp}, state:{state}")

    update_and_log(speed=speed, angle=angle)
  

def sub_attitude_info_handler(attitude_info):
    yaw, pitch, roll = attitude_info
    print(f"chassis attitude: yaw:{yaw}, pitch:{pitch}, roll:{roll} ")

    update_and_log(yaw=yaw, pitch=pitch, roll=roll)

def sub_position_handler(position_info):
    x, y, z = position_info
    print(f"chassis position: x:{x}, y:{y}, z:{z}")

    update_and_log(x=x, y=y, z=z)

def sub_imu_info_handler(imu_info):
    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_info
    print(f"chassis imu: acc_x:{acc_x}, acc_y:{acc_y}, acc_z:{acc_z}, gyro_x:{gyro_x}, gyro_y:{gyro_y}, gyro_z:{gyro_z}")

    update_and_log(acc_x=acc_x, acc_y=acc_y, acc_z=acc_z,
                   gyro_x=gyro_x, gyro_y=gyro_y, gyro_z=gyro_z)

def sub_status_info_handler(status_info):
    static_flag, up_hill, down_hill, on_slope, pick_up, slip_flag, impact_x, impact_y, impact_z, \
    roll_over, hill_static = status_info
    print(f"chassis status: static_flag:{static_flag}, up_hill:{up_hill}, down_hill:{down_hill}, on_slope:{on_slope}, "
          "pick_up:{pick_up}, impact_x:{pact_x}, impact_y:{impact_y}, impact_z:{impact_z}, roll_over:{roll_over}, "
          "hill_static:{hill_static}")
    
    update_and_log(static_flag=static_flag, up_hill=up_hill, down_hill=down_hill,
                   on_slope=on_slope, impact_x=impact_x, impact_y=impact_y, impact_z=impact_z)

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

    # เริ่มบันทึกข้อมูลลง CSV เมื่อหุ่นเริ่มทำงานเท่านั้น
    logging_enabled = True

    for i in range(4):
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.move(x=0, y=0, z=-z_val, z_speed=45).wait_for_completed()

    logging_enabled = False  # หยุดบันทึกข้อมูลเมื่อเสร็จสิ้นการเคลื่อนที่

    ep_chassis.unsub_position() 

    ep_chassis.unsub_status()
    ep_chassis.unsub_esc()
    ep_chassis.unsub_imu()
    ep_chassis.unsub_attitude()
     

    ep_robot.close()
    csv_file.close()