import os
import sys


class Util:
    @staticmethod  # type: ignore
    def print_(message):
        print(f"  {message}")

    @staticmethod  # type: ignore
    def print_with_spacing(message):
        print()
        Util.print_(message)

    @staticmethod  # type: ignore
    def input_(message):
        return input(f"  {message}")

    @staticmethod  # type: ignore
    def input_with_spacing(message):
        print()
        return Util.input_(message)

    @staticmethod  # type: ignore
    def save_temp_text(temp_text, extension):
        """
        Save intermediate result.
        """
        # Save intermediate result
        temp_filename = 'io/temp' + extension
        Util.save_to_file(temp_filename, temp_text)
        Util.print_(
            f"Intermediate result saved to {temp_filename}")

    @staticmethod  # type: ignore
    def save_output_text(output_text, extension):
        """
        Dynamically name and save final output.
        """
        output_filename = Util.generate_output_filename(extension)
        Util.save_to_file(output_filename, output_text)
        Util.print_with_spacing(f"Final output saved to {output_filename}")

    @staticmethod  # type: ignore
    def generate_output_filename(extension):
        """
        Generates a unique filename for saving the output.

        Creates a filename based on a sequential number to avoid overwriting existing files. The filename is generated in the 'io' directory with a '.md' extension.

        Returns:
            str: The generated unique output filename.
        """
        n = 1
        output_filename = f'io/output_{n}{extension}'
        while os.path.exists(output_filename):
            n += 1
            output_filename = f'io/output_{n}{extension}'
        return output_filename

    @staticmethod  # type: ignore
    def save_to_file(file_path, text):
        """
        Saves the given text to a specified file path.

        Args:
            file_path (str): The path to the file where the text will be saved.
            text (str): The text to be written to the file.

        Raises:
            IOError: If there's an error in writing to the file.
        """
        try:
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(text)
        except Exception as e:
            Util.print_with_spacing(
                f"Error writing to file '{file_path}': {e}")
            sys.exit()
