
from time import sleep
import pyautogui
import keyboard
import threading
import sys
import pickle
import os

coordinates_accept = []
coordinates_finish = []

exit_flag = False
sleepTime = 0
pauseBeforeOk = 0.15
key_control ='Insert'
key_complete ='Page_Down'
key_accept ='Page_Up'

class Coordinates:
 
    def __init__(self, x, y):
        self.x = x    
        self.y = y       
        
def Save():
    global coordinates_accept
    global coordinates_finish
    with open('coordinates_accept.pkl', 'wb') as f:
        pickle.dump(coordinates_accept, f)

    with open('coordinates_finish.pkl', 'wb') as f:
        pickle.dump(coordinates_finish, f)


def Load():
    global coordinates_accept
    global coordinates_finish
    with open('coordinates_accept.pkl', 'rb') as f:
        coordinates_accept = pickle.load(f)

    with open('coordinates_finish.pkl', 'rb') as f:
        coordinates_finish = pickle.load(f)

def EraseSaves():
    global coordinates_accept
    global coordinates_finish
    while True:
        keyboard.wait('Delete')
        keyboard.block_key(key_complete)
        keyboard.block_key(key_accept)
        coordinates_accept.clear()
        coordinates_finish.clear()
        try:
            os.remove('coordinates_accept.pkl')
            os.remove('coordinates_finish.pkl')
            print("Файлы сохранения успешно удалены.")
        except FileNotFoundError:
            print("Файлы сохранения не найдены.")
        print(f"Примите любой контракт, используя кнопку  {key_control} вместо мышки")
        for pointName in 'Принять', 'Да':
            coordinates_accept.append(RecordCoordinates(pointName))
        print("Переключитесь на вкладку Принятые контракты щелчком мыши и выберете любой контракт, который можете завершить")
        print(f"Завершите этот контракт, используя клавишу {key_control} вместо мышки")
        for pointName in 'Завершить', 'Инвертарь персонажа', 'Название вашего корабля', 'Принять', 'Ок':
            coordinates_finish.append(RecordCoordinates(pointName))
        Save()
        print(f"")
        print(f"===============================================")
        print(f"Координаты успешно перезаписаны")
        print(f"===============================================")
        print(f"")
        keyboard.unblock_key(key_complete)
        keyboard.unblock_key(key_accept)
   

    
        
def RecordCoordinates(pointName):
    print(f"Наведите курсор мыши на кнопку {pointName} и нажмите {key_control} для записи ее координат...")
    keyboard.wait(key_control)
    coords = pyautogui.position()
    coordinate = Coordinates(coords.x, coords.y)
    pyautogui.mouseDown()
    sleep(sleepTime)
    pyautogui.mouseUp()
    print(f"{pointName}: ({coordinate.x}, {coordinate.y})")
    sleep(sleepTime)
    return coordinate
 
        
def ContactsFinishing(coordinateList:list):
    while True:
        keyboard.wait(key_complete)
        for (index, element) in enumerate(coordinateList):
            if index == 4:
                break
            pyautogui.moveTo(element.x, element.y)
            pyautogui.mouseDown()
            sleep(sleepTime)
            pyautogui.mouseUp()
        pyautogui.moveTo(coordinateList[4].x, coordinateList[4].y)
        sleep(pauseBeforeOk)
        pyautogui.mouseDown()
        sleep(sleepTime)
        pyautogui.mouseUp()

    
def ContractsAccepting(coordinateList:list):
    while True:
        keyboard.wait(key_accept)
        pyautogui.moveTo(coordinateList[0].x, coordinateList[0].y)
        pyautogui.mouseDown()
        sleep(sleepTime)
        pyautogui.mouseUp()
        pyautogui.moveTo(coordinateList[1].x, coordinateList[1].y)
        sleep(pauseBeforeOk)
        pyautogui.mouseDown()
        sleep(sleepTime)
        pyautogui.mouseUp()
  
def main():
    global coordinates_accept
    global coordinates_finish
    accept_file_exists = os.path.isfile('coordinates_accept.pkl')
    finish_file_exists = os.path.isfile('coordinates_finish.pkl')
    if accept_file_exists and finish_file_exists:
        print("Найдено сохранение координат.")
        Load()
    else:
        print("Следуйте указаниям для записи координат.")
        print(f"Примите любой контракт, используя кнопку {key_control} вместо мышки ")
        for pointName in 'Принять', 'Да':
            coordinates_accept.append(RecordCoordinates(pointName))
        print("Переключитесь на вкладку Принятые контракты щелчком мыши и выберете любой контракт, который можете завершить")
        print(f"Завершите этот контракт, используя клавишу {key_control} вместо мышки")
        for pointName in 'Завершить', 'Инвертарь персонажа', 'Название вашего корабля', 'Принять', 'Ок':
            coordinates_finish.append(RecordCoordinates(pointName))
        Save()
        print(f"")
        print(f" Координаты записаны и сохранены в папке .exe файла.")
        print(f"")

    thread_Accepting = threading.Thread(target = ContractsAccepting, args = (coordinates_accept,))
    thread_Accepting.start()
    thread_Finishing = threading.Thread(target = ContactsFinishing, args = (coordinates_finish,))
    thread_Finishing.start()
    thread_Erasing = threading.Thread(target = EraseSaves)
    thread_Erasing.start()
    print(f"")
    print(f"==================Управление==================")
    print(f"{key_accept} - Макрос примет контракт.")
    print(f"{key_complete} - Завершит контракт.")
    print(f"Delete - Удалит сохраненные координаты и запишет новые.")
    print(f"===============================================")
    print(f"")

    keyboard.wait()

if __name__ == "__main__":
    main()
        



