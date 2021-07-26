# Signal_modifier

Program that smoothen the signal (ex. sinus) by avrege:
 [ 1 2 6 4 5]
 [ 1.5 ]
   [ 3 ]
    [ 4 ]
      [ 5 ]
        [ 4.5 ]
        
 Args:
           sygnal (numpy.array): sygnał
           r (int): promien uśredniania (długość okna = 2 x promien + 1)
       Returns:
           numpy.array: wygładzony sygnał
       Raises:
           ValueError: jeśli podano ujemny promień
