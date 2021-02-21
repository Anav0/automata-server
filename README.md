# Drawing automata

## Web application created to help my fellow students create nice DFA automatons and then minimise them using variouse alghorithms (Moore etc.)
Backend can also read automata from .txt and minimize them that way.

- Typescript
- Canvas
- No fancy frontend framework 
- math math math math
- Python as backend (for minimization: https://github.com/Anav0/automata-server)
- Frontend (https://github.com/Anav0/drawing-automata)

![DFA automaton](https://github.com/Anav0/drawing-automata/blob/master/drawing-automata%20(1).jpeg)


#### P.S Aby parsowanie automatu z pliku działało poprawnie trzeba mieć kilka rzeczy na względzie:

- Kolumny powinny być oddzielone 1 tabem.
- ' na końcu nazwy stanu oznacza stan akceptujący.
- \_ na końcu nazwy stanu oznacza stan początkowy.
- Pierwsza linia zaczyna się dwoma tabami i określa symbole alfabetu.
- nazwy symboli i stanów muszą być liczbami, poczynając od 0.
