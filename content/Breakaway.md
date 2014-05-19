Title: Breakaway
Date: 2013-08-30
Category: not software
tags: robotics
status: draft

#Introduction

In high school I was involved in the robotics team. We participated in the
[*FIRST* Robotics Competition](http://www.usfirst.org/roboticsprograms/frc).

Each year they came up with a new game for our robots to play and we would get 6
weeks to design, build, and test the robot. In 2010 we had to play a sort of
modified soccer:

<center>
<iframe width="420" height="315" src="//www.youtube.com/embed/IEHAj3EmpMw"
frameborder="0" allowfullscreen></iframe>
</center>

For months this was my life and blood; here are some anecdotes from then.

## Designing the Robot

### Drivetrain

The field was split into three parts by big speed bumps. We wanted to be able to
move between the sections, so we needed to be able to go over the bumps. This
was challenging because most existing robot drivetrains didn't have enough ground
clearance to avoid getting stuck on the bumps.

After considering several complicated designs with jointed, articulating
drivetrains, I decided to try putting some big wheels on the simple 6-wheel
drivetrain we had been using in the past. It easily cleared the bump.

Then I spent some time redesigning the drivetrain in SolidWorks to improve on
the previous year's design and add some strength in anticipation of falling
over.

**graduation dt image**

**freyja dt image**

This set a good precedent of trying the dumbest thing possible before spending
time on hard things.

### Accumulator

We also needed to somehow control the soccer balls. We were not allowed to have
more than 3" of the ball inside the robot.

We were considering two broad classes of designs: roller-based and
suction-based.

The idea behind the roller-based design was that we could give the ball
backspin. Then the ball would try to roll towards our robot, which would give it
more backspin. This apparently works very well with ping-pong balls.

However, it didn't work great for us. Our roller was relatively high up, and
when we ran into the ball we pushed down on it very hard. So the ball stayed
still and the robot climbed over it. But if we were gentle the ball would stick
with us.

While we were playing around with the roller we were also trying out some
suction cups made from thin plastic. They were unable to form a good enough seal
to hold on to the ball.

We spent a long time trying to get the rollers to work well. One morning, we

  * accumulator
    * got to competition - duh! double roller
      * pinch vs idle
  * kicker
    * quick prototype
    * how to make variable?
      * dog gears
      * ratchet
  * attempt at chokehold strategy
    * make a ramp that redirects
    * built the thing in 1 week
    * it didn't work
      * also I became deathly ill
    * lesson: don't pivot a week before launch
