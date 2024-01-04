import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from tkinter import Tk, Entry, Label, Button, IntVar, Radiobutton, Scale
import os
import sys


import warnings

warnings.filterwarnings("ignore")


class Gui:
    def __init__(self, model):
        """
        creates a graphical user interface
        """

        # make the mode an attribute of the class
        self.model = model

        win = Tk()
        win.title("House price Prediction")

        # Labels
        Label(win, text="Number of bedrooms").grid(row=0, column=0, sticky="w", padx=5)
        Label(win, text="Number of bathrooms").grid(row=1, column=0, sticky="w", padx=5)
        Label(win, text="Area of house (sqft)").grid(
            row=2, column=0, sticky="w", padx=5
        )
        Label(win, text="Area of lot (sqft)").grid(row=3, column=0, sticky="w", padx=5)
        Label(win, text="Number of floors").grid(row=4, column=0, sticky="w", padx=5)
        Label(win, text="Waterfront present?").grid(row=5, column=0, sticky="w", padx=5)
        Label(win, text="'View' rated out of 4").grid(
            row=6, column=0, sticky="w", padx=5
        )
        Label(win, text="'Condition' rated out of 5").grid(
            row=7, column=0, sticky="w", padx=5
        )
        Label(win, text="Grade (King County grading system)").grid(
            row=0, column=3, sticky="w", padx=5
        )
        Label(win, text="Area of house apart from basement (sqft)").grid(
            row=1, column=3, sticky="w", padx=5
        )
        Label(win, text="Area of basement (sqft)").grid(
            row=2, column=3, sticky="w", padx=5
        )
        Label(win, text="Year built").grid(row=3, column=3, sticky="w", padx=5)
        Label(win, text="Year renovated").grid(row=4, column=3, sticky="w", padx=5)
        Label(win, text="Zipcode").grid(row=5, column=3, sticky="w", padx=5)
        Label(win, text="Latitude").grid(row=6, column=3, sticky="w", padx=5)
        Label(win, text="Longitude").grid(row=7, column=3, sticky="w", padx=5)
        Label(win, text="Area of house in 2015").grid(
            row=8, column=0, sticky="w", padx=5
        )
        Label(win, text="Area of lot in 2015").grid(row=8, column=3, sticky="w", padx=5)

        # add a spacer
        for i in range(10):
            Label(win, text=" " * 5).grid(row=i, column=2)

        # Entries
        self.bedooms = Entry(win)
        self.bathrooms = Entry(win)
        self.sqft_living = Entry(win)
        self.sqft_lot = Entry(win)
        self.floors = Entry(win)
        self.grade = Entry(win)
        self.sqft_above = Entry(win)
        self.sqft_basement = Entry(win)
        self.yr_built = Entry(win)
        self.yr_renovated = Entry(win)
        self.zipcode = Entry(win)
        self.lat = Entry(win)
        self.lon = Entry(win)
        self.sqft_living15 = Entry(win)
        self.sqft_lot15 = Entry(win)

        # Layout
        self.bedooms.grid(row=0, column=1, padx=5, pady=5)
        self.bathrooms.grid(row=1, column=1, padx=5, pady=5)
        self.sqft_living.grid(row=2, column=1, padx=5, pady=5)
        self.sqft_lot.grid(row=3, column=1, padx=5, pady=5)
        self.floors.grid(row=4, column=1, padx=5, pady=5)
        self.grade.grid(row=0, column=4, padx=5, pady=5)
        self.sqft_above.grid(row=1, column=4, padx=5, pady=5)
        self.sqft_basement.grid(row=2, column=4, padx=5, pady=5)
        self.yr_built.grid(row=3, column=4, padx=5, pady=5)
        self.yr_renovated.grid(row=4, column=4, padx=5, pady=5)
        self.zipcode.grid(row=5, column=4, padx=5, pady=5)
        self.lat.grid(row=6, column=4, padx=5, pady=5)
        self.lon.grid(row=7, column=4)
        self.sqft_living15.grid(row=8, column=1)
        self.sqft_lot15.grid(row=8, column=4)

        # the button
        Button(text=" Predict ", command=self.predict).grid(row=10, columnspan=5)

        # special button
        # waterfront radio buttons
        self.waterfront = IntVar()
        Radiobutton(win, text="Yes", variable=self.waterfront, value=1).grid(
            row=5, column=1, sticky="W"
        )
        Radiobutton(win, text="No", variable=self.waterfront, value=0).grid(
            row=5, column=1, sticky="SN"
        )

        # view scale
        self.view = IntVar()
        Scale(win, variable=self.view, from_=0, to=4, orient="horizontal").grid(
            row=6, column=1
        )

        # condition scale
        self.condition = IntVar()
        Scale(win, variable=self.condition, from_=1, to=5, orient="horizontal").grid(
            row=7, column=1
        )

        win.mainloop()

    def predict(self):
        # set the current year to 2020
        year = 2020

        # compute the bins
        x1 = []

        # convert yr_built and yr_renovated to bins
        for i, var in enumerate((self.yr_built.get(), self.yr_renovated.get())):
            var = float(var)
            bins = [0 for _ in range(8)] if i == 0 else [0 for _ in range(7)]

            if year - var < 1:
                bins[0] = 1
            elif year - var < 6:
                bins[1] = 1
            elif year - var < 11:
                bins[2] = 1
            elif year - var < 26:
                bins[3] = 1
            elif year - var < 51:
                bins[4] = 1
            elif year - var < 76:
                bins[5] = 1
            elif year - var < 101:
                bins[6] = 1
            else:
                k = 7 if i == 0 else 6
                bins[k] = 1

            x1 += bins

        # extract the data from the entries
        x0 = [
            float(self.bedooms.get()),
            float(self.bathrooms.get()),
            float(self.sqft_living.get()),
            float(self.sqft_lot.get()),
            float(self.floors.get()),
            self.waterfront.get(),
            self.view.get(),
            self.condition.get(),
            float(self.grade.get()),
            float(self.sqft_above.get()),
            float(self.sqft_basement.get()),
        ]

        x2 = [
            float(self.zipcode.get()),
            float(self.lat.get()),
            float(self.lon.get()),
            float(self.sqft_living15.get()),
            float(self.sqft_lot15.get()),
        ]

        # predict the price
        x = np.array(x0 + x1 + x2).reshape(1, -1)
        y = self.model.predict(x)

        # pop up window
        child = Tk()
        msg = f"\nPredicted price: $\n {y[0]:.2f} "
        Label(child, text=msg).grid(padx=10, pady=10)


def train():
    """returns a trained model"""
    # Get the directory where the script is located
    script_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, "kc_house_data.csv")

    print(f"Script directory: {script_dir}")
    print(f"CSV file path: {csv_file_path}")

    # Check if the CSV file exists
    if not os.path.isfile(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    print("CSV file found!")

    # Read the CSV file using the absolute path
    df = pd.read_csv(csv_file_path)
    df_dm = df.copy()

    # just take the year from the date column
    df_dm["sales_yr"] = df_dm["date"].astype(str).str[:4]

    # add the age of the buildings when the houses were sold as a new column
    df_dm["age"] = df_dm["sales_yr"].astype(int) - df_dm["yr_built"]

    # add the age of the renovation when the houses were sold as a new column
    df_dm["age_rnv"] = 0
    df_dm["age_rnv"] = (
        df_dm["sales_yr"][df_dm["yr_renovated"] != 0].astype(int)
        - df_dm["yr_renovated"][df_dm["yr_renovated"] != 0]
    )
    df_dm["age_rnv"][df_dm["age_rnv"].isnull()] = 0

    # partition the age into bins
    bins = [-2, 0, 5, 10, 25, 50, 75, 100, 100000]
    labels = ["<1", "1-5", "6-10", "11-25", "26-50", "51-75", "76-100", ">100"]
    df_dm["age_binned"] = pd.cut(df_dm["age"], bins=bins, labels=labels)

    # partition the age_rnv into bins
    bins = [-2, 0, 5, 10, 25, 50, 75, 100000]
    labels = ["<1", "1-5", "6-10", "11-25", "26-50", "51-75", ">75"]
    df_dm["age_rnv_binned"] = pd.cut(df_dm["age_rnv"], bins=bins, labels=labels)

    # transform the factor values to be able to use in the model
    df_dm = pd.get_dummies(df_dm, columns=["age_binned", "age_rnv_binned"])

    train_data_dm, test_data_dm = train_test_split(
        df_dm, train_size=0.8, random_state=0
    )

    features = [
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "sqft_lot",
        "floors",
        "waterfront",
        "view",
        "condition",
        "grade",
        "sqft_above",
        "sqft_basement",
        "age_binned_<1",
        "age_binned_1-5",
        "age_binned_6-10",
        "age_binned_11-25",
        "age_binned_26-50",
        "age_binned_51-75",
        "age_binned_76-100",
        "age_binned_>100",
        "age_rnv_binned_<1",
        "age_rnv_binned_1-5",
        "age_rnv_binned_6-10",
        "age_rnv_binned_11-25",
        "age_rnv_binned_26-50",
        "age_rnv_binned_51-75",
        "age_rnv_binned_>75",
        "zipcode",
        "lat",
        "long",
        "sqft_living15",
        "sqft_lot15",
    ]

    complex_model_4 = linear_model.LinearRegression()
    complex_model_4.fit(train_data_dm[features], train_data_dm["price"])

    return complex_model_4


if __name__ == "__main__":
    # create the model
    model = train()

    # create the gui
    Gui(model)
