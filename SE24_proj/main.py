import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI
import unittest

# execute_command를 제어하는 콜백 함수
def execute_command_callback(command, car_controller):
    # current_speed = car_controller.get_speed()

    if command == "ENGINE_BTN":
        if car_controller.get_engine_status(): # 시동 ON -> OFF
            if car_controller.get_speed() == 0: # 속도가 0이어야
                car_controller.toggle_engine() # ON -> OFF 동작
                return True
            print("Command failed: 주행 중에는 시동을 끌 수 없습니다.")
            return False
        else: # 시동 OFF -> ON
            car_controller.toggle_engine() # 시동 ON / OFF
            return True

    elif command == "ACCELERATE":
        # '테스트임' 시동 꺼졌을 때 작동 불가
        if not car_controller.get_engine_status():
            print("Command failed: 시동이 꺼져있어 가속할 수 없습니다.")
            return False
        if car_controller.get_speed() >= 200:
            print("200 이상으로 속도를 높힐 수 없음")
            return False
        if not car_controller.get_trunk_status():
            print("트렁크 문이 열려있습니다. 가속할 수 없습니다.")
            return False
        if car_controller.get_right_door_status() == "Opened":
            print("오른쪽 문이 열려있습니다. 가속할 수 없습니다.")
            return False
        if car_controller.get_left_door_status() == "Opeded":
            print("왼쪽 문이 열려있습니다. 가속할 수 없습니다.")
            return False
        car_controller.accelerate()  # 속도 +10
        if car_controller.get_speed() >= 10:
            car_controller.lock_vehicle()
            # '테스트임' 실행해보니 속도 증가할 때 문이 안잠겨서 조건 추가함 근데 lock_vehicle 진짜 어따 써먹는거지 ㅋㅋ
            # 차량 잠금을 하면 문잠금이랑 연관시키지 말고 아무것도 조작 못하도록 설정할까
            car_controller.lock_left_door()   # 각 도어도 잠가야 함
            car_controller.lock_right_door()
        return True

    elif command == "BRAKE":
         car_controller.brake()   # 감속 -10
         return True

    elif command == "LOCK":
        if car_controller.get_lock_status():
            print("이미 문이 잠겨있습니다.")
            return False
        elif car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 열려있습니다.")
            return False
        elif car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽 문이 열려있습니다.")
            return False
            # '테스트임' status 함수의 () 빠져있었음 ㅇ
        elif not car_controller.get_trunk_status():
            print("Commad failed: 트렁크가 열려있습니다.")
            return False
        else:
            car_controller.lock_vehicle()
            car_controller.lock_left_door()
            car_controller.lock_right_door() # 차량잠금
            return True

    elif command == "UNLOCK":
        if (car_controller.get_speed() > 0):
            print("Command failed: 주행 중으로 문을 잠금 해제 할 수 없습니다.")
            # 실패시 
            return False 
        elif not car_controller.get_lock_status():
            print("이미 문의 잠금이 해제되어 있습니다.")
            return False
        # 중복
        # elif car_controller.get_right_door_status() == "OPEN":
        #     print("오른쪽 문이 열려있습니다.")
        # elif car_controller.get_left_door_status() == "OPEN":
        #     print("왼쪽 문이 열려있습니다.")
        else:
            car_controller.unlock_vehicle()
            car_controller.unlock_left_door()
            car_controller.unlock_right_door() # 차량잠금해제
            return True

    elif command == "LEFT_DOOR_LOCK":
        if car_controller.get_left_door_status() == "OPEN":
            print("Command failed: 왼쪽문이 열려있어 잠글 수 없습니다.")
            return False
        if car_controller.get_left_door_lock() == "LOCKED":
           print("Command failed: 이미 잠겨있습니다.")
           return False
        car_controller.lock_left_door()  # 왼쪽문 잠금
        return True

    elif command == "RIGHT_DOOR_LOCK":
        if car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 열려있어 잠글 수 없습니다.")
            return False
        if car_controller.get_right_door_lock() == "LOCKED":
           print("Command failed: 이미 잠겨있습니다.")
           return False
        car_controller.lock_right_door()  # 오른쪽문 잠금
        return True

    elif command == "LEFT_DOOR_UNLOCK":
        if car_controller.get_speed() > 0:
            print("Command failed: 차량이 주행 중입니다. 왼쪽 문 잠금해제 불가")
            return False
        if car_controller.get_left_door_lock() == "UNLOCKED":
           print("Command failed: 이미 잠금 해제되어 있습니다.")
           return False
        if car_controller.get_lock_status():
           print("Command failed: 차량 전체 잠금이 설정되어있습니다. 문 못연다")
           return False
        car_controller.unlock_left_door()  # 왼쪽문 잠금해제
        return True

    elif command == "RIGHT_DOOR_UNLOCK":
        if car_controller.get_speed() > 0:
            print("Command failed: 차량이 주행 중입니다. 오른쪽 문 잠금해제 불가")
            return False
        if car_controller.get_right_door_lock() == "UNLOCKED":
           print("Command failed: 이미 잠금 해제되어 있습니다.")
           return False
        if car_controller.get_lock_status():
           print("Command failed: 차량 전체 잠금이 설정되어있습니다. 문 못연다")
           return False
        car_controller.unlock_right_door()  # 오른쪽문 잠금해제
        return True

    elif command == "LEFT_DOOR_OPEN":
        # '테스트임' 주행 중 차량 문 열기 제약조건 추가
        if car_controller.get_speed() > 0:  # 주행 중 체크 추가
            print("Command failed: 주행 중에는 문을 열 수 없습니다.")
            return False
        # '테스트임' 첫번째 if문 조건 잘못됨 door_status는 boolen 값이 아니라 상태를 오픈, 클로스 지정해줘야함
        #if car_controller.get_left_door_status():  # 문이 이미 열려 있는지 확인
        if car_controller.get_left_door_status() == "OPEN":  # 명확하게 OPEN 상태 체크
            print("Command failed: 왼쪽 문이 이미 열려 있습니다.")
            return False
        #if car_controller.get_left_door_lock():  # 문이 잠겨 있는지 확인
        if car_controller.get_left_door_lock() == "LOCKED":  # 명확하게 LOCKED 상태 체크
            print("Command failed: 왼쪽 문이 잠겨 있어 열 수 없습니다.")
            return False
        car_controller.open_left_door()  # 문 열기
        print("왼쪽 문이 열렸습니다.")
        return True

    elif command == "RIGHT_DOOR_OPEN":
        if car_controller.get_speed() > 0:
           print("Command failed: 주행 중에는 문을 열 수 없습니다.")
           return False
        #if car_controller.get_right_door_status():  # 문이 이미 열려 있는지 확인
        if car_controller.get_right_door_status() == "OPEN":
            print("Command failed: 오른쪽 문이 이미 열려 있습니다.")
            return False
        #if car_controller.get_right_door_lock():  # 문이 잠겨 있는지 확인
        if car_controller.get_right_door_lock() == "LOCKED":
            print("Command failed: 오른쪽 문이 잠겨 있어 열 수 없습니다.")
            return False
        car_controller.open_right_door()  # 문 열기
        print("오른쪽 문이 열렸습니다.")
        return True

    # 문 닫기
    elif command == "LEFT_DOOR_CLOSE":
        if car_controller.get_left_door_status() == "CLOSED":
           print("Command failed: 왼쪽 문이 이미 닫혀 있습니다.")
           return False
        car_controller.close_left_door()  # 문 닫기
        print("왼쪽 문이 닫혔습니다.")
        return True

    elif command == "RIGHT_DOOR_CLOSE":
        if car_controller.get_right_door_status() == "CLOSED":
           print("Command failed: 오른쪽 문이 이미 닫혀 있습니다.")
           return False
        car_controller.close_right_door()  # 문 닫기
        print("오른쪽 문이 닫혔습니다.")
        return True

    elif command == "TRUNK_OPEN":
        # 속도가 0일 때만 트렁크를 열 수 있음
        # if car_controller.get_speed() == 0:
        #     if car_controller.get_trunk_status():  # 트렁크가 닫혀 있을 때만 열기
        #         car_controller.open_trunk()
        #         print("트렁크가 열렸습니다.")
        #     else:
        #         print("트렁크가 이미 열려 있습니다.")
        # else:
        #     print("속도가 0이 아닙니다. 차량을 정지한 후 트렁크를 열 수 있습니다.")
        # '테스트임' 이중반복문 불필요
        if car_controller.get_speed() > 0:
           print("속도가 0이 아닙니다. 차량을 정지한 후 트렁크를 열 수 있습니다.")
           return False
        if not car_controller.get_trunk_status():
           print("트렁크가 이미 열려 있습니다.")
           return False
        car_controller.open_trunk()
        return True

    elif command == "TRUNK_CLOSE":
        # 트렁크가 열린 상태일 때만 닫기 가능
        # if not car_controller.get_trunk_status():  # 트렁크가 열려 있는 경우
        #     car_controller.close_trunk()
        #     print("트렁크가 닫혔습니다.")
        #     return False
        # else:
        #     print("트렁크가 이미 닫혀 있습니다.")
        # '테스트임' 함비교해보자
        if car_controller.get_trunk_status():
           print("트렁크가 이미 닫혀 있습니다.")
           return False
        car_controller.close_trunk()
        return True
    
    elif command == "SOS":
        while car_controller.get_speed() > 0:
            car_controller.brake()
        car_controller.unlock_vehicle()
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()
        car_controller.open_trunk()
        return
    
    return True



# -------------------------------------------------------------------------------



class TestCarSimulator(unittest.TestCase):
   def setUp(self):
       self.car = Car()
       self.controller = CarController(self.car)
       
   def execute_command(self, command):
       if command == "ENGINE_BTN":
           if self.controller.get_engine_status(): 
               if self.controller.get_speed() == 0:
                   self.controller.toggle_engine()
                   return True
               print("Command failed: 주행 중에는 시동을 끌 수 없습니다.")
               return False
           else:
               self.controller.toggle_engine()
               return True

       elif command == "ACCELERATE":
           if not self.controller.get_engine_status():  # 엔진 상태 체크 추가
               print("Command failed: 시동이 꺼져있어 가속할 수 없습니다.")
               return False
           if self.controller.get_speed() >= 200:
               print("200 이상으로 속도를 높힐 수 없음")
               return False
           if not self.controller.get_trunk_status():
               print("트렁크 문이 열려있습니다. 가속할 수 없습니다.")
               return False
           if self.controller.get_right_door_status() == "OPEN":
               print("오른쪽 문이 열려있습니다. 가속할 수 없습니다.")
               return False
           if self.controller.get_left_door_status() == "OPEN":
               print("왼쪽 문이 열려있습니다. 가속할 수 없습니다.")
               return False
           self.controller.accelerate()  # 속도 +10
           if self.controller.get_speed() >= 10:
               self.controller.lock_vehicle()
               self.controller.lock_left_door()   
               self.controller.lock_right_door()
           return True

       elif command == "BRAKE":
           self.controller.brake()   
           return True

       elif command == "LOCK":
           if self.controller.get_lock_status():
               print("이미 문이 잠겨있습니다.")
               return False
           elif self.controller.get_right_door_status() == "OPEN":
               print("Command failed: 오른쪽 문이 열려있습니다.")
               return False
           elif self.controller.get_left_door_status() == "OPEN":
               print("Command failed: 왼쪽 문이 열려있습니다.")
               return False
           elif not self.controller.get_trunk_status():
               print("Command failed: 트렁크가 열려있습니다.")
               return False
           else:
               self.controller.lock_vehicle()
               self.controller.lock_left_door()
               self.controller.lock_right_door()
               return True

       elif command == "UNLOCK":
           if (self.controller.get_speed() > 0):
               print("Command failed: 주행 중으로 문을 잠금 해제 할 수 없습니다.")
               return False
           elif not self.controller.get_lock_status():
               print("이미 문의 잠금이 해제되어 있습니다.")
               return False
           else:
               self.controller.unlock_vehicle()
               self.controller.unlock_left_door()
               self.controller.unlock_right_door()
               return True

       elif command == "LEFT_DOOR_LOCK":
           if self.controller.get_left_door_status() == "OPEN":
               print("Command failed: 왼쪽문이 열려있어 잠글 수 없습니다.")
               return False
           if self.controller.get_left_door_lock() == "LOCKED":
               print("Command failed: 이미 잠겨있습니다.")
               return False
           self.controller.lock_left_door()
           return True

       elif command == "RIGHT_DOOR_LOCK":
           if self.controller.get_right_door_status() == "OPEN":
               print("Command failed: 오른문 닫아라")
               return False
           if self.controller.get_right_door_lock() == "LOCKED":
               print("Command failed: 이미 잠겨있습니다.")
               return False
           self.controller.lock_right_door()
           return True

       elif command == "LEFT_DOOR_UNLOCK":
           if self.controller.get_speed() > 0:
               print("Command failed: 차량이 주행 중입니다. 왼쪽 문 잠금해제 불가")
               return False
           if self.controller.get_left_door_lock() == "UNLOCKED":
               print("Command failed: 이미 잠금 해제되어 있습니다.")
               return False
           self.controller.unlock_left_door()
           return True

       elif command == "RIGHT_DOOR_UNLOCK":
           if self.controller.get_speed() > 0:
               print("Command failed: 차량이 주행 중입니다. 오른쪽 문 잠금해제 불가")
               return False
           if self.controller.get_right_door_lock() == "UNLOCKED":
               print("Command failed: 이미 잠금 해제되어 있습니다.")
               return False
           self.controller.unlock_right_door()
           return True

       elif command == "LEFT_DOOR_OPEN":
           if self.controller.get_speed() > 0:
               print("Command failed: 주행 중에는 문을 열 수 없습니다.")
               return False
           if self.controller.get_left_door_status() == "OPEN":
               print("Command failed: 왼쪽 문이 이미 열려 있습니다.")
               return False
           if self.controller.get_left_door_lock() == "LOCKED":
               print("Command failed: 왼쪽 문이 잠겨 있어 열 수 없습니다.")
               return False
           self.controller.open_left_door()
           return True

       elif command == "RIGHT_DOOR_OPEN":
           if self.controller.get_speed() > 0:
               print("Command failed: 주행 중에는 문을 열 수 없습니다.") 
               return False
           if self.controller.get_right_door_status() == "OPEN":
               print("Command failed: 오른쪽 문이 이미 열려 있습니다.")
               return False
           if self.controller.get_right_door_lock() == "LOCKED":
               print("Command failed: 오른쪽 문이 잠겨 있어 열 수 없습니다.")
               return False
           self.controller.open_right_door()
           return True

       elif command == "LEFT_DOOR_CLOSE":
           if self.controller.get_left_door_status() == "CLOSED":
               print("Command failed: 왼쪽 문이 이미 닫혀 있습니다.")
               return False
           self.controller.close_left_door()
           return True

       elif command == "RIGHT_DOOR_CLOSE": 
           if self.controller.get_right_door_status() == "CLOSED":
               print("Command failed: 오른쪽 문이 이미 닫혀 있습니다.")
               return False
           self.controller.close_right_door()
           return True

       elif command == "TRUNK_OPEN":
           if self.controller.get_speed() > 0:
               print("속도가 0이 아닙니다. 차량을 정지한 후 트렁크를 열 수 있습니다.")
               return False
           if not self.controller.get_trunk_status():
               print("트렁크가 이미 열려 있습니다.")
               return False
           self.controller.open_trunk()
           return True

       elif command == "TRUNK_CLOSE":
           if self.controller.get_trunk_status():
               print("트렁크가 이미 닫혀 있습니다.")
               return False
           self.controller.close_trunk()
           return True

       return True

   def test_initial_state(self):
       """초기 상태 테스트"""
       self.assertFalse(self.controller.get_engine_status())  # 엔진 꺼짐
       self.assertEqual(self.controller.get_speed(), 0)  # 속도 0
       self.assertTrue(self.controller.get_trunk_status())  # 트렁크 닫힘
       self.assertEqual(self.controller.get_left_door_status(), "CLOSED")  # 좌측 문 닫힘
       self.assertEqual(self.controller.get_right_door_status(), "CLOSED")  # 우측 문 닫힘
       self.assertEqual(self.controller.get_left_door_lock(), "LOCKED")  # 좌측 문 잠김
       self.assertEqual(self.controller.get_right_door_lock(), "LOCKED")  # 우측 문 잠김

   def test_door_operations_sequence(self):
       """도어 작동 시퀀스 테스트"""
       # UNLOCK -> LEFT_DOOR_UNLOCK -> LEFT_DOOR_OPEN -> LEFT_DOOR_CLOSE -> LOCK
       self.assertTrue(self.execute_command("UNLOCK"))
       self.assertTrue(self.execute_command("LEFT_DOOR_OPEN"))  # 도어가 이미 unlock 되어 있으므로
       self.assertTrue(self.execute_command("LEFT_DOOR_CLOSE"))
       self.assertTrue(self.execute_command("LOCK"))

       # 잠긴 상태에서 열기 시도
       self.assertFalse(self.execute_command("LEFT_DOOR_OPEN"))

   def test_engine_and_speed(self):
       """엔진과 속도 제어 테스트"""
       # 엔진 켜고 가속
       self.assertTrue(self.execute_command("ENGINE_BTN"))
       self.assertTrue(self.execute_command("ACCELERATE"))
       self.assertEqual(self.controller.get_speed(), 10)
       
       # 속도 있을 때 엔진 끄기 시도
       self.assertFalse(self.execute_command("ENGINE_BTN"))
       
       # 브레이크로 감속
       self.assertTrue(self.execute_command("BRAKE"))
       self.assertEqual(self.controller.get_speed(), 0)
       
       # 속도 0에서 엔진 끄기
       self.assertTrue(self.execute_command("ENGINE_BTN"))
       self.assertFalse(self.controller.get_engine_status())

   def test_speed_restrictions(self):
       """속도 제한 관련 테스트"""
       self.execute_command("ENGINE_BTN")
       
       # 200km/h 제한 테스트
       for _ in range(20):
           self.execute_command("ACCELERATE")
       self.assertEqual(self.controller.get_speed(), 200)
       self.assertFalse(self.execute_command("ACCELERATE"))

       # 주행 중 제약사항 테스트
       self.assertFalse(self.execute_command("UNLOCK"))
       self.assertFalse(self.execute_command("LEFT_DOOR_UNLOCK"))
       self.assertFalse(self.execute_command("LEFT_DOOR_OPEN"))
       self.assertFalse(self.execute_command("TRUNK_OPEN"))

   def test_safety_features(self):
       """안전 기능 테스트"""
       self.execute_command("UNLOCK")
       self.execute_command("ENGINE_BTN")
       
       # 트렁크 열린 상태에서 가속 제한
       self.execute_command("TRUNK_OPEN")
       self.assertFalse(self.execute_command("ACCELERATE"))
       
       # 도어 열린 상태에서 가속 제한
       self.execute_command("TRUNK_CLOSE")
       self.execute_command("LEFT_DOOR_UNLOCK")
       self.execute_command("LEFT_DOOR_OPEN")
       self.assertFalse(self.execute_command("ACCELERATE"))

   def test_auto_lock(self):
       """자동 잠금 기능 테스트"""
       self.execute_command("UNLOCK")
       self.execute_command("ENGINE_BTN")
       self.execute_command("ACCELERATE")  # 10km/h
       
       # 속도 10km/h 이상에서 자동 잠금 확인
       self.assertTrue(self.controller.get_lock_status())
       self.assertEqual(self.controller.get_left_door_lock(), "LOCKED")
       self.assertEqual(self.controller.get_right_door_lock(), "LOCKED")

   def test_fail_scenario(self):
       """실패 시나리오 테스트"""
       # 잘못된 순서로 명령 실행
       self.assertFalse(self.execute_command("LEFT_DOOR_OPEN"))  # 잠긴 상태
       self.assertFalse(self.execute_command("ACCELERATE"))  # 엔진 꺼진 상태
       
       # 중복 명령 실행
       self.execute_command("UNLOCK")
       self.assertFalse(self.execute_command("UNLOCK"))  # 이미 잠금 해제됨
       
       # 부적절한 상태에서 명령 실행
       self.execute_command("ENGINE_BTN")
       self.execute_command("ACCELERATE")
       self.assertFalse(self.execute_command("TRUNK_OPEN"))  # 주행 중

   def test_example_success(self):
       """예제 성공 시나리오"""
       self.assertTrue(self.execute_command("UNLOCK"))
       self.assertTrue(self.execute_command("ENGINE_BTN"))
       self.assertTrue(self.execute_command("ACCELERATE"))
       self.assertEqual(self.controller.get_speed(), 10)

   def test_example_fail(self):
       """예제 실패 시나리오"""
       # 시나리오 1: 주행 중 트렁크 열기
       self.execute_command("UNLOCK")
       self.execute_command("ENGINE_BTN")
       self.execute_command("ACCELERATE")
       self.assertFalse(self.execute_command("TRUNK_OPEN"))

       # 시나리오 2: 잠긴 상태에서 문 열기
       self.execute_command("LEFT_DOOR_LOCK")
       self.assertFalse(self.execute_command("LEFT_DOOR_OPEN"))




# ------------------------------------------------------------------------



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

    # suite = unittest.TestSuite()
    
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEngineOperations))
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSpeedControl))
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDoorOperations))
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTrunkOperations))
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSafetyFeatures))
    
    # unittest.TextTestRunner().run(suite)
    
    #unittest.main()
