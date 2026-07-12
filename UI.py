import customtkinter as ctk
from tkinter import messagebox
import pandas as pd

from risk_classifier import questions, evaluate

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

RESULT_FILE = r"C:\Users\dviro\Downloads\school\תואר ראשון\שנה ג\Theory_Of_Data_Science\Theory-Of-Data-Science\lstm\Oil_lstm_predictions.csv"

CLASSIFICATION_FILE = r"C:\Users\dviro\Downloads\school\תואר ראשון\שנה ג\Theory_Of_Data_Science\Theory-Of-Data-Science\final_stock_classification.csv"


class RiskApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("AI Stock Recommendation")
        self.geometry("1200x750")

        self.current_question = 0
        self.answers = []

        self.selected = ctk.IntVar(value=-1)

        self.build_question_screen()

    ##########################################################

    def clear(self):

        for w in self.winfo_children():
            w.destroy()

    ##########################################################

    def build_question_screen(self):


        self.clear()

        self.progress = ctk.CTkLabel(
            self,
            font=("Arial",22,"bold")
        )

        self.progress.pack(pady=20)

        self.question = ctk.CTkLabel(
            self,
            wraplength=1000,
            justify="left",
            font=("Arial",24,"bold")
        )

        self.question.pack(pady=20)

        self.answer_frame = ctk.CTkFrame(self)

        self.answer_frame.pack(
            fill="both",
            expand=True,
            padx=30
        )

        # self.next_button = ctk.CTkButton(

        #     self,

        #     text="Next",

        #     width=180,

        #     height=45,

        #     command=self.next_question

        # )

        # self.next_button.pack(pady=25)

        self.load_question()

    def load_question(self):

        self.selected.set(-1)

        q = questions[self.current_question]

        self.progress.configure(
            text=f"Question {self.current_question + 1} / {len(questions)}"
        )

        self.question.configure(text=q["question"])

        for widget in self.answer_frame.winfo_children():
            widget.destroy()

        for i, answer in enumerate(q["answers"]):

            # radio = ctk.CTkRadioButton(
            #     self.answer_frame,
            #     text=answer,
            #     value=i,
            #     variable=self.selected,
            #     font=("Arial", 18)
            # )
            radio = ctk.CTkRadioButton(
                self.answer_frame,
                text=answer,
                value=i,
                variable=self.selected,
                font=("Arial",18),
                command=self.answer_selected
            )

            radio.pack(anchor="w", pady=10, padx=20)

    ##########################################################
    def answer_selected(self):

        self.answers.append(self.selected.get())

        self.current_question += 1

        if self.current_question >= len(questions):

            score, profile = evaluate(self.answers)

            self.show_results(score, profile)

        else:

            self.load_question()


    def next_question(self):

        if self.selected.get() == -1:
            messagebox.showwarning(
                "Missing Answer",
                "Please choose one answer."
            )
            return

        self.answers.append(self.selected.get())

        self.current_question += 1

        if self.current_question >= len(questions):

            score, profile = evaluate(self.answers)

            self.show_results(score, profile)

            return

        self.load_question()


    ##########################################################

    def profile_to_class(self, profile):

        if profile == "Risk Averse":
            return 0

        elif profile == "Risk Neutral":
            return 1

        else:  # Risk Seeking
            return 2

    ##########################################################

    def load_stock_data(self, profile):

        user_class = self.profile_to_class(profile)

        classification_df = pd.read_csv(CLASSIFICATION_FILE)

        prediction_df = pd.read_csv(RESULT_FILE)

        prediction_df["Date"] = pd.to_datetime(prediction_df["Date"])

        prediction_df = prediction_df.sort_values("Date")

        last_prediction = (
            prediction_df
            .groupby("Stock")
            .last()
            .reset_index()
        )

        merged = last_prediction.merge(
            classification_df,
            left_on="Stock",
            right_on="Name"
        )

        print("After merge:", len(merged))
        print(merged.head())
        print(merged["Classification"].value_counts())

        merged = merged[
            merged["Classification"] == user_class
        ].copy()
        print("After filter:", len(merged))
        print(merged.head())
        merged["Prediction"] = merged["Pred"].map({
            1: "UP",
            0: "DOWN"
        })

        merged["Confidence"] = merged.apply(
            lambda row: row["Prob"] if row["Pred"] == 1 else 1 - row["Prob"],
            axis=1
        )

        merged["Confidence"] = (merged["Confidence"] * 100).round(2)

        merged = merged.sort_values(
            "Confidence",
            ascending=False
        )
        print("User class:", user_class)
        print(classification_df.head())
        print(prediction_df.head())
        return merged[
            [
                "Stock",
                "Date",
                "Prediction",
                "Confidence"
            ]
        ]

    ##########################################################

    def show_results(self, score, profile):

        self.clear()

        data = self.load_stock_data(profile)

        title = ctk.CTkLabel(
            self,
            text="AI Stock Recommendations",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(20, 10))

        info = ctk.CTkLabel(
            self,
            text=f"Profile: {profile}    |    Score: {score}",
            font=("Arial", 20)
        )
        info.pack(pady=(0, 20))

        table = ctk.CTkScrollableFrame(
            self,
            width=1100,
            height=500
        )
        table.pack(fill="both", expand=True, padx=20, pady=20)

        headers = [
            "Ticker",
            "Prediction",
            "Confidence",
            "Last Date"
        ]

        for col, text in enumerate(headers):

            lbl = ctk.CTkLabel(
                table,
                text=text,
                font=("Arial", 18, "bold")
            )

            lbl.grid(
                row=0,
                column=col,
                padx=25,
                pady=10,
                sticky="w"
            )

        for row, (_, stock) in enumerate(data.iterrows(), start=1):

            prediction = stock["Prediction"]

            if prediction == "UP":
                color = "#00cc66"
                prediction_text = "🟢 UP"
            else:
                color = "#ff4d4d"
                prediction_text = "🔴 DOWN"

            ctk.CTkLabel(
                table,
                text=stock["Stock"],
                text_color=color,
                font=("Arial", 16, "bold")
            ).grid(row=row, column=0, padx=20, pady=6, sticky="w")

            ctk.CTkLabel(
                table,
                text=prediction_text,
                text_color=color,
                font=("Arial", 16)
            ).grid(row=row, column=1, padx=20, pady=6, sticky="w")

            ctk.CTkLabel(
                table,
                text=f"{stock['Confidence']:.2f}%",
                font=("Arial", 16)
            ).grid(row=row, column=2, padx=20, pady=6, sticky="w")

            ctk.CTkLabel(
                table,
                text=stock["Date"].strftime("%Y-%m-%d"),
                font=("Arial", 16)
            ).grid(row=row, column=3, padx=20, pady=6, sticky="w")
        note = ctk.CTkLabel(
            self,
            text=(
                "Note:\n"
                "Since our dataset ends on 2018-02-06, we assume that today is 2018-02-06.\n"
                "Therefore, the recommendations below are based on the model's prediction "
                "for the last available trading day in the dataset."
            ),
            font=("Arial", 15),
            justify="left",
            wraplength=1000,
            text_color="lightgray"
        )

        note.pack(pady=(0, 20))
        close_btn = ctk.CTkButton(
            self,
            text="Close",
            width=180,
            command=self.destroy
        )
        close_btn.pack(pady=20)
##########################################################

    def answer_selected(self):

        if self.selected.get() == -1:
            return

        self.answers.append(self.selected.get())

        self.current_question += 1

        if self.current_question >= len(questions):

            score, profile = evaluate(self.answers)

            self.show_results(score, profile)

        else:

            self.load_question()
    # def refresh_table(self):

    #     profile = self.profile_var.get()

    #     data = self.load_stock_data(profile)

    #     # מנקה את הטבלה הישנה
    #     # ובונה אותה מחדש

app = RiskApp()
app.mainloop()