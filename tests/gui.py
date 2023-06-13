import PySimpleGUI as sg

def create_text(text, size=(15, 1), font=("Helvetica", 14)):
    return sg.Text(text, size=size, font=font)

def create_button(text, key, font=("Helvetica", 14)):
    return sg.Button(text, key=key, font=font)

IMU_data_labels = ['Heading:', 'Pitch:', 'Roll:']
Acoustic_data_labels = [('Sound Velocity:', 'sound_velocity'), ('Frequency:', 'frequency'), ('Signal Strength:', 'signal_strength')]

IMU_layout = [[create_text(label, size=(20, 1)), sg.Text('0', size=(20, 1), font=("Helvetica", 14))] for label in IMU_data_labels]
Acoustic_layout = [[create_text(label, size=(20, 1)), sg.Text('0', size=(20, 1), font=("Helvetica", 14)) if key != 'signal_strength'
                   else sg.ProgressBar(100, orientation='h', size=(20, 20), key=key)]
                   for label, key in Acoustic_data_labels]

layout = [
    [
        create_text('Surface Station', size=(30, 1), font=("Helvetica", 25)),
    ],
    [
        sg.Column([
            [create_text('AUV Configuration', size=(20, 1))],
            # Additional layout code can be inserted here...
        ], size=(320, 1080)),

        sg.Column([
            [sg.Image('imgs/placeholder.png', key='camera_feed', size=(1280, 720))],
            # Additional layout code can be inserted here...
        ], size=(1280, 1080)),

        sg.Column([
            [create_text('IMU Data', size=(20, 1))],
            IMU_layout,
            [sg.HorizontalSeparator()],
            [create_text('Acoustics Data', size=(20, 1))],
            Acoustic_layout,
            [sg.HorizontalSeparator()],
            [create_button('Save Settings', key='save_settings')],
            [create_button('Load Settings', key='load_settings')],
            [create_button('Reset', key='reset')],
            [create_button('Exit', key='exit')],
        ], size=(320, 1080)),
    ],  
]

# Create a dictionary of sg.Text objects for updating later.
text_objects = {
    'IMU_heading': window['IMU_heading'],
    'IMU_pitch': window['IMU_pitch'],
    'IMU_roll': window['IMU_roll'],
    'sound_velocity': window['sound_velocity'],
    'frequency': window['frequency']
}

# When you want to update a text field later on in your code, use the following syntax:
text_objects['IMU_heading'].update('new_value')
