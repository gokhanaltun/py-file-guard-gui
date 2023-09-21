from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from Ui.PfgDesign import Ui_MainWindow
from Enc import aes256, sha256
from Os import fileOs


class PfgWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_ui()

        self.file_paths = []
        self.output_folder = ""
        self.mode = "Encrypt"

    def init_ui(self):
        self.ui.modeBox.currentTextChanged.connect(self.update_ui)
        self.ui.btnSelectFile.clicked.connect(self.open_file_dialog)
        self.ui.btnSelectFolder.clicked.connect(self.open_folder_dialog)
        self.ui.btnEncDec.clicked.connect(self.check_requirements_and_continue)

    def update_ui(self):
        mode = self.ui.modeBox.currentText()
        self.mode = mode
        self.ui.btnEncDec.setText(mode)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.FileMode = QFileDialog.ExistingFiles

        files, _ = file_dialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")

        if files:
            self.file_paths = files
            self.ui.txtLog.append("\nSelected Files:\n")

            for file in files:
                self.ui.txtLog.append("- " + file)

    def open_folder_dialog(self):
        folder_dialog = QFileDialog()
        folder_dialog.FileMode = QFileDialog.DirectoryOnly

        path = folder_dialog.getExistingDirectory(caption="Select Output Path")

        if path:
            self.output_folder = path
            self.ui.txtLog.append("\n Output Folder: " + path + "\n")

    def check_requirements_and_continue(self):
        if not any(self.file_paths):
            QMessageBox.warning(self, "Warning", "Please Select Files", QMessageBox.Ok)
            return

        if self.ui.inputKey.text() == "":
            QMessageBox.warning(self, "Warning", "Please Enter Your Key", QMessageBox.Ok)
            return

        if self.output_folder == "":
            reply = QMessageBox.warning(self, 'Warning', 'No output path selected, files will be overwritten. Do you confirm?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.No:
                QMessageBox.warning(self, "Warning", "Please Choose Output Path", QMessageBox.Ok)
                return

        if self.mode == "Encrypt":
            self.encrypt_files()

        elif self.mode == "Decrypt":
            self.decrypt_files()

    def encrypt_files(self):
        for file in self.file_paths:

            file_bytes = fileOs.file_read_bytes(file)
            if file_bytes.data is None:
                self.ui.txtLog.append(f"\nfile read error: {file_bytes.error} {file}")
            else:
                hashed_password = sha256.hash_data(self.ui.inputKey.text().encode("utf-8"))

                encrypted_data = aes256.encrypt(hashed_password, file_bytes.data)
                if encrypted_data.data is None:
                    self.ui.txtLog.append(f"\nencrypt error: {encrypted_data.error} {file}")
                else:
                    target_file_path = self.output_folder + "/" + file.split("/")[-1] if self.output_folder != "" else file
                    result = fileOs.file_write_bytes(encrypted_data.data, target_file_path)

                    if result.error:
                        self.ui.txtLog.append(f"\nfile write error: {result.error} {target_file_path}")

        self.ui.txtLog.append("\ncomplete\n")

    def decrypt_files(self):
        for file in self.file_paths:

            file_bytes = fileOs.file_read_bytes(file)
            if file_bytes.data is None:
                self.ui.txtLog.append(f"\nfile read error: {file_bytes.error} {file}")
            else:
                hashed_password = sha256.hash_data(self.ui.inputKey.text().encode("utf-8"))

                decrypted_data = aes256.decrypt(hashed_password, file_bytes.data)
                if decrypted_data.data is None:
                    self.ui.txtLog.append(f"\ndecrypt error: {decrypted_data.error} {file}")
                else:
                    target_file_path = self.output_folder + "/" + file.split("/")[-1] if self.output_folder != "" else file
                    result = fileOs.file_write_bytes(decrypted_data.data, target_file_path)

                    if result.error:
                        self.ui.txtLog.append(f"\nfile write error: {result.error} {target_file_path}")

        self.ui.txtLog.append("\ncomplete\n")


def main():
    app = QApplication([])
    window = PfgWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
