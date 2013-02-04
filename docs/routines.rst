Routines
========

Routines are the building blocks of TimeFlow workflows. If you are scripting in
python, you can use them directly. Support for building non-python algorithms
into TimeFlow routines is planned.


Base Classes
------------

RoutineBase
^^^^^^^^^^^

An abstract base class that gives the basic TimeFlow mechanics for free.

routines just import and then export.

when something calls one of their exports, they try to import whatever is
necessary and then give the result.

future plan: ask if data has changed (which gets propagated all the way up to
the first file, or other thing that has actually changed. if nothing changed,
reply with the memoized value.)

Stores data internally on the [something] property.


Routine Cycle
~~~~~~~~~~~~~

#. The routine is asked if its data has changed.

    * if it knows, it can respond right away.
    * if it depends on whether a dependency's data has changed, it passes
      the request up the chain, and passes the response back down.

#. The routine may be asked for its data, possibly with arguments.
#. The routine may ask a dependency for data.
#. The routine provides gives the data back.

The first and last routines in a chain are special. The first one can get its
data from wherever it wants, but must still provide returned data in the
standard timeflow format. The last one has to get data in that format, but may
return data in an arbirary format. Or do anything, like open a plot.


How do Routines Affect Data?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a routine is asked for its output, it should return one of

* The original table augmented with one or more extra columns
* The original table, with modifications to values in one or more columns

Routines may accept arguments with data requests, and return data in a form
appropriate to the arguments. For example, a filter might, by default, add a
column to the data annotating whether a row passed or failed a criteria. Passing
the routine an :code:`if` argument when requesting data could cause it to instead
remove rows which pass or fail the criteria.


Built-in Routines
-----------------

The built-in routines are useful on their own, but also designed to be
subclassed. Extend away!


File
^^^^

Import data from a variety of formats

eventually this will have an answer for whether the file has changed.


Export
^^^^^^

numpy, pickle, csv, ...


Plot
^^^^

make pretty graphs


