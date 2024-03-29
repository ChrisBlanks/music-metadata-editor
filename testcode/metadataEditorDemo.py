#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Date: Late June 2019
Purpose: This script is the metadata editor demo application.
"""

import os.path
from os.path import sep, expanduser
import sys

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

#Backend functions modules
import metadataTagFunctions as mdt
import musicConversionFunctions as mcf


class ChrisWindow(GridLayout):
    #Class variables    
    red=1
    green=1
    blue=1
    alpha=1
    color_vector = [red,green,blue,alpha]

    def __init__(self,**kwargs):
        super().__init__(**kwargs) #call __init__() of parent
        self.cols= 1           #initial configuration for start page
        
        self._acquireInputFile()
        self._setupStartPage()


    def getColorVector(self):
        """Returns the class variable color_vector."""
        return self.color_vector


    def _acquireInputFile(self):
        """Sets the input file depending on whether a CLI was given."""
        if len(sys.argv) > 1:
            self.cur_file= sys.argv[1]

            #get full path of input file; may need to be updated
            self.cur_file = os.path.abspath(self.cur_file)
            print(self.cur_file)
        else:
            self.cur_file="None"


    def _setupStartPage(self):
        """Creates the start page for the application."""
        startup_page_label = Label(text="Metadata Music Editor",font_size="50sp")
        self.add_widget(startup_page_label)
        start_but = Button(text="Start Editing File",background_color=self.color_vector,size_hint_x=0.5,size_hint_y=0.1)
        start_but.bind(on_press= self._transferToEditor)
        self.add_widget(start_but)
    
    
    def _transferToEditor(self,instance):
        """Clears startup page to populate root with editor widgets"""
        self.clear_widgets()
        self.cols=2               #update number of columns for new window
        self._setupEditorWindow()
    
    
    def _setupEditorWindow(self):
        """Creates the widget items, their attributes, and their callbacks. """
        self.input_widget_store = []
        
        self.cur_file_label = Label(text="File being edited: {}".format(self.cur_file))
        self.add_widget(self.cur_file_label)

        #Apply changes button
        self.apply_but = Button(text="Apply Changes?",background_color=self.color_vector)
        self.apply_but.bind(on_press=self._applyChangesCallback)
        self.add_widget( self.apply_but )
        
        #Name of song
        self.name_label = Label(text="Track Name:", color=self.color_vector,font_size=20)
        self.add_widget( self.name_label)
        
        self.name_input = TextInput(multiline=False)
        self.add_widget(self.name_input)
        
        self.input_widget_store.append(self.name_input)

        #Artist of song
        self.artist_label = Label(text="Artist Name:", color=self.color_vector,font_size=20)
        self.add_widget( self.artist_label)
        
        self.artist_input = TextInput(multiline=False)
        self.add_widget(self.artist_input)
        
        self.input_widget_store.append(self.artist_input)
        
        #Track Number of song
        self.track_num_label = Label(text="Track Number:", color=self.color_vector,font_size=20)
        self.add_widget( self.track_num_label)
        
        self._createTrackNumberWidget()  #Setup a grid within the parent grid layout
        
        #Album name of song
        self.album_label = Label(text="Album Name:", color=self.color_vector,font_size=20)
        self.add_widget( self.album_label)
        
        self.album_input = TextInput(multiline=False)
        self.add_widget(self.album_input)
        
        self.input_widget_store.append(self.album_input)
        
        # Date of song
        self.date_label = Label(text="Release Date (mon/day/yr):", color=self.color_vector,font_size=20)
        self.add_widget( self.date_label)
        
        self.date_input = TextInput(multiline=False)
        self.add_widget(self.date_input)
        
        self.input_widget_store.append(self.date_input)
        
        # Genre of song
        self.genre_label = Label(text="Genre:", color=self.color_vector,font_size=20)
        self.add_widget( self.genre_label)
        
        self.genre_input = TextInput(multiline=False)
        self.add_widget(self.genre_input)
        
        self.input_widget_store.append(self.genre_input)
       
        #Get pic button
        self.select_pic_but = Button(text="Find cover art.",background_color=self.color_vector)
        self.select_pic_but.bind(on_press=self._acquireCoverArt)
        self.add_widget(self.select_pic_but)

        self.pic_selection = "No picture selected." #variable for storing file path of image that is selected

        #Convert to Flac option
        self.conversion_spinner = Spinner(text="No conversion.",values=("No conversion","Convert to Flac."))
        self.add_widget(self.conversion_spinner)

    

    def _createTrackNumberWidget(self):
        """Creates a combined widget to be embedded into the editor view."""
        self.embedded_box = GridLayout(cols=2)
        track_color= [0,0,1,1]
        self.track_num_widget = Slider(min=1,max=15,value=1,value_track=True,
                                        step=1,value_track_color=track_color)
        self.track_num_inner_label = Label(text=str(self.track_num_widget.value),
                                            color=track_color,size_hint_x=0.3)
        
        def updateInnerLabel(instance,value):
            """Callback for updating inner label to display slider value."""
            self.track_num_inner_label.text = str(value)
            
        self.track_num_widget.bind(value= updateInnerLabel)
        
        self.embedded_box.add_widget(self.track_num_widget)
        self.embedded_box.add_widget(self.track_num_inner_label)
        
        self.add_widget(self.embedded_box)

    
    def _acquireCoverArt(self,instance):
        """Creates a window for the user to select a cover art image from the file system."""
        self.pic_selection = "No picture selected."

        user_path = expanduser('~')+sep+'Pictures'
        
        self.file_chooser = FileChooserListView(path=user_path,filters=["*.jpg","*.jpeg","*.png"])
        self.file_chooser.bind(on_submit=self._retrieveFileSelection)
        
        self.close_button = Button(text="Close",size_hint_y=None,height=30)
        self.close_button.bind(on_press=self._dismissFileSelectionWindow)
        
        self.file_chooser_grid = GridLayout(rows=2)
        self.file_chooser_grid.add_widget(self.close_button)
        self.file_chooser_grid.add_widget(self.file_chooser)

        self.file_chooser_window = Popup(title="Image Selector",content=self.file_chooser_grid)
        self.file_chooser_window.open()


    def _retrieveFileSelection(self,instance,selection,touch):
        """Prints file when it is sucessfully retrieved."""
        print("Retrieved: {}".format(selection[0]))
        self.pic_selection = selection[0]
        self.file_chooser_window.dismiss() 


    def _dismissFileSelectionWindow(self,instance):
        """Handles the dismiss event of the popup window for selecting an image file."""
        if self.pic_selection=="No picture selected.":
            print("Failure to retrieve file image.")
        else:
            print("Retrieved an image file successfully.")
        self.file_chooser_window.dismiss()


    def _applyChangesCallback(self,instance):
        """Callback() for button widget. """
        print("Button was pressed for the `{}` widget.\n".format(instance.text) )
        
        self.needToConvert = False #controls whether input file must be converted to flac
        self.needToChangeCoverArt= False #controls whether the cover art image will be changed

        self.tag_pairs = [] #a list of lists w/ 1st element as TAG to change & 2nd as value
        self.possible_tags = ["TITLE","ARTIST","ALBUM","DATE","GENRE","TRACKNUMBER"]
        
        count = 0
        for input_wig in self.input_widget_store:
            pair = []
            
            if input_wig.text == "": #checks for empty strings & inapproriate names
                print("Input is invalid -> \'{}\'".format(input_wig.text))
            else:
                pair.append(self.possible_tags[count]) #append corresponding tag
                pair.append(input_wig.text)
                self.tag_pairs.append(pair)
                    
            count = count +1

        self.tag_pairs.append( ["TRACKNUMBER",self.track_num_widget.value] )
        print(int(self.track_num_widget.value))
        
        self.tag_pairs.reverse() #changes TITLE tag last because it causes file name to change

        print(self.conversion_spinner.text)

        if self.conversion_spinner.text != "No conversion." and ".flac" not in self.cur_file:
            self.needToConvert= True

        print(self.pic_selection)
        if self.pic_selection != "No picture selected.":
            self.needToChangeCoverArt= True

        self.clear_widgets()
        
        #maybe put a wait screen here: self._showWaitScreen()
        self._applyChanges()
        self._setupFinishScreen()


    def _applyChanges(self):
        """Performs any changes requested via GUI."""
        
        if self.needToConvert:
            self.cur_file = mcf.convertFileToFlac(self.cur_file) #convert to flac & update file name
        
        if self.needToChangeCoverArt:
            mdt.setCoverArt(self.pic_selection,self.cur_file)
        
        if self.cur_file == 'None' or ".flac" not in self.cur_file:
            print("Invaid input file.")
        else:
            for i in range(len(self.tag_pairs)):
                mdt.changeTagValue(self.tag_pairs[i][0],self.tag_pairs[i][1],self.cur_file)


    def _setupFinishScreen(self):
        """Shows final screen if changes worked."""
        self.add_widget(Label(text="Done. Please, exit the application."))
        return


class MetaEditorApp(App):
    def build(self):
        """Establishes root widget for application."""
        self.root = ChrisWindow()
        return self.root


if __name__ == "__main__":

    app = MetaEditorApp()
    app.run()
