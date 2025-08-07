# https://sdurobotics.gitlab.io/ur_rtde/examples/examples.html#basic-use

import rtde_control
import rtde_receive


def robot_move() -> None:
    robot_ip = "172.17.0.2"

    rtde_c = rtde_control.RTDEControlInterface(hostname=robot_ip)
    rtde_c.moveL([-0.143, -0.435, 0.20, -0.001, 3.12, 0.04], 0.5, 0.3)

    rtde_r = rtde_receive.RTDEReceiveInterface(hostname=robot_ip)
    actual_q = rtde_r.getActualQ()
    print("Actual Q:", actual_q)


def main() -> None:
    robot_move()


if __name__ == "__main__":
    main()
