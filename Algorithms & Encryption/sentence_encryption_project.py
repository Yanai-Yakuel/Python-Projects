import art  # Importing the art module to use the logo

print(art.logo)  # Displaying the logo of the Caesar Cipher game

# Alphabet list to map each letter to its position
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Function to perform Caesar cipher encoding or decoding
def caesar(original_text, shift_amount, encode_or_decode):
    output_text = ""  # Initialize the variable to store the result
    if encode_or_decode == "decode":
        shift_amount *= -1  # Reverse the shift amount for decoding

    for letter in original_text:  # Loop through each character in the input text
        if letter not in alphabet:  # If the character is not in the alphabet (e.g., spaces, punctuation)
            output_text += letter  # Add it to the result without changing it
        else:
            # Calculate the new shifted position of the letter
            shifted_position = alphabet.index(letter) + shift_amount
            shifted_position %= len(alphabet)  # Ensure the position wraps around the alphabet
            output_text += alphabet[shifted_position]  # Add the shifted letter to the result
    
    print(f"Here is the {encode_or_decode}d result: {output_text}")  # Output the final result

# Main program loop for multiple runs
should_continue = True
while should_continue:
    # Get user input for encoding/decoding
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
    text = input("Type your message:\n").lower()  # Convert the message to lowercase
    shift = int(input("Type the shift number:\n"))  # Get the shift number

    # Call the caesar function to encode or decode the message
    caesar(original_text=text, shift_amount=shift, encode_or_decode=direction)

    # Ask the user if they want to continue
    restart = input("Type 'yes' if you want to go again. Otherwise, type 'no'.\n").lower()
    if restart == "no":
        should_continue = False  # Exit the loop if the user chooses not to continue
        print("Goodbye")  # Farewell message


