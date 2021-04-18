import os


image_file = "z.jpg"
# TODO: @Yogesh, introduce some means to check and use the appropriate command

command1 = 'python ocr.py --image-path {}' #for image
os.system(command1.format(image_file))


          
#command2 = 'python ocr.py --pdf-file {}' #for pdf
#os.system(command2.format(pdf_file))



# file will be saved in .txt format


command3 = 'python text_to_speech.py --file {} --channels {} --swidth {} --change-rate {}'
os.system(command3.format('text.txt', '1', '2', '0.5'))


# changed file saved by the name of changed.wav
# original file saved by name of okie.wav'
