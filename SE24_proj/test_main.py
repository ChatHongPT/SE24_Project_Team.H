import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback


class TestCarSystem(unittest.TestCase):
    def setUp(self):
        self.car = Car()  # 새로운 Car 인스턴스 생성
        self.car_controller = CarController(self.car)  # CarController 인스턴스 생성

    def test_engine_toggle(self):
        # ENGINE_BTN 명령 테스트
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())  # 엔진이 켜졌는지 확인

        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertFalse(self.car_controller.get_engine_status())  # 엔진이 꺼졌는지 확인

    def test_accelerate(self):
        # 시동 켜고 가속 테스트
        execute_command_callback("ENGINE_BTN", self.car_controller)  # 엔진 켬
        execute_command_callback("ACCELERATE", self.car_controller)  # 가속
        self.assertEqual(self.car_controller.get_speed(), 10)  # 속도가 10인지 확인

        # 속도가 200을 초과하지 않는지 테스트
        for _ in range(20):
            execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 200)

    def test_brake(self):
        # 시동 켜고 가속 후 감속 테스트
        execute_command_callback("ENGINE_BTN", self.car_controller)  # 엔진 켬
        execute_command_callback("ACCELERATE", self.car_controller)  # 가속
        execute_command_callback("BRAKE", self.car_controller)  # 브레이크
        self.assertEqual(self.car_controller.get_speed(), 0)  # 속도가 0인지 확인

    def test_lock_unlock_vehicle(self):
        # 차량 잠금 및 잠금 해제 테스트
        execute_command_callback("LOCK", self.car_controller)  # 차량 잠금
        self.assertTrue(self.car_controller.get_lock_status())  # 차량이 잠겼는지 확인

        execute_command_callback("UNLOCK", self.car_controller)  # 차량 잠금 해제
        self.assertFalse(self.car_controller.get_lock_status())  # 차량이 잠금 해제되었는지 확인

    def test_door_lock_unlock(self):
        # 차량 전체 잠금을 해제한 후 테스트
        execute_command_callback("UNLOCK", self.car_controller)
    
        # 왼쪽 도어 잠금 해제
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_lock(), 'UNLOCKED')

        # 왼쪽 도어 잠금
        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_lock(), 'LOCKED')

        # 오른쪽 도어 잠금 해제
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_lock(), 'UNLOCKED')

        # 오른쪽 도어 잠금
        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_lock(), 'LOCKED')


    def test_door_open_close(self):
        # 차량 잠금 해제 후 문 열고 닫기
        execute_command_callback("UNLOCK", self.car_controller)

        # 왼쪽 문 열기/닫기
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")

        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

        # 오른쪽 문 열기/닫기
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")

        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

    def test_trunk_open_close(self):
        # 트렁크 열기/닫기 테스트
        execute_command_callback("UNLOCK", self.car_controller)

        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertFalse(self.car_controller.get_trunk_status())  # 트렁크가 열렸는지 확인

        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertTrue(self.car_controller.get_trunk_status())  # 트렁크가 닫혔는지 확인

    def test_sos(self):
        # 긴급 상황 테스트
        execute_command_callback("ENGINE_BTN", self.car_controller)  # 엔진 켬
        execute_command_callback("ACCELERATE", self.car_controller)  # 가속

        execute_command_callback("SOS", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 0)  # 차량 정지
        self.assertEqual(self.car_controller.get_left_door_lock(), 'UNLOCKED')
        self.assertEqual(self.car_controller.get_right_door_lock(), 'UNLOCKED')
        self.assertFalse(self.car_controller.get_trunk_status())  # 트렁크가 열렸는지 확인 


if __name__ == "__main__":
    unittest.main()
