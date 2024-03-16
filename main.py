# generate_your_mushroom
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # import messagebox
import os
from mushroom_class import Mushroom, MushroomDatabase
from PIL import Image, ImageTk

def open_part_image(part, attribute):
    """
    Open an image file for the given part attribute.
    """
    filename = f"C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\images\\{part}\\{attribute}.png"
    return Image.open(filename)


def create_mushroom_image(parts, filename=None):
    """
    Create a composite image of a mushroom from the provided parts.
    """
    # Load the background/biome image
    bg_image = open_part_image('growth_biome', parts['biome'])

    # Open all the part images
    stem_image = open_part_image('stem', parts['stem'])
    margin_image = open_part_image('cap_margin', parts['cap_margin'])
    cap_shape_image = open_part_image('cap_shape', parts['cap_shape'])

    # Composite dimensions should match the size of the box where all these parts will be placed
    composite = Image.new('RGBA', bg_image.size)
    
    # Paste the images onto the composite image
    composite.paste(bg_image, (0, 0))
    composite.paste(stem_image, (150, 200), stem_image.split()[3] if stem_image.mode == 'RGBA' else None)
    composite.paste(margin_image, (50, 200), margin_image.split()[3] if margin_image.mode == 'RGBA' else None)
    composite.paste(cap_shape_image, (25, 20), cap_shape_image.split()[3] if cap_shape_image.mode == 'RGBA' else None)

    # Save the image to filename if provided
    if filename is not None:
        composite.save(filename)

    return composite


class MushroomGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Mushroom Generator')

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.export_button = ttk.Button(self.mainframe, text='Export', command=self.export_mushroom, state='disabled')
        self.export_button.grid(column=2, row=1)

        # Generate button
        self.generate_button = ttk.Button(self.mainframe, text='Generate', command=self.generate_mushroom)
        self.generate_button.grid(column=1, row=1)

        # Text area for mushroom description
        self.desc_text = tk.StringVar()
        self.desc_label = ttk.Label(self.mainframe, textvariable=self.desc_text, wraplength=600)
        self.desc_label.grid(column=1, row=2)

        # Image for mushroom
        self.image_label = ttk.Label(self.mainframe)
        self.image_label.grid(column=1, row=3)
        self.default_image = tk.PhotoImage(file='C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\placeholder_mushroom.png')  # Placeholder image path
        self.image_label['image'] = self.default_image

    def export_mushroom(self):
        '''
        Export the mushroom to a text file and an HTML file.
        '''
        # Check if a Mushroom has been generated, yet.
        ## If not- Provide an alert to the user. 
        if not hasattr(self, 'mushroom'):
            messagebox.showinfo("Exporter", "Please generate a mushroom before exporting!")
            return
        
        # File name shall be the adjective + _ + the noun.
        file_name = f"{self.mushroom.adjective}_{self.mushroom.noun}"
        txt_description, html_description = self.mushroom.export_description()

        with open(f"C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\{file_name}.txt", 'w') as file:
            file.write(txt_description)

        with open(f"C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\{file_name}.html", 'w') as file:
            file.write(html_description)

        img_filename = f"C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\{file_name}.png"
        create_mushroom_image(self.parts, filename=img_filename)
        messagebox.showinfo("Exporter", f"Exported data to 'C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\{file_name}'")

    def generate_mushroom(self):
        """Call this to generate a new mushroom and update the GUI."""
        # Create database and mushroom instance
        db = MushroomDatabase('C:\\Users\\Haesh\\Documents\\GitHub\\mushroom_generator\\mushroom_data.db')
        self.mushroom = Mushroom(db)

        # Generate a new mushroom
        self.mushroom.generate()

        # Define parts
        self.parts = {
            'biome': self.mushroom.growth_biome[3],
            'stem': self.mushroom.stem[2],
            'cap_margin': self.mushroom.cap_margin[2],
            'cap_shape': self.mushroom.cap_shape[2]
        }

        # Generate mushroom image
        mushroom_image = create_mushroom_image(self.parts)

        # Get a string description of the mushroom
        desc = str(self.mushroom)

        # Update the description on the GUI
        self.desc_text.set(desc)
        
        self.export_button.config(state='normal')  # Enable export button
        
        # Convert PIL Image to PhotoImage to use in tkinter
        self.image_tk = ImageTk.PhotoImage(mushroom_image)
        
        # Update Image on GUI
        self.image_label['image'] = self.image_tk

# Run the application
app = MushroomGenerator()
app.mainloop()