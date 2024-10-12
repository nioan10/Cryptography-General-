import re
import copy

#Устанавливаем длинну регистра 19, 22, 23
reg_x_length = 19
reg_y_length = 22
reg_z_length = 23

#Инициализируем глобальные переменные
key_one = "" #ключ
reg_x = [] #списоки для хранения значений регистров x, y, z
reg_y = []
reg_z = []

def loading_registers(key): #инициализируем регистры, используя 64-битный ключ в качестве параметра
    global reg_x, reg_y, reg_z
    reg_x = [int(key[i]) for i in range(reg_x_length)]                                                            #первые 19 элементов из ключа
    reg_y = [int(key[i]) for i in range(reg_x_length, reg_x_length + reg_y_length)]                               #следующие 22 элемента из ключа
    reg_z = [int(key[i]) for i in range(reg_x_length + reg_y_length, reg_x_length + reg_y_length + reg_z_length)] #следующие 23 элемента из ключа

def set_key(key): #устанавливаем ключ и загружаем регистры, если он содержит 0 и 1 и если он состоит ровно из 64 битов
    if len(key) == 64 and re.match("^([01])+$", key):
        global key_one
        key_one = key #устанавливаем ключ в глобальной переменной
        loading_registers(key) #инициализируем регистры
        return True
    return False

def get_key(): #получаем ключ, вспомогательная функция
    return key_one

def to_binary(plain): #преобразуем текст в бинарный формат
    binary_list = []
    for char in plain:                           #проходим по всем символам
        binary_string = format(ord(char), '08b') #преобразуем символ в 8-битный бинарный формат
        for bit in binary_string: 
            int_bit = int(bit) 
            binary_list.append(int_bit) 
    return binary_list

def get_majority(x, y, z): #определяем большинство, складывая значения x, y и z и если оно больше 1 (например, две 1 и один 0), возвращаем большинство (1). В противном случае, если два 0 и один 1, большинство возвращается как 0.
    return 1 if x + y + z > 1 else 0

def shift_register(register, new_bit): #сдвигаем регистр на один бит влево и добавляем новый бит в начало
    return [new_bit] + register[:-1]

def get_keystream(length): #генерируем поток ключей
    reg_x_temp = copy.deepcopy(reg_x) #копируем значения регистров, чтобы не изменять оригинальные значения
    reg_y_temp = copy.deepcopy(reg_y) 
    reg_z_temp = copy.deepcopy(reg_z) 
    keystream = [] #список для хранения потока ключей

    for _ in range(length):                                                                 #проходим по всем битам
        majority = get_majority(reg_x_temp[8], reg_y_temp[10], reg_z_temp[10])              #определяем большинство битов
        if reg_x_temp[8] == majority:                                                       #если бит 8 регистра x равен большинству                       
            new_bit = reg_x_temp[13] ^ reg_x_temp[16] ^ reg_x_temp[17] ^ reg_x_temp[18]     #вычисляем новый бит 
            reg_x_temp = shift_register(reg_x_temp, new_bit)                                #сдвигаем регистр на один бит влево и добавляем новый бит в начало
        if reg_y_temp[10] == majority:                                                      #если бит 10 регистра y равен большинству
            new_bit = reg_y_temp[20] ^ reg_y_temp[21]                                       #вычисляем новый бит
            reg_y_temp = shift_register(reg_y_temp, new_bit)                                #сдвигаем регистр на один бит влево и добавляем новый бит в начало
        if reg_z_temp[10] == majority:                                                      #если бит 10 регистра z равен большинству                 
            new_bit = reg_z_temp[7] ^ reg_z_temp[20] ^ reg_z_temp[21] ^ reg_z_temp[22]      #вычисляем новый бит
            reg_z_temp = shift_register(reg_z_temp, new_bit)                                #сдвигаем регистр на один бит влево и добавляем новый бит в начало
        keystream.append(reg_x_temp[18] ^ reg_y_temp[21] ^ reg_z_temp[22])                  #добавляем XOR-енный бит в поток ключей

    return keystream #возвращаем поток ключей

def convert_binary_to_str(binary): #преобразуем бинарный формат в строку
	s = "" 
	length = len(binary) - 8
	i = 0
	while(i <= length):                     #проходим по всем битам
		s = s + chr(int(binary[i:i+8], 2))  #преобразуем 8 битов в символ и добавляем его к строке
		i = i + 8                           #переходим к следующим 8 битам
	return str(s)

def encrypt(plain): #Шифруем текст
	s = ""
	binary = to_binary(plain) #преобразуем текст в бинарный формат
	keystream = get_keystream(len(binary)) #генерируем поток ключей
	i = 0
	while(i < len(binary)): #XOR-им каждый бит текста с соответствующим битом потока ключей
		s = s + str(binary[i] ^ keystream[i]) 
		i = i + 1
	return s

def decrypt(cipher): #Дешифруем текст
	s = ""
	binary = [] 
	keystream = get_keystream(len(cipher)) #генерируем поток ключей
	i = 0
	while(i < len(cipher)):                     #XOR-им каждый бит текста с соответствующим битом потока ключей
		binary.insert(i,int(cipher[i]))         #преобразуем текст в бинарный формат
		s = s + str(binary[i] ^ keystream[i])   #XOR-им каждый бит текста с соответствующим битом потока ключей
		i = i + 1                               #переходим к следующему биту
	return convert_binary_to_str(str(s))

def user_input_key(): #получаем 64-битный ключ от пользователя
    while True:
        tha_key = input('Enter a 64-bit key: ')
        if len(tha_key) == 64 and re.match("^([01])+$", tha_key): #если ключ состоит ровно из 64 битов и содержит только 0 и 1
            return tha_key

def user_input_choice(): #получаем выбор от пользователя
    while True:
        choice = input('[0]: Quit\n[1]: Encrypt\n[2]: Decrypt\nPress 0, 1, or 2: ')
        if choice in {'0', '1', '2'}:
            return choice

def user_input_plaintext(): #получаем текст от пользователя
    return input('Enter text: ')

def the_main(): #основная функция
    while True:
        key = user_input_key()
        set_key(key)
        choice = user_input_choice()
        
        if choice == '0':
            print('Have an awesome day!!!')
            break
        elif choice == '1':
            plaintext = user_input_plaintext()
            encrypted_text = encrypt(plaintext)
            print(f'Encrypted text: {encrypted_text}')
        elif choice == '2':
            ciphertext = user_input_plaintext()
            decrypted_text = decrypt(ciphertext)
            print(f'Decrypted text: {decrypted_text}')

the_main()


# Пример 64-битного ключа: 0101001000011010110001110001100100101001000000110111111010110111
# Пример зашифровонного текста "hello_wold_!" :
# 11110000111011111000110111111000000110111000011001001111000001101101011110011111110010111001101010111100

#----------------------------------------------------------------------#
# Программа основана на алгоритме шифрования A5/1.

# Как работает программа:
    # 1. Пользователь вводит 64-битный ключ
    # 2. Ключ загружается в регистры x, y, z
    # 3. Пользователь выбирает, зашифровать или расшифровать текст
    # 4. Если пользователь выбирает зашифровать, он вводит текст
    # 5. Текст преобразуется в бинарный формат
    # 6. Генерируется поток ключей
    # 7. Каждый бит текста XOR-ится с соответствующим битом потока ключей
    # 8. Результат выводится на экран
    # 9. Если пользователь выбирает расшифровать, он вводит текст
    # 10. Текст преобразуется в бинарный формат
    # 11. Генерируется поток ключей
    # 12. Каждый бит текста XOR-ится с соответствующим битом потока ключей
    # 13. Результат выводится на экран
    # 14. Пользователь может повторить процесс или завершить программу
#----------------------------------------------------------------------#

