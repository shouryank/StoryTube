weathers = ["sunny", "rainy", "windy", "snowy", "night"]

def get_weather(text):

    extracted_weather = None

    # If weather occurs in the text, return it
    for weather in weathers:
        if weather in text:
            extracted_weather = weather
            break
    
    return extracted_weather

    