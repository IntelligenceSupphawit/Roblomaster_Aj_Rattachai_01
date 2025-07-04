from robomaster import robot

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    x_val = 0.6
    # y_val = 0.6
    z_val = 90
    for i in range(4):
        ep_chassis.move(x=x_val, y=0, z=0, xy_speed=0.7).wait_for_completed()
        ep_chassis.move(x=0, y=0, z=-z_val, z_speed=45).wait_for_completed()

        # 获取传感器转接板adc值
        adc = ep_sensor_adaptor.get_adc(id=1, port=1)
        print("sensor adapter id1-port1 adc is {0}".format(adc))

        # 获取传感器转接板io电平
        io = ep_sensor_adaptor.get_io(id=1, port=1)
        print("sensor adapter id1-port1 io is {0}".format(io))

        # 获取传感器转接板io电平持续时间
        duration = ep_sensor_adaptor.get_pulse_period(id=1, port=1)
        print("sensor adapter id1-port1 duration is {0}ms".format(duration))

    ep_robot.close()