import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

# execute_command를 제어하는 콜백 함수
def execute_command_callback(command, car_controller):
#시동
    if command == "ENGINE_BTN":
        if car_controller.get_engine_status():
            if car_controller.get_speed() != 0:
                print("Command failed: 주행 중으로 시동을 끌 수 없습니다.")
            else:
                car_controller.toggle_engine()
                print("시동이 꺼졌습니다.")
        else:
            car_controller.toggle_engine()
            print("시동이 켜졌습니다.")

#가속
    elif command == "ACCELERATE":
        if not car_controller.get_engine_status():
            print("Command failed: 시동이 꺼져있어 가속할 수 없습니다.")
            return
        if car_controller.get_speed() >= 200:
            print("Command failed: 200 이상으로 속도를 높힐 수 없습니다.")
            return
        if not car_controller.get_trunk_status() :
            print("Command failed: 트렁크 문이 열려있습니다. 가속할 수 없습니다.")
            return
        if car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 열려있습니다. 가속할 수 없습니다.")
            return
        if car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽 문이 열려있습니다. 가속할 수 없습니다.")
            return
        car_controller.accelerate()
        if car_controller.get_speed() >= 10 and not car_controller.get_lock_status():
            print("주행 중으로 문이 잠깁니다.")
            car_controller.lock_vehicle()
            car_controller.lock_left_door()
            car_controller.lock_right_door()

#감속
    elif command == "BRAKE":
         car_controller.brake()

#자동차 전체 문 잠금
    elif command == "LOCK":
        if car_controller.get_lock_status():
            print("Command failed: 이미 문이 잠겨있습니다.")
        elif car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 열려있습니다.")
        elif car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽 문이 열려있습니다.")
        elif not car_controller.get_trunk_status():
            print("Commad failed: 트렁크가 열려있습니다.")
        else:
            car_controller.lock_vehicle()
            car_controller.lock_left_door()
            car_controller.lock_right_door()

#자동차 전체 문 잠금 해제
    elif command == "UNLOCK":
        if (car_controller.get_speed() > 0):
            print("Command failed: 주행 중으로 문을 잠금 해제 할 수 없습니다.")
        elif not car_controller.get_lock_status():
            print("Command failed: 이미 문의 잠금이 해제되어 있습니다.")
        else:
            car_controller.unlock_vehicle()
            car_controller.unlock_left_door()
            car_controller.unlock_right_door()
            print("과제3 TEST 전체 잠금 해제된다.")

#왼쪽 문 잠금
    elif command == "LEFT_DOOR_LOCK":
        if car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽 문이 열려있습니다.")
            return
        elif car_controller.get_left_door_lock() == "LOCKED":
            print("Command failed: 왼쪽 문이 이미 잠겨있습니다.")
            return
        car_controller.lock_left_door()

#오른쪽 문 잠금
    elif command == "RIGHT_DOOR_LOCK":
        if car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 열려있습니다.")
            return
        elif car_controller.get_right_door_lock() == "LOCKED":
            print("Command failed: 오른쪽 문이 이미 잠겨있습니다.")
            return
        car_controller.lock_right_door()

#왼쪽 문 잠금해제
    elif command == "LEFT_DOOR_UNLOCK":
        if car_controller.get_lock_status():
            print("Command failed: 차량 전체 잠금이 설정되어있습니다. 잠금을 해제할 수 없습니다")
            return
        elif car_controller.get_speed() > 0:
            print("Command failed: 차량이 주행 중입니다. 왼쪽 문을 잠금해제 할 수 없습니다.")
            return
        elif car_controller.get_left_door_lock() == "UNLOCKED":
            print("Command failed: 이미 왼쪽 문의 잠금이 해제되어 있습니다.")
            return
        car_controller.unlock_left_door()

#오른쪽 문 잠금 해제
    elif command == "RIGHT_DOOR_UNLOCK":
        if car_controller.get_lock_status():
            print("Command failed: 차량 전체 잠금이 설정되어있습니다. 잠금을 해제할 수 없습니다.")
            return
        elif car_controller.get_speed() > 0:
            print("Command failed: 차량이 주행 중입니다. 오른쪽 문을 잠금해제 할 수 없습니다.")
            return
        elif car_controller.get_left_door_lock() == "UNLOCKED":
            print("Command failed: 이미 오른쪽 문의 잠금이 해제되어 있습니다.")
            return
        car_controller.unlock_right_door()

#왼쪽 문 열기
#memo : 전체 문잠금이 되어있을 경우 왼쪽 문을 열려고 하면, 안된다고 표시(print문)를 해야하나?
    elif command == "LEFT_DOOR_OPEN":
        if car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽 문이 이미 열려 있습니다.")
            return
        elif car_controller.get_left_door_lock() == "LOCKED":
            print("Command failed: 왼쪽 문이 잠겨 있어 열 수 없습니다.")
            return
        car_controller.open_left_door()
        print("왼쪽 문이 열렸습니다.")

#오른쪽 문 열기
    elif command == "RIGHT_DOOR_OPEN":
        if car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 이미 열려 있습니다.")
            return
        elif car_controller.get_right_door_lock() == "LOCKED":
            print("Command failed: 오른쪽 문이 잠겨 있어 열 수 없습니다.")
            return
        car_controller.open_right_door()
        print("오른쪽 문이 열렸습니다.")

#왼쪽 문 닫기
    elif command == "LEFT_DOOR_CLOSE":
        if car_controller.get_left_door_status() == "CLOSED":
            print("Command failed: 왼쪽 문이 이미 닫혀 있습니다.")
            return
        car_controller.close_left_door()
        print("왼쪽 문이 닫혔습니다.")

#오른쪽 문 닫기
    elif command == "RIGHT_DOOR_CLOSE":
        if car_controller.get_right_door_status() == "CLOSED":
            print("Command failed: 오른쪽 문이 이미 닫혀 있습니다.")
            return
        car_controller.close_right_door()
        print("오른쪽 문이 닫혔습니다.")

#트렁크 열기
    elif command == "TRUNK_OPEN":
        if car_controller.get_speed() > 0:
            print("Command failed: 속도가 0이 아닙니다. 차량을 정지한 후 트렁크를 열 수 있습니다.")
            return
        elif not car_controller.get_trunk_status():
            print("Command failed: 트렁크가 이미 열려 있습니다.")
            return
        elif car_controller.get_lock_status():
            print("Command failed: 차량 전체 잠금이 설정되어있습니다. 트렁크를 열 수 없습니다.")
            return
        car_controller.open_trunk()
        # [변경] 프린트문 추가
        print("트렁크가 열렸습니다.")

#트렁크 닫기
    elif command == "TRUNK_CLOSE":
        if not car_controller.get_trunk_status():
            car_controller.close_trunk()
            print("트렁크가 닫혔습니다.")
        else:



            print("Command failed: 트렁크가 이미 닫혀 있습니다.")


#긴급 SOS
    elif command == "SOS":
        while car_controller.get_speed() > 0:
            car_controller.brake()
            print("차량이 위급 상태입니다")
        car_controller.unlock_vehicle()
        print("차량 전체 잠금이 해제 되었습니다.")
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()
        car_controller.open_trunk()



# 파일 경로를 입력받는 함수
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        gui.window.after(0, lambda: gui.process_commands(file_path))

# 메인 실행
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car_controller, lambda command: execute_command_callback(command, car_controller))

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()