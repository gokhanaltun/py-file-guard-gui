from rx.subject import Subject

from Enc import aes256, sha256
from Os import fileOs


class PfgController:
    def __init__(self):
        self.log = Subject()

    def get_log_observable(self):
        return self.log

    def encrypt_files(self, file_paths, key, output_folder=""):
        for file in file_paths:

            file_bytes = fileOs.file_read_bytes(file)
            if file_bytes.data is None:
                self.log.on_next(f"\nfile read error: {file_bytes.error} {file}")
            else:
                hashed_password = sha256.hash_data(key)

                encrypted_data = aes256.encrypt(hashed_password, file_bytes.data)
                if encrypted_data.data is None:
                    self.log.on_next(f"\nencrypt error: {encrypted_data.error} {file}")
                else:
                    target_file_path = output_folder + "/" + file.split("/")[
                        -1] if output_folder != "" else file
                    result = fileOs.file_write_bytes(encrypted_data.data, target_file_path)

                    if result.error:
                        self.log.on_next(f"\nfile write error: {result.error} {target_file_path}")

        self.log.on_next("complete")

    def decrypt_files(self, file_paths, key, output_folder):
        for file in file_paths:

            file_bytes = fileOs.file_read_bytes(file)
            if file_bytes.data is None:
                self.log.on_next(f"\nfile read error: {file_bytes.error} {file}")
            else:
                hashed_password = sha256.hash_data(key)

                decrypted_data = aes256.decrypt(hashed_password, file_bytes.data)
                if decrypted_data.data is None:
                    self.log.on_next(f"\ndecrypt error: {decrypted_data.error} {file}")
                else:
                    target_file_path = output_folder + "/" + file.split("/")[
                        -1] if output_folder != "" else file
                    result = fileOs.file_write_bytes(decrypted_data.data, target_file_path)

                    if result.error:
                        self.log.on_next(f"\nfile write error: {result.error} {target_file_path}")

        self.log.on_next("complete")
