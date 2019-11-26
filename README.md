# ConwaysGame
Conway's Game of Life written in Python, using Pygame as a graphics window.

The plane is infinite, as cells are stored as tuples rather than in a list-of-lists grid.
The game begins paused, and can be started by pressing Enter.

Controls:
  Z - Zoom in
  X - Zoom out
  C - Snap zoom to nearest whole pixel
  Arrow keys/wasd - Move
  Shift - Hold to move faster
  Enter - Pause/Resume
  Left mouse button - Place a cell
  Right mouse button - Remove a cell
  
Zooming fills pixels using nearest-neighbor; Snapping the zoom by pressing C makes the cells pixel-perfect.
