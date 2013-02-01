TimeFlow
========

Play with your time-series data.


Anatomy of a time-series data analyis
-------------------------------------

So you have some data you want to look at. Let me guess, you're going to need:

 1. An import routine to fetch the data

 2. One, or a series of, routines acting upon the data.
 
 3. Routines to plot the output of the routines, or export to some format.


Sound familiar?

When you think of working with data, #2 is probably the one you think of. It's
juicy part that takes creativity and inginuity. It's fun!

The problem is that numbers 1 and 3 and the extra work between steps is not fun.
The time it will take is hard to estimate (or even remember to consider). Even
with high-level tools like python and matlab, the overhead around actually doing
analysis on time-series data is annoying.


Why TimeFlow?
-------------

Before going into what TimeFlow is, here's why I built it:

 1. Numpy, matlab, and other high-level tools commonly used for processing time-
    series data make the hard things easy, but don't give enough help with the
    tedious overhead associated with working on time-series data.

 2. Higher-level data tools make too many. I'm making stuff up here, I just
    wanted to have a second point. Maybe something better already exists. Blah.


Where is TimeFlow useful?
-------------------------

TimeFlow seeks to augment your data-processing workflow by making one critical
assumption:

*Your dataset consists of rows of values with one independant variable*

The set of problems meeting that criteria have a lot in common when it comes
to workflows for solving them, and TimeFlow simply seeks to fill this gap.

Consider a small meteorological station. If you have a log of the outputs of
your intruments (say you have a thermometer, barometer, anemometer, and a
pyranometer) every minute. In that case, time is your independant varible,
for which you have readings of sensor values. Perfect!

While the tools and routines included with TimeFlow are selected for their
applicability to data with a single independant variable, it is not limited
to that domain. The routine-dependancy framework and input/output methods
in the BaseRoutine class might be useful for a wide variety of data-processing
applications.


What is TimeFlow?
-----------------

There are two main components of TimeFlow:

1. A `BaseRoutine` abstract class (and some more specific subclasses simple
   concrete ready-to-go subclasses) to organize your workflow into steps.

2. A yaml-based declarative syntax of describing your workflow.

3. A script for running 


The author is talented at counting and mental math.


What else to I need?
--------------------

 * **Numpy** -- TimeFlow uses numpy `ndarray`s internally for all data.


So... where is it?
------------------

Sounded too good to be true? I guess it is, at least for now. I'm working on it.
If you want to help out, let me (uniphil) know.


Docz plz?
---------

read em up: 

