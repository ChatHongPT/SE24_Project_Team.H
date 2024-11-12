import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

# execute_command를 제어하는 콜백 함수
def execute_command_callback(command, car_controller):
    current_speed = car_controller.get_speed()

    if command == "ENGINE_BTN":
        if car_controller.get_engine_status(): # 시동 ON -> OFF
            if car_controller.get_speed() == 0: # 속도가 0이어야
                car_controller.toggle_engine() # ON -> OFF 동작
        else: # 시동 OFF -> ON
            car_controller.toggle_engine() # 시동 ON / OFF
        car_controller.toggle_engine() # 시동 ON / OFF

    elif command == "ACCELERATE":
        if car_controller.get_speed() >= 200:
            print("200 이상으로 속도를 높힐 수 없음")
            return
        if not car_controller.get_trunk_status() :
            print("트렁크 문이 열려있습니다. 가속할 수 없습니다.")
            return
        if car_controller.get_right_door_status() == "Opened":
            print("오른쪽 문이 열려있습니다. 가속할 수 없습니다.")
            return
        if car_controller.get_left_door_status() == "Opened":
            print("왼쪽 문이 열려있습니다. 가속할 수 없습니다.")
            return
        car_controller.accelerate()  # 속도 +10
        if car_controller.get_speed() >= 10:
            car_controller.lock_vehicle()

    elif command == "BRAKE":
         car_controller.brake()   # 감속 -10

    elif command == "LOCK":
        if car_controller.get_lock_status() == True:
            print("이미 문이 잠겨있습니다.")
        elif car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 열려있습니다.")
        elif car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽 문이 열려있습니다.")
        elif car_controller.get_trunk_status == False:
            print("Commad failed: 트렁크가 열려있습니다.")
        else:
            car_controller.lock_vehicle()
            car_controller.lock_left_door()
            car_controller.lock_right_door() # 차량잠금

    elif command == "UNLOCK":
        if (car_controller.get_speed()>0):
            print("Command failed: 주행 중으로 문을 잠금 해제 할 수 없습니다.")
        elif car_controller.get_lock_status() == True:
            print("이미 문의 잠금이 해제되어 있습니다.")
        elif car_controller.get_right_door_status() == "OPEN":
            print("오른쪽 문이 열려있습니다.")
        elif car_controller.get_left_door_status() == "OPEN":
            print("왼쪽 문이 열려있습니다.")
        else:
            car_controller.unlock_vehicle()
            car_controller.unlock_left_door()
            car_controller.unlock_right_door() # 차량잠금해제

    elif command == "LEFT_DOOR_LOCK":
        if car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽문 닫아라")
            return
        car_controller.lock_left_door()  # 왼쪽문 잠금

    elif command == "RIGHT_DOOR_LOCK":
        if car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른문 닫아라")
            return
        car_controller.lock_right_door()  # 오른쪽문 잠금

    elif command == "LEFT_DOOR_UNLOCK":
        if car_controller.get_speed() > 0:
            print("Command failed: 멈춰라")
            return
        car_controller.unlock_left_door()  # 왼쪽문 잠금해제

    elif command == "RIGHT_DOOR_UNLOCK":
        if car_controller.get_speed() > 0:
            print("Command failed: 멈춰라")
            return
        car_controller.unlock_right_door()  # 오른쪽문 잠금해제

    elif command == "LEFT_DOOR_OPEN":
        if car_controller.get_left_door_status():  # 문이 이미 열려 있는지 확인
            print("Command failed: 왼쪽 문이 이미 열려 있습니다.")
            return
        if car_controller.get_left_door_lock():  # 문이 잠겨 있는지 확인
            print("Command failed: 왼쪽 문이 잠겨 있어 열 수 없습니다.")
            return
        car_controller.open_left_door()  # 문 열기
        print("왼쪽 문이 열렸습니다.")

    elif command == "RIGHT_DOOR_OPEN":
        if car_controller.get_right_door_status():  # 문이 이미 열려 있는지 확인
            print("Command failed: 오른쪽 문이 이미 열려 있습니다.")
            return
        if car_controller.get_right_door_lock():  # 문이 잠겨 있는지 확인
            print("Command failed: 오른쪽 문이 잠겨 있어 열 수 없습니다.")
            return
        car_controller.open_right_door()  # 문 열기
        print("오른쪽 문이 열렸습니다.")

    # 문 닫기
    elif command == "LEFT_DOOR_CLOSE":
        if not car_controller.get_left_door_status():  # 문이 열려 있는 상태인지 확인
            print("Command failed: 왼쪽 문이 이미 닫혀 있습니다.")
            return
        car_controller.close_left_door()  # 문 닫기
        print("왼쪽 문이 닫혔습니다.")

    elif command == "RIGHT_DOOR_CLOSE":
        if not car_controller.get_right_door_status():  # 문이 열려 있는 상태인지 확인
            print("Command failed: 오른쪽 문이 이미 닫혀 있습니다.")
            return
        car_controller.close_right_door()  # 문 닫기
        print("오른쪽 문이 닫혔습니다.")

    elif command == "TRUNK_OPEN":
        # 속도가 0일 때만 트렁크를 열 수 있음
        if car_controller.get_speed() == 0:
            if car_controller.get_trunk_status():  # 트렁크가 닫혀 있을 때만 열기
                car_controller.open_trunk()
                print("트렁크가 열렸습니다.")
            else:
                print("트렁크가 이미 열려 있습니다.")
        else:
            print("속도가 0이 아닙니다. 차량을 정지한 후 트렁크를 열 수 있습니다.")

    elif command == "TRUNK_CLOSE":
        # 트렁크가 열린 상태일 때만 닫기 가능
        if not car_controller.get_trunk_status():  # 트렁크가 열려 있는 경우
            car_controller.close_trunk()
            print("트렁크가 닫혔습니다.")
        else:
            print("트렁크가 이미 닫혀 있습니다.")


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
