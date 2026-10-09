import joblib

data = joblib.load("water_potability_model.pkl")

print("TYPE:")
print(type(data))

print("\nCONTENT:")

if isinstance(data, dict):

    for key, value in data.items():

        print("\nKEY:", key)
        print("TYPE:", type(value))

        if hasattr(value, "predict"):
            print("HAS predict: YES")
        else:
            print("HAS predict: NO")

        if hasattr(value, "predict_proba"):
            print("HAS predict_proba: YES")
        else:
            print("HAS predict_proba: NO")

else:

    print(data)

    print("\nHAS predict:",
          hasattr(data, "predict"))

    print("HAS predict_proba:",
          hasattr(data, "predict_proba"))