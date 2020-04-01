## Repo Organization
1. **base/**  
Core and shared functionality  

   **Files**   
`board.py`: Base gameboard that may be useful for other games
`colors.py`: (R, G, B) color codes useful for customization
`score_keeper.py`: Helper score keeper class 

2. **userdev/**  
Location for user/team game development

3.  **app/**  
Games ready for team play/prototyping  

   **Files**  
    `gem_board.py`: Hidden gems board functionality
    `play_gem_sweeper.py`: Driver

## Current Games  
1. **Title**  
Hidden Gem Sweeper (i.e. Wayfair-themed Mine Sweeper)  

   **Rules**   
  Click anywhere on the 10x10 board to start. As you click, you'll uncover numbers, gray squares, and hidden gems. Numbers tell  you how many gems the box you clicked touches.  Gray boxes mean that the box touches 0 gems; find one of these, and you'll get some boxes for free. Finally, gem boxes are the things to avoid; hit a gem, and you lose.  

   You can protect yourself from mistakes by right clicking a box you suspect to hold a gem; if you right click again, the protection goes away and you're free to click the box again.  

    Win the game by finding all 90 gem-free locations.

  **How to play**  
    `> python play_gem_sweeper.py`


