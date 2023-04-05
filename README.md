# Ballz Recreation
Trying to recreate the ballz mobile game on pc. In python...

# How to run
If you really want to run it heres a step by step guide.
- install python 3.9
- import pygame
- run main script

# How it works
If you are using this repo to try and learn from it good luck. This thing was made by adding on features and structure as i went. But i can still give a pretty good rundown

- # Bricks 
  - Bricks come in 2 diffrent forms square and triangle
    - Squares are simple. They are just a rectangle that can be drawn with pygame's draw rect function
    - Triangles are complacated. They require pygames draw polygon function whitch mean i need the exact set of points to draw them.
- # Balls
  - Very simple. just a circle drawn with the pygame draw circle command.
  - Has a time (t) that indicates its position in the raycast.

- # Mechanics
  - Movement: Every frame the ball moves a certin distence in its pre-defied tregectory. This tregectory is just a raycast reflecting arround 
  - HP: At the time (t) where the ball bounces on a non-floor brick the brick looses 1 hp
