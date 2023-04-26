#An application to generate data from Aspiring Panda Pilot WHO Farming Project
import pandas as pd
import numpy as np
import random as r
from scipy import stats
from matplotlib import pyplot as plt
from MyStatsFunctions import *

def GenerateMyDataFrame(file_location, desired_size):
    # Modified the calculated rows in the DataFrame
    df = pd.read_csv(file_location)
    df["sold_ratio"] = df["qty_for_sale"]/df["qty_for_produced"]
    df["points"] = df["qty_for_sale"] * 3
    df["std_unit"] = df.apply(lambda row:
        row.qty_for_sale * 10
        if row.unit == "10Kg Boxes"
        else row.qty_for_sale * 1
        , axis=1)
    df["product_yield"] = df.apply(lambda row:
        row.product_yield * 10
        if row.unit == "10Kg Boxes"
        else row.product_yield * 1
        , axis=1)
    df["land_efficiency"] = df["std_unit"]/df["product_yield"]

    # Initialise the dictionary accounting for the variable types
    dict = {}
    columns = df.columns
    for col in columns:
        if type(df[col].values[0]) == np.int64:
            print(col, "integer", df[col].values[0])
            field = {"type": "integer", "variable": "fixed"}
        elif type(df[col].values[0]) == str:
            print(col, "string", df[col].values[0])
            field = {"type": "string", "variable": "fixed"}
        else:
            print(col, "float", df[col].values[0])
            field = {"type": "float", "variable": "fixed"}
        dict[col] = field
    print("\n")
    dict["sold_ratio"]["variable"] = "calculated"
    dict["points"]["variable"] = "calculated"
    dict["std_unit"]["variable"] = "calculated"
    dict["land_efficiency"]["variable"] = "calculated"

    # Generate data depending on the data type and whether it is variable/fixed
    generated_dict = {}
    for field in dict:
        values = df[field].values
        if dict[field]["variable"] == "fixed":
            if dict[field]["type"] == "integer":
                if field == "user_id":
                    generated_dict[field] = GenerateMyUniqueValues(desired_size, values, "constrained")
                if field == "warehouse_id" or "cproject_id":
                    generated_dict[field] = GenerateWeightedUniformDisitribution(desired_size, values, 0.2)
                if field == "qty_for_produced":
                    generated_dict[field] = GenerateNormalDistribution(desired_size, values)
                if field == "qty_for_sale":
                    generated_dict[field], generated_dict["sold_ratio"] = GenerateSoldValues(desired_size, generated_dict["qty_for_produced"])
                if field == "product_yield":
                    generated_dict[field] = GenerateEnclosedUniformDistribution(desired_size, values)
            else:
                fields_for_dummy = ["program_partner_name", "warehouse_name", "subcounty_name", "parish_name",
                                    "village_name", "supervisor_name", "product_name", "program_name",
                                    "community_project_name", "batch_number", "owner_worker_name"]
                for f in fields_for_dummy:
                    generated_dict[f] = GenerateDummyNames(desired_size, f)
                if field == "district_name":
                    additional_array = ["Dummy District 1", "Dummy District 2", "Dummy District 3"]
                    generated_dict[field] = GenerateDiscreteDistribution(desired_size, values, additional_array, None)
                if field == "unit":
                    generated_dict[field] = GenerateProportionateDisitribution(desired_size, values)

    # Assign the values for our calculated variables based on the generated data
    multiplier = [10 if "10Kg" in x else 1 for x in generated_dict["unit"]]
    generated_dict["points"] = np.array(generated_dict["qty_for_sale"]) * 3
    generated_dict["product_yield"] = np.array(generated_dict["product_yield"]) * np.array(multiplier)
    generated_dict["std_unit"] = np.array(generated_dict["qty_for_produced"]) * np.array(multiplier)
    generated_dict["land_efficiency"] = np.array(generated_dict["std_unit"]) / np.array(generated_dict["product_yield"])

    # Append generated data to original information & normalise values with land_efficiency > 1
    generated_dataFrame = pd.DataFrame(generated_dict)
    theoretical_df = df.append(generated_dataFrame, ignore_index = True)
    theoretical_df.loc[theoretical_df['land_efficiency'] >= 1, "product_yield"] = theoretical_df.loc[theoretical_df['land_efficiency'] >= 1, "qty_for_sale"]
    theoretical_df.loc[theoretical_df['land_efficiency'] >= 1, "land_efficiency"] = 1
    print(theoretical_df)
    return theoretical_df
