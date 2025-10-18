# supervisor for the interaction loop


def main():
    investigator = Investigator()
    symptoms_func = cosine_func

    while True:
        response_received = False
        while not response_received:
            try_read_response()

    
        symptoms_score = symptoms_func(response)
        investigator.update_patient_representation(symptoms_score)
        instruction =  investigator.generate_instruction()



        send_response(instruction)





if __name__ == '__main__':
    main()

    