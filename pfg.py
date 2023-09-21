from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from Controller.pfg_controller import PfgController
from Ui.PfgDesign import Ui_MainWindow


class PfgWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_ui()

        self.controller = PfgController()
        self.observe_controller()

        self.file_paths = []
        self.output_folder = ""
        self.mode = "Encrypt"
        self.key = ""

    def init_ui(self):
        self.ui.modeBox.currentTextChanged.connect(self.update_ui)
        self.ui.btnSelectFile.clicked.connect(self.open_file_dialog)
        self.ui.btnSelectFolder.clicked.connect(self.open_folder_dialog)
        self.ui.btnEncDec.clicked.connect(self.check_requirements_and_continue)

    def update_ui(self):
        mode = self.ui.modeBox.currentText()
        self.mode = mode
        self.ui.btnEncDec.setText(mode)

    def observe_controller(self):
        self.controller.get_log_observable().subscribe(
            on_next=lambda log_data: self.on_next(log_data))

    def on_next(self, log_data: str):
        if log_data == "complete":
            self.on_complete()
        else:
            self.print_log(log_data)

    def print_log(self, data: str):
        self.ui.txtLog.append(data)

    def on_complete(self):
        self.file_paths = []
        self.output_folder = ""
        self.key = ""
        self.mode = "Encrypt"
        self.ui.modeBox.setCurrentIndex(0)
        self.ui.inputKey.setText("")
        self.print_log("\ncomplete\n")

    def display_warning_message(self, message: str):
        QMessageBox.warning(self, "Warning", message, QMessageBox.Ok)

    def display_warning_message_with_yes_no(self, message: str):
        reply = QMessageBox.warning(self, 'Warning', message,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.FileMode = QFileDialog.ExistingFiles

        files, _ = file_dialog.getOpenFileNames(self,
                                                "Select Files", "", "All Files (*)")

        if files:
            self.file_paths = files
            self.print_log("\nSelected Files:\n")

            for file in files:
                self.print_log("- " + file)

    def open_folder_dialog(self):
        folder_dialog = QFileDialog()
        folder_dialog.FileMode = QFileDialog.DirectoryOnly

        path = folder_dialog.getExistingDirectory(caption="Select Output Path")

        if path:
            self.output_folder = path
            self.print_log("\n Output Folder: " + path + "\n")

    def check_requirements_and_continue(self):
        if not any(self.file_paths):
            self.display_warning_message("Please Select Files")
            return

        if self.ui.inputKey.text() == "":
            self.display_warning_message("Please Enter Your Key")
            return
        else:
            self.key = self.ui.inputKey.text().encode("utf-8")

        if self.output_folder == "":
            reply = self.display_warning_message_with_yes_no(
                'No output path selected, files will be overwritten. Do you confirm?')

            if reply == QMessageBox.No:
                self.display_warning_message("Please Choose Output Path")
                return

        if self.mode == "Encrypt":
            self.controller.encrypt_files(self.file_paths, self.key, self.output_folder)

        elif self.mode == "Decrypt":
            self.controller.decrypt_files(self.file_paths, self.key, self.output_folder)


def main():
    app = QApplication([])
    window = PfgWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
