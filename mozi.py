class DH_Endpoint(object):
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None
    def generate_partial_key(self):
        partial_key = self.public_key1**self.private_key
        partial_key = partial_key%self.public_key2
        return partial_key
    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r**self.private_key
        full_key = full_key%self.public_key2
        self.full_key = full_key
        return full_key
    def encrypt_message(self, message):
        encrypted_message = ""
        key = self.full_key
        for c in message:
            encrypted_message += chr(ord(c)+key)
        return encrypted_message
    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c)-key)
        return decrypted_message



print ("Персонажи Bob и Patrick передают друг другу зашифрованные сообщения")

print ("Bob генерирует открытый и закрытый ключ")
Bob_pubkey = int(input())
Bob_privkey = int(input())

print ("Patrick генерирует открытый и закрытый ключ")
Patrick_pubkey = int(input())
Patrick_privkey = int(input())

Bob = DH_Endpoint(Bob_pubkey,Patrick_pubkey,Bob_privkey)
Patrick = DH_Endpoint(Bob_pubkey,Patrick_pubkey,Patrick_privkey)

Bob_partkey = Bob.generate_partial_key()
Patrick_partkey = Patrick.generate_partial_key()

Bob_fullkey = Bob.generate_full_key(Patrick_partkey)
Patrick_fullkey = Patrick.generate_full_key(Bob_partkey)

print ("Bob и Patrick имеют закрытые ключи, которые совпадают\n", Bob_fullkey, " = ", Patrick_fullkey)

print("Используя ключ Bob шифрует сообщение")
msg=input()
encrypted=Bob.encrypt_message(msg)

print("По каналу идёт сообщение: ", encrypted)

print("Patrick получает его и дешифрует")
dmsg=Patrick.decrypt_message(encrypted)
print("Боб пишет: ", dmsg)

print("Однако им смог помешать Squidward, оказавшись посередине" )
Squidward_pubkey = int(input())
Squidward_privkey = int(input())


Patrick = DH_Endpoint(Squidward_pubkey,Patrick_pubkey,Patrick_privkey)# Сквидвард имеет ключи Боба и Патрика
BobS = DH_Endpoint(Squidward_pubkey,Patrick_pubkey,Squidward_privkey) # Комбинирует со своими 

Bob = DH_Endpoint(Bob_pubkey,Squidward_pubkey,Bob_privkey)            # Подменяет им свои ключи
PatrickS = DH_Endpoint(Bob_pubkey,Squidward_pubkey,Squidward_privkey)

BobS_partkey = BobS.generate_partial_key()
PatrickS_partkey = PatrickS.generate_partial_key()

Bob_partkey = Bob.generate_partial_key()
Patrick_partkey = Patrick.generate_partial_key()


Bob_fullkey = Bob.generate_full_key(PatrickS_partkey)   
PatrickS_fullkey = PatrickS.generate_full_key(Bob_partkey)

BobS_fullkey = BobS.generate_full_key(Patrick_partkey)
Patrick_fullkey = Patrick.generate_full_key(BobS_partkey)

print("Теперь он имел один ключ с Бобом\n", Bob_fullkey," = ",PatrickS_fullkey)
print("И с Патриком\n", BobS_fullkey," = ",Patrick_fullkey )

print("Когда Patrick пишет")
msg=input()
encrypted=Patrick.encrypt_message(msg)

print("Squidward принимает его: ", encrypted)

print("И дешефрует")
dmsg=BobS.decrypt_message(encrypted)
print("Патрик пишет: ",dmsg)

print("Затем переписывает его")
msg=input()
encrypted=PatrickS.encrypt_message(msg)

print("И отправляет Бобу: ", encrypted)

print("И наконец наслаждается покоем")
dmsg=Bob.decrypt_message(encrypted)
print("Патрик пишет: ",dmsg)