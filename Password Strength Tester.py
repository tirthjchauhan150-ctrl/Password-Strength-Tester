import customtkinter as ctk
import tkinter as tk
import re
import random
import string
import math
from tkinter import messagebox

# ---------------- Password Strength Logic ----------------
def password_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Include numbers.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("Include special characters (!@#$%^&*).")

    weak_list = ["123456", "password", "qwerty", "abc123"]
    if password.lower() in weak_list:
        suggestions.append("Avoid common passwords.")

    if score <= 2:
        strength = "Weak"
        color = "red"
        bg_color = "#1a1a1a"
        emoji = "😢"
        msg = "⚠️ Hackers will love this password."
    elif score == 3 or score == 4:
        strength = "Medium"
        color = "orange"
        bg_color = "#333333"
        emoji = "😐"
        msg = "🙂 Getting better, keep going."
    else:
        strength = "Strong"
        color = "green"
        bg_color = "#000000"
        emoji = "😎"
        msg = "💪 Your password is a fortress!"

    return strength, suggestions, color, score, bg_color, emoji, msg

# ---------------- Entropy Calculation ----------------
def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[!@#$%^&*]", password): charset += 8
    if charset == 0: return 0
    entropy = math.log2(charset) * len(password)
    return round(entropy, 2)

# ---------------- Breach Checker ----------------
def check_breach(password):
    breached = ["123456", "password", "qwerty", "abc123", "letmein"]
    return password.lower() in breached

# ---------------- Update UI ----------------
def update_password(event=None):
    pwd = entry.get()
    strength, tips, color, score, bg_color, emoji, msg = password_strength(pwd)

    result_label.configure(text=f"Strength: {strength} {emoji}", text_color=color)
    message_label.configure(text=msg, text_color=color)

    suggestions_text.configure(state="normal")
    suggestions_text.delete("1.0", "end")
    if tips:
        for tip in tips:
            suggestions_text.insert("end", f"• {tip}\n")
    else:
        suggestions_text.insert("end", "No suggestions 🎉")
    suggestions_text.configure(state="disabled")

    score_label.configure(text=f"Score: {score}/5", text_color=color)
    
    if not pwd:              # agar password khali hai
        progress.set(0.0)    # 0% fill
        
    elif strength == "Weak":
        progress.set(0.3)    # 30% fill
    elif strength == "Medium":
        progress.set(0.6)    # 60% fill
    else:  # Strong
        progress.set(1.0)    # 100% fill


    entropy = calculate_entropy(pwd)
    entropy_label.configure(text=f"Entropy: {entropy} bits", text_color=color)

    if check_breach(pwd):
        breach_label.configure(text="⚠️ This password has been leaked before!", text_color="red")
    else:
        breach_label.configure(text="✅ Not found in known breaches", text_color="green")

    root.configure(fg_color=bg_color)

# ---------------- Extra Features ----------------
def toggle_password():
    if entry.cget("show") == "*":
        entry.configure(show="")
        toggle_button.configure(text="🙈 Hide Password")
    else:
        entry.configure(show="*")
        toggle_button.configure(text="👁 Show Password")

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choice(chars) for _ in range(12))
    entry.delete(0, "end")
    entry.insert(0, password)
    update_password()

def copy_password():
    root.clipboard_clear()
    root.clipboard_append(entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def toggle_theme():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        root.configure(fg_color="#f0f0f0")
        for lbl in [title_label, entry_label, result_label, message_label,
                    score_label, entropy_label, breach_label]:
            lbl.configure(text_color="black")
        suggestions_text.configure(text_color="black", fg_color="white")
        progress.configure(progress_color="blue")
    else:
        ctk.set_appearance_mode("Dark")
        root.configure(fg_color="#000000")
        for lbl in [title_label, entry_label, result_label, message_label,
                    score_label, entropy_label, breach_label]:
            lbl.configure(text_color="white")
        suggestions_text.configure(text_color="white", fg_color="#1a1a1a")
        progress.configure(progress_color="green")

def show_tips():
    messagebox.showinfo("Password Tips",
                        "🔑 Best Practices:\n\n"
                        "✔ Don’t reuse passwords\n"
                        "✔ Use a password manager\n"
                        "✔ Enable Two-Factor Authentication\n"
                        "✔ Avoid dictionary words\n"
                        "✔ Change passwords regularly")

def show_about():
    messagebox.showinfo("About Password Strength Tester",
                        "🔐 Password Strength Tester\n\n"
                        "Unique Features:\n"
                        "✔ Strength & Suggestions\n"
                        "✔ Entropy Meter\n"
                        "✔ Breach Checker\n"
                        "✔ Password Generator\n"
                        "✔ Copy to Clipboard\n"
                        "✔ Dark/Light Mode Toggle\n"
                        "✔ Motivational Messages\n\n"
                        "Made with ❤️ in Python Tkinter.")

# ---------------- UI Setup ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🔐 Password Strength Tester")
root.geometry("650x650")  # slightly taller window

# Menu bar
menubar = tk.Menu(root)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
help_menu.add_command(label="Tips", command=show_tips)
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)

title_label = ctk.CTkLabel(root, text="🔐 Password Strength Tester",font=("Helvetica", 20, "bold"))
title_label.pack(pady=20)

entry_label = ctk.CTkLabel(root, text="Enter Password:",font=("Arial", 13, "bold"))
entry_label.pack()

entry = ctk.CTkEntry(root, show="*", width=300, font=("Arial", 13))
entry.pack(pady=10)

toggle_button = ctk.CTkButton(root, text="👁 Show Password",command=toggle_password,font=("Arial", 11, "bold"))
toggle_button.pack(pady=5)

generate_button = ctk.CTkButton(root, text="🎲 Generate Password",
                                command=generate_password,
                                font=("Arial", 11, "bold"))
generate_button.pack(pady=5)

copy_button = ctk.CTkButton(root, text="📋 Copy Password",
                            command=copy_password,
                            font=("Arial", 11, "bold"))
copy_button.pack(pady=5)

theme_button = ctk.CTkButton(root, text="🌓 Toggle Theme",command=toggle_theme,font=("Arial", 11, "bold"))
theme_button.pack(pady=5)

entry.bind("<KeyRelease>", update_password)

result_label = ctk.CTkLabel(root, text="", font=("Arial", 15, "bold"))
result_label.pack(pady=15)

message_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
message_label.pack()

progress_frame = ctk.CTkFrame(root)
progress_frame.pack(pady=10, fill="x")

progress = ctk.CTkProgressBar(progress_frame, width=350)
progress.pack(pady=10)
progress.set(0)

score_label = ctk.CTkLabel(progress_frame, text="", font=("Arial", 12, "bold"))
score_label.pack()

entropy_label = ctk.CTkLabel(progress_frame, text="", font=("Arial", 12))
entropy_label.pack()

breach_label = ctk.CTkLabel(progress_frame, text="", font=("Arial", 12))
breach_label.pack()

# Suggestions box (BIGGER now)
suggestions_frame = ctk.CTkFrame(root)
suggestions_frame.pack(pady=15, fill="both", expand=True)

suggestions_text = ctk.CTkTextbox(
    suggestions_frame,
    wrap="word",
    font=("Arial", 12),
    width=600,
    height=150
)
suggestions_text.pack(padx=10, pady=10, fill="both", expand=True)
suggestions_text.configure(state="disabled")

# ---------------- Run App ----------------
root.mainloop()
