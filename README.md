Setup by running 
> pip install -r requirements.txt


Description of repo contents:
1. base/
  Core, shared functionality

  board.py: Base gameboard that may be useful for other games
  colors.py: (R, G, B) color codes useful for customization
  score\_keeper: Helper score keeper for any game


2. app/
  Games ready for team play/prototyping

  Game:
		  Hidden Gem Sweeper
				(i.e. Wayfair-themed Mine Sweeper)

  Files:
    gem\_board.py: Hidden gems board functionality
    play\_gem\_sweeper.py: Driver

  Rules:
    Click anywhere on the 10x10 board to start. As you click, you'll
    uncover numbers, gray squares, and hidden gems. Numbers tell
    you how many gems the box you clicked touches.  Gray boxes mean
    that the box touches 0 gems; find one of these, and you'll get
    some boxes for free. Finally, gem boxes are the things to avoid;
    hit a gem, and you lose.
  
    You can protect yourself from mistakes by right clicking a
    box you suspect to hold a gem; if you right click again,
    the protection goes away and you're free to click the box again.
  
    Win the game by finding all 90 gem-free locations.

  How to play:
		  > python play\_gem\_sweeper.py


3. userdev/
  Location for user game development
