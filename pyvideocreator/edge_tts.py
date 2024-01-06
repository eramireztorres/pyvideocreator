import subprocess

# class EdgeTTS:
#     def __init__(self):
#         self.base_command = "edge-tts"
    
#     def convert_text_to_audio(self, text, output_filename, voice="es-US-AlonsoNeural", rate=None, volume=None, subtitle_filename=None):
#         # Eliminar comillas internas del texto
#         sanitized_text = text.replace("\"", "")
        
#         # Construir el comando base
#         command = f"{self.base_command} --voice \"{voice}\" --text \"{sanitized_text}\" --write-media \"{output_filename}\""
        
#         # Añadir argumentos opcionales
#         if rate:
#             command += f" --rate=\"{str(rate)}\""
        
#         if volume:
#             command += f" --volume=\"{str(volume)}\""
        
#         if subtitle_filename:
#             command += f" --write-subtitles \"{subtitle_filename}\""
        
#         # Imprimir el comando para depuración
#         print(f"Executing command: {command}")
        
#         # Ejecutar el comando con PowerShell
#         try:
#             powershell_command = ["powershell.exe", "-Command", command]
#             completed_process = subprocess.run(powershell_command, shell=False, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             print(f"Texto a Audio terminado. {completed_process.stdout.decode('utf-8', errors='replace')}")
#         except subprocess.CalledProcessError as e:
#             print(f"An error occurred: {e}")
#             print(f"Stderr: {e.stderr.decode('utf-8', errors='replace')}")



import platform

class EdgeTTS:
    def __init__(self):
        self.os_type = platform.system()
        if self.os_type == 'Windows':
            self.base_command = "edge-tts"
        elif self.os_type in ['Linux', 'Darwin']:  # Darwin is macOS
            self.base_command = "edge-tts"  # or another command for Linux and macOS
        else:
            raise NotImplementedError("Unsupported Operating System")

    def convert_text_to_audio(self, text, output_filename, voice="default", rate=None, volume=None, subtitle_filename=None):
        # Remove internal quotes from the text
        sanitized_text = text.replace("\"", "")
        sanitized_text = sanitized_text.replace(':', '...')
        
        command = f"{self.base_command} --voice \"{voice}\" --text \"{sanitized_text}\" --write-media \"{output_filename}\""

        # # Construct the base command
        # if self.os_type == 'Windows':
        #     command = f"{self.base_command} --voice \"{voice}\" --text \"{sanitized_text}\" --write-media \"{output_filename}\""
        # else:
        #     command = f"{self.base_command} \"{sanitized_text}\" -o \"{output_filename}\""
        #     if voice != "default":
        #         command += f" --voice={voice}"
        #     # Add other parameters as per the syntax of the TTS command in Linux/macOS

        # Add optional arguments
        if rate:
            command += f" --rate={str(rate)}"
        if volume:
            command += f" --volume={str(volume)}"
        if subtitle_filename:
            command += f" --write-subtitles \"{subtitle_filename}\""

        # Execute the command
        try:
            if self.os_type == 'Windows':
                powershell_command = ["powershell.exe", "-Command", command]
                completed_process = subprocess.run(powershell_command, shell=False, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                completed_process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print(f"Text to Audio conversion completed. {completed_process.stdout.decode('utf-8', errors='replace')}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            print(f"Stderr: {e.stderr.decode('utf-8', errors='replace')}")


# Ejemplo de uso
#if __name__ == "__main__":
    #tts = EdgeTTS()
#tts.convert_text_to_audio("Hola mundo", "output.wav")


