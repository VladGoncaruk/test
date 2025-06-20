import customtkinter as ctk
import requests

# АКТУАЛЬНИЙ API
API_URL = "https://open.er-api.com/v6/latest/USD"

def fetch_rates():
    try:
        response = requests.get(API_URL)
        data = response.json()
        return data["rates"]
    except Exception as e:
        print("Помилка при отриманні курсів:", e)
        return {}

class CurrencyConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("💱 Конвертер Валют")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.rates = fetch_rates()
        if not self.rates:
            self.rates = {"USD": 1.0, "EUR": 0.92, "UAH": 40.0}  # запасні курси

        self.currencies = list(self.rates.keys())
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Конвертер Валют", font=("Arial", 24)).pack(pady=20)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Сума", font=("Arial", 16))
        self.amount_entry.pack(pady=10)

        self.from_currency = ctk.CTkComboBox(self, values=self.currencies, font=("Arial", 14))
        self.from_currency.set("USD")
        self.from_currency.pack(pady=5)

        self.to_currency = ctk.CTkComboBox(self, values=self.currencies, font=("Arial", 14))
        self.to_currency.set("EUR")
        self.to_currency.pack(pady=5)

        self.result_label = ctk.CTkLabel(self, text="Результат: ", font=("Arial", 18))
        self.result_label.pack(pady=20)

        convert_btn = ctk.CTkButton(self, text="Конвертувати", command=self.convert)
        convert_btn.pack(pady=10)

        refresh_btn = ctk.CTkButton(self, text="🔄 Оновити курси", command=self.refresh_rates)
        refresh_btn.pack(pady=5)

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            result = amount * self.rates[to_curr] / self.rates[from_curr]
            self.result_label.configure(text=f"Результат: {result:.2f} {to_curr}")
        except Exception as e:
            self.result_label.configure(text="⚠️ Помилка! Перевірте вхідні дані.")
            print(e)

    def refresh_rates(self):
        self.rates = fetch_rates()
        self.result_label.configure(text="Курси оновлено!")

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()
