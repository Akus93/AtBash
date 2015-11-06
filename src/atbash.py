#!/usr/bin/python3
from gi.repository import Gtk


class MyBuilder(Gtk.Builder):


    def __init__(self):
        Gtk.Builder.__init__(self)
        self.add_from_file("ui.glade")

        handlers = {
            "encrypt": self.encrypt,
            "decrypt": self.decrypt
        }

        self.connect_signals(handlers)

        self.window = self.get_object("main_window")
        self.textview1 = self.get_object("textview1")
        self.textview2 = self.get_object("textview2")
        self.entry1 = self.get_object("entry1")
        self.statusbar1 = self.get_object("statusbar1")

        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()


    def encrypt(self, widget):
        encrypt_buffer = self.textview1.get_buffer()
        start_iter = encrypt_buffer.get_start_iter()
        end_iter = encrypt_buffer.get_end_iter()
        plain_text = encrypt_buffer.get_text(start_iter, end_iter, False)
        encrypted_text = ""
        for char in plain_text.upper():
            index = self.alphabet.find(char)
            if index >= 0:
                encrypted_text = encrypted_text + self.alphabet[::-1][index]
            else:
                encrypted_text = encrypted_text + char
        self.textview2.get_buffer().set_text(encrypted_text)


    def decrypt(self, widget):
        if not self.check_password():
            self.set_error("Incorrect password..." , "error")
        else:
            decrypt_buffer = self.textview2.get_buffer()
            start_iter = decrypt_buffer.get_start_iter()
            end_iter = decrypt_buffer.get_end_iter()
            cipher_text = decrypt_buffer.get_text(start_iter, end_iter, False)
            decrypted_text = ""
            for char in cipher_text.upper():
                index = self.alphabet[::-1].find(char)
                if index >= 0:
                    decrypted_text = decrypted_text + self.alphabet[index]
                else:
                    decrypted_text = decrypted_text + char
            self.textview1.get_buffer().set_text(decrypted_text)


    def check_password(self):
        return True if self.entry1.get_buffer().get_text() == "secret" else False


    def set_error(self, text, context):
        context_id = self.statusbar1.get_context_id(context)
        self.statusbar1.push(context_id, text)


if __name__ == "__main__":
	program = MyBuilder()
	Gtk.main()
