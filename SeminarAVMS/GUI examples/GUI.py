import customtkinter

# Options: 'dark', 'light', 'System'
customtkinter.set_appearance_mode('dark')

# Options: 'green', 'blue', 'dark-blue'
customtkinter.set_default_color_theme('green') 

root = customtkinter.CTk()
root.geometry('500x500')


def login():
    print('Test login.')


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill='both', expand=True)

label = customtkinter.CTkLabel(master=frame, text='Login')
label.pack(pady = 12, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame, placeholder_text='Username')
entry_1.pack(pady=12, padx=10)

entry_2 = customtkinter.CTkEntry(master=frame, placeholder_text='Password', show='*')
entry_2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text='Remeber Me')
checkbox.pack(pady=12, padx=10)

root.mainloop()
