from Enc import aes256, sha256
from Os import fileOs


def encrypt_files():
    for file in self.file_paths:

        file_bytes = fileOs.file_read_bytes(file)
        if file_bytes.data is None:
            print("file read error: ", file_bytes.error, " ", file)
        else:
            hashed_password = sha256.hash_data(self.ui.inputKey.text().encode("utf-8"))

            encrypted_data = aes256.encrypt(hashed_password, file_bytes.data)
            if encrypted_data.data is None:
                print("Encrypt error: ", encrypted_data.error, " ", file)
            else:
                if self.output_folder == "":
                    fileOs.file_write_bytes(encrypted_data.data, file)
                else:
                    file_path = self.output_folder + "/" + file.split("/")[-1]
                    data = fileOs.file_write_bytes(encrypted_data.data, file_path)
                    if data.error:
                        print(data.error, " ", file_path)
    print("Complete")


def decrypt_files():
    for file in self.file_paths:

        file_bytes = fileOs.file_read_bytes(file)
        if file_bytes.data is None:
            print("file read error: ", file_bytes.error, " ", file)
        else:
            hashed_password = sha256.hash_data(self.ui.inputKey.text().encode("utf-8"))

            decrypted_data = aes256.decrypt(hashed_password, file_bytes.data)
            if decrypted_data.data is None:
                print("Encrypt error: ", decrypted_data.error, " ", file)
            else:
                if self.output_folder == "":
                    fileOs.file_write_bytes(decrypted_data.data, file)
                else:
                    file_path = self.output_folder + "/" + file.split("/")[-1]
                    data = fileOs.file_write_bytes(decrypted_data.data, file_path)
                    if data.error:
                        print(data.error, " ", file_path)

    print("Complete")